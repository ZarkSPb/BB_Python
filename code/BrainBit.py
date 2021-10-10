import sys

import numpy as np
from brainflow.board_shim import BoardIds, BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, DetrendOperations, FilterTypes
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import (QPointF, QThreadPool, QTimer)
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QMainWindow

from ui_mainwindow import Ui_MainWindow
from worker import Worker

# configuring BB
BOARD_ID = BoardIds.SYNTHETIC_BOARD.value
# BOARD_ID = BoardIds.BRAINBIT_BOARD.value
SAMPLE_RATE = BoardShim.get_sampling_rate(BOARD_ID)  # 250
EXG_CHANNELS = BoardShim.get_exg_channels(BOARD_ID)
NUM_CHANNELS = len(EXG_CHANNELS)
MAX_CHART_SIGNAL_DURATION = 20  # seconds
UPDATE_SPEED_MS = 20
SIGNAL_CLIPPING_SEC = 2

if BOARD_ID == BoardIds.SYNTHETIC_BOARD.value:
    NUM_CHANNELS = 4
    EXG_CHANNELS = EXG_CHANNELS[:NUM_CHANNELS]


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.threadpool = QThreadPool()

        self.charts = []

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # --------------------BUTTON CONNECT--------------------
        self.ui.ButtonConnect.clicked.connect(self._connect)
        self.ui.ButtonStart.clicked.connect(self._start_capture)
        self.ui.ButtonStop.clicked.connect(self._stop_capture)
        self.ui.ButtonDisconnect.clicked.connect(self._disconnect)

        # --------------------CHART MAKE--------------------
        self.channel_names = BoardShim.get_board_descr(
            BOARD_ID)['eeg_names'].split(',')

        self.serieses = []
        self.chart_buffers = []
        for channel_name in self.channel_names[:NUM_CHANNELS]:
            chart_view = QChartView(self.create_line_chart(channel_name))
            chart_view.setRenderHint(QPainter.Antialiasing, True)
            self.ui.verticalLayout_3.addWidget(chart_view)
            self.charts.append(chart_view)

        self.ui.SliderDuration.setMaximum(MAX_CHART_SIGNAL_DURATION)
        self.ui.SliderDuration.setValue(MAX_CHART_SIGNAL_DURATION)
        self.ui.SliderDuration.setSliderPosition(MAX_CHART_SIGNAL_DURATION)

        self.update()

    # --------------------UPDATE UI--------------------
    def update(self):
        self.chart_duration = self.ui.SliderDuration.value()
        text = "Duration (sec): " + str(self.chart_duration)
        self.ui.LabelDuration.setText(text)

        for chart_view in self.charts:
            chart_view.chart().axisX().setRange(
                0, SAMPLE_RATE * self.chart_duration)

        chart_amplitude = self.ui.SliderAmplitude.value()
        text = "Amplitude (uV): " + str(chart_amplitude)
        self.ui.LabelAmplitude.setText(text)
        for chart_view in self.charts:
            chart_view.chart().axisY().setRange(-chart_amplitude,
                                                chart_amplitude)

    # --------------------CHART CREATE--------------------
    def create_line_chart(self, chartname):
        chart = QChart()
        # chart.setTitle(chartname)
        chart.legend().hide()

        series = QLineSeries()
        self.serieses.append(series)
        chart.addSeries(self.serieses[-1])

        axis_x = QValueAxis()
        axis_x.setRange(0, SAMPLE_RATE)
        axis_y = QValueAxis()
        axis_y.setRange(-50, 50)
        axis_y.setTitleText(chartname)
        chart.setAxisX(axis_x, self.serieses[-1])
        chart.setAxisY(axis_y, self.serieses[-1])

        self.chart_buffers.append([
            QPointF(x, 0)
            for x in range(MAX_CHART_SIGNAL_DURATION * SAMPLE_RATE)
        ])

        self.serieses[-1].append(self.chart_buffers[-1])
        return chart

    def signal_filtering(self, data):
        DataFilter.detrend(data, DetrendOperations.CONSTANT.value)
        DataFilter.perform_bandpass(data, SAMPLE_RATE, 16.0, 28.0, 4,
                                    FilterTypes.BUTTERWORTH.value, 0)
        DataFilter.perform_bandpass(data, SAMPLE_RATE, 16.0, 28.0, 4,
                                    FilterTypes.BUTTERWORTH.value, 0)
        DataFilter.perform_bandstop(data, SAMPLE_RATE, 50.0, 4.0, 4,
                                    FilterTypes.BUTTERWORTH.value, 0)
        DataFilter.perform_bandstop(data, SAMPLE_RATE, 60.0, 4.0, 4,
                                    FilterTypes.BUTTERWORTH.value, 0)

    def redraw_charts(self):
        # only for draw ???
        data = self.board.get_current_board_data(
            (self.chart_duration + SIGNAL_CLIPPING_SEC) *
            SAMPLE_RATE)[EXG_CHANNELS, :]

        if np.any(data):
            for channel in range(NUM_CHANNELS):
                self.signal_filtering(data[channel])
                redraw_data = data[channel, SIGNAL_CLIPPING_SEC * SAMPLE_RATE:]
                for s in range(redraw_data.shape[0]):
                    self.chart_buffers[channel][s].setY(redraw_data[s])
                self.serieses[channel].replace(self.chart_buffers[channel])

    def connect_toBB(self):
        params = BrainFlowInputParams()
        self.board = BoardShim(BOARD_ID, params)
        self.board.prepare_session()

    def result_connect_toBB(self):
        self.ui.ButtonStart.setEnabled(True)
        self.ui.ButtonDisconnect.setEnabled(True)

    # --------------------BUTTONS--------------------
    def _connect(self):
        self.ui.ButtonConnect.setEnabled(False)

        worker = Worker(self.connect_toBB)
        worker.signals.result.connect(self.result_connect_toBB)
        self.threadpool.start(worker)

    def _start_capture(self):
        self.ui.ButtonStart.setEnabled(False)
        self.ui.ButtonDisconnect.setEnabled(False)
        self.ui.ButtonStop.setEnabled(True)

        # CHART buffer renew
        self.chart_buffers = []
        for i in range(NUM_CHANNELS):
            self.chart_buffers.append([
                QPointF(x, 0) for x in range(self.chart_duration * SAMPLE_RATE)
            ])

        self.board.start_stream(450000)
        data = self.board.get_board_data()

        self.timer = QTimer()
        self.timer.timeout.connect(self.redraw_charts)
        self.timer.start(UPDATE_SPEED_MS)

    def _stop_capture(self):
        self.timer.stop()

        self.board.stop_stream()

        self.ui.ButtonStart.setEnabled(True)
        self.ui.ButtonDisconnect.setEnabled(True)
        self.ui.ButtonStop.setEnabled(False)

    def _disconnect(self):
        # Release all BB resources
        if self.board.is_prepared():
            self.board.release_session()

        self.ui.ButtonDisconnect.setEnabled(False)
        self.ui.ButtonConnect.setEnabled(True)
        self.ui.ButtonStart.setEnabled(False)


def main():
    BoardShim.enable_dev_board_logger()

    # Create the Qt application
    app = QApplication(sys.argv)
    # Create window
    window = MainWindow()
    window.show()

    # Run the main Qt loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

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

# Configuring BB
BOARD_ID = BoardIds.SYNTHETIC_BOARD.value
# BOARD_ID = BoardIds.BRAINBIT_BOARD.value

# Getting BB settings
SAMPLE_RATE = BoardShim.get_sampling_rate(BOARD_ID)  # 250
EXG_CHANNELS = BoardShim.get_exg_channels(BOARD_ID)
NUM_CHANNELS = len(EXG_CHANNELS)
EEG_CHANNEL_NAMES = BoardShim.get_eeg_names(BOARD_ID)
RESISTANCE_CHANNELS = BoardShim.get_resistance_channels(BOARD_ID)

# Chart setting
MAX_CHART_SIGNAL_DURATION = 20  # seconds
UPDATE_CHART_SPEED_MS = 40
SIGNAL_CLIPPING_SEC = 2
UPDATE_IMPEDANCE_SPEED_MS = 500

if BOARD_ID == BoardIds.SYNTHETIC_BOARD.value:
    NUM_CHANNELS = 4
    EXG_CHANNELS = EXG_CHANNELS[:NUM_CHANNELS]
    EEG_CHANNEL_NAMES = EEG_CHANNEL_NAMES[:4]


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.threadpool = QThreadPool()

        self.charts = []

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # --------------------CHART MAKE--------------------
        self.channel_names = BoardShim.get_board_descr(
            BOARD_ID)['eeg_names'].split(',')

        self.serieses = []
        self.chart_buffers = []
        for channel_name in self.channel_names[:NUM_CHANNELS]:
            chart_view = QChartView(self.create_line_chart(channel_name))
            chart_view.setRenderHint(QPainter.Antialiasing, True)

            self.ui.LayoutCharts.addWidget(chart_view)
            self.charts.append(chart_view)

        self.ui.SliderDuration.setMaximum(MAX_CHART_SIGNAL_DURATION)
        self.ui.SliderDuration.setValue(MAX_CHART_SIGNAL_DURATION)
        self.ui.SliderDuration.setSliderPosition(MAX_CHART_SIGNAL_DURATION)

        # --------------------Impedance label fill--------------------
        self.ui.LabelCh0.setText(f'{EEG_CHANNEL_NAMES[0]} (Ohm):')
        self.ui.LabelCh1.setText(f'{EEG_CHANNEL_NAMES[1]} (Ohm):')
        self.ui.LabelCh2.setText(f'{EEG_CHANNEL_NAMES[2]} (Ohm):')
        self.ui.LabelCh3.setText(f'{EEG_CHANNEL_NAMES[3]} (Ohm):')

        self.update_ui()

    # --------------------UPDATE UI--------------------
    def update_ui(self):
        self.chart_duration = self.ui.SliderDuration.value()
        text = "Duration (sec): " + str(self.chart_duration)
        self.ui.LabelDuration.setText(text)

        # renwe chart params
        for chart_view in self.charts:
            chart_view.chart().axisX().setRange(
                0, SAMPLE_RATE * self.chart_duration)

        # renew buffer size
        self.chart_buffers = []
        for i in range(NUM_CHANNELS):
            self.chart_buffers.append([
                QPointF(x, 0) for x in range(self.chart_duration * SAMPLE_RATE)
            ])

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

    def impedance_update(self):
        # --------------------Impedance label fill--------------------
        data = self.board.get_current_board_data(1)

        if np.any(data) > 0:
            data = data[RESISTANCE_CHANNELS, 0]

            self.ui.LabelCh0.setText(
                f'{EEG_CHANNEL_NAMES[0]} (Ohm): {data[0]:.0f}')
            self.ui.LabelCh1.setText(
                f'{EEG_CHANNEL_NAMES[1]} (Ohm): {data[1]:.0f}')
            if len(RESISTANCE_CHANNELS) > 2:
                self.ui.LabelCh2.setText(
                    f'{EEG_CHANNEL_NAMES[2]} (Ohm): {data[2]:.0f}')
                self.ui.LabelCh3.setText(
                    f'{EEG_CHANNEL_NAMES[3]} (Ohm): {data[3]:.0f}')

    def connect_toBB(self):
        params = BrainFlowInputParams()
        self.board = BoardShim(BOARD_ID, params)
        self.board.prepare_session()

    def result_connect_toBB(self):
        self.ui.ButtonStart.setEnabled(True)
        self.ui.ButtonDisconnect.setEnabled(True)
        self.ui.ButtonImpedanceStart.setEnabled(True)

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
        self.ui.ButtonImpedanceStart.setEnabled(False)

        # CHART buffer renew
        self.chart_buffers = []
        for i in range(NUM_CHANNELS):
            self.chart_buffers.append([
                QPointF(x, 0) for x in range(self.chart_duration * SAMPLE_RATE)
            ])

        self.board.start_stream(450000)
        self.board.config_board ('CommandStartSignal')

        # Start timer for chart redraw
        self.chart_redraw_timer = QTimer()
        self.chart_redraw_timer.timeout.connect(self.redraw_charts)
        self.chart_redraw_timer.start(UPDATE_CHART_SPEED_MS)

    def _stop_capture(self):
        self.chart_redraw_timer.stop()

        self.board.stop_stream()

        self.ui.ButtonStart.setEnabled(True)
        self.ui.ButtonDisconnect.setEnabled(True)
        self.ui.ButtonStop.setEnabled(False)
        self.ui.ButtonImpedanceStart.setEnabled(True)

    def _disconnect(self):
        # Release all BB resources
        if self.board.is_prepared():
            self.board.release_session()

        self.ui.ButtonDisconnect.setEnabled(False)
        self.ui.ButtonConnect.setEnabled(True)
        self.ui.ButtonStart.setEnabled(False)

    def _start_impedance(self):
        self.board.start_stream(450000)
        self.board.config_board('CommandStartResist')

        # Start timer for impedance renew
        self.impedance_update_timer = QTimer()
        self.impedance_update_timer.timeout.connect(self.impedance_update)
        self.impedance_update_timer.start(UPDATE_IMPEDANCE_SPEED_MS)

        self.ui.ButtonImpedanceStart.setEnabled(False)
        self.ui.ButtonImpedanceStop.setEnabled(True)
        self.ui.ButtonStart.setEnabled(False)
        self.ui.ButtonDisconnect.setEnabled(False)

    def _stop_impedance(self):
        self.board.config_board('CommandStopResist')
        self.board.stop_stream()
        self.impedance_update_timer.stop()

        self.ui.ButtonImpedanceStart.setEnabled(True)
        self.ui.ButtonImpedanceStop.setEnabled(False)
        self.ui.ButtonStart.setEnabled(True)
        self.ui.ButtonDisconnect.setEnabled(True)

    def close(self):
        # Release all BB resources
        if self.board.is_prepared():
            self.board.release_session()
        print("Close")




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
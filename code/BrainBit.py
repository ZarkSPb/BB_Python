import signal
import sys
import traceback

import numpy as np
from brainflow.board_shim import BoardIds, BoardShim
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import (QObject, QPointF, QRunnable, QThreadPool, Signal,
                            Slot)
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QMainWindow

from eeg import Eeg
from ui_mainwindow import Ui_MainWindow

# configuring BB
BOARD_ID = BoardIds.SYNTHETIC_BOARD.value
# BOARD_ID = BoardIds.BRAINBIT_BOARD.value
SAMPLE_RATE = BoardShim.get_sampling_rate(BOARD_ID)  # 250
EXG_CHANNELS = BoardShim.get_exg_channels(BOARD_ID)
NUM_CHANNELS = len(EXG_CHANNELS)
SIGNAL_DURATION = 5  # seconds

if BOARD_ID == BoardIds.SYNTHETIC_BOARD.value:
    NUM_CHANNELS = 4


class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(np.ndarray)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()  #QtCore.Slot
    def run(self):
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            extype, value = sys.exc_info()[:2]
            self.signals.error.emit((extype, value, traceback.format_exc()))
        else:
            # Return the result of the processing
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()  # Done


def get_fft(signal):
    amps = np.absolute(np.fft.rfft(signal))
    return amps / signal.shape[0]


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.threadpool = QThreadPool()

        self.charts = []

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ----------BUTTON CONNECT----------
        self.ui.ButtonConnect.clicked.connect(self._connect)
        self.ui.ButtonStart.clicked.connect(self._start_capture)
        self.ui.ButtonStop.clicked.connect(self._stop_capture)
        self.ui.ButtonDisconnect.clicked.connect(self._disconnect)
        # ----------BUTTON CONNECT----------

        # ----------CHART MAKE----------
        self.channel_names = BoardShim.get_board_descr(
            BOARD_ID)['eeg_names'].split(',')

        self.serieses = []
        self.chart_buffers = []
        for channel_name in self.channel_names[:NUM_CHANNELS]:
            chart_view = QChartView(self.create_line_chart(channel_name))
            # chart_view.setRenderHint(QPainter.Antialiasing, True)
            self.ui.verticalLayout_3.addWidget(chart_view)
            self.charts.append(chart_view)
        # ----------CHART MAKE----------

        self.ui.SliderDuration.setMaximum(SIGNAL_DURATION)
        self.ui.SliderDuration.setValue(SIGNAL_DURATION)
        self.ui.SliderDuration.setSliderPosition(SIGNAL_DURATION)

        self.update()

    # ----------UPDATE UI----------
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

    # ----------UPDATE UI----------

    def create_line_chart(self, chartname):
        chart = QChart()
        chart.setTitle(chartname)
        chart.legend().hide()

        series = QLineSeries()
        self.serieses.append(series)
        chart.addSeries(self.serieses[-1])

        axis_x = QValueAxis()
        axis_x.setRange(0, SAMPLE_RATE)
        axis_y = QValueAxis()
        axis_y.setRange(-50, 50)
        chart.setAxisX(axis_x, self.serieses[-1])
        chart.setAxisY(axis_y, self.serieses[-1])

        self.chart_buffers.append(
            [QPointF(x, 0) for x in range(SAMPLE_RATE * SIGNAL_DURATION)])

        self.serieses[-1].append(self.chart_buffers[-1])

        return chart

    def capture_execute(self, progress_callback):

        self.ui.ButtonStop.setEnabled(True)

        self.signal = signal.Buffer(SAMPLE_RATE, SIGNAL_DURATION, NUM_CHANNELS)
        self.eeg.work = True
        self.eeg.capture(progress_callback)

    def redraw_charts(self, n):
        # print(n[:NUM_CHANNELS, 0])
        self.signal.add(n)

        for channel_num in range(NUM_CHANNELS):
            data = self.signal.get_buff()[:, channel_num]
            for s, value in enumerate(data[-self.chart_duration *
                                           SAMPLE_RATE:]):
                self.chart_buffers[channel_num][s].setY(value)
            self.serieses[channel_num].replace(self.chart_buffers[channel_num])

    def thread_complite(self):
        pass

    def connect_toBB(self, progress_callback):
        self.eeg = Eeg(BOARD_ID, NUM_CHANNELS)

    def result_connect_toBB(self):
        self.ui.ButtonStart.setEnabled(True)
        self.ui.ButtonDisconnect.setEnabled(True)

    # ----------BUTTONS----------
    def _connect(self):
        self.ui.ButtonConnect.setEnabled(False)

        worker = Worker(self.connect_toBB)
        worker.signals.result.connect(self.result_connect_toBB)
        self.threadpool.start(worker)

    def _start_capture(self):
        self.ui.ButtonStart.setEnabled(False)
        self.ui.ButtonDisconnect.setEnabled(False)

        worker = Worker(self.capture_execute)
        worker.signals.progress.connect(self.redraw_charts)
        worker.signals.result.connect(self.thread_complite)

        # Execute
        self.threadpool.start(worker)

    def _stop_capture(self):
        self.eeg.work = False
        self.eeg.stop_stream()

        self.ui.ButtonStart.setEnabled(True)
        self.ui.ButtonDisconnect.setEnabled(True)
        self.ui.ButtonStop.setEnabled(False)

    def _disconnect(self):
        self.eeg.release_session()
        self.ui.ButtonDisconnect.setEnabled(False)
        self.ui.ButtonConnect.setEnabled(True)
        self.ui.ButtonStart.setEnabled(False)

    # -------BUTTONS----------


def main():
    print('\n\n\n')

    # Create the Qt application
    app = QApplication(sys.argv)
    # Create window
    window = MainWindow()
    window.show()

    # Run the main Qt loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

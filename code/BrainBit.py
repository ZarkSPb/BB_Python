import sys
import traceback
from time import sleep

import numpy as np
from brainflow.board_shim import BoardIds
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
SAMPLE_RATE = 250
AVERAGE_LENGTH = 7 * SAMPLE_RATE


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

        # self.ui.statusbar.tex

        # ----------CHART MAKE----------
        chart_view = QChartView(self.create_line_chart("Line chart 1"))
        self.ui.gridLayout.addWidget(chart_view, 0, 1)
        self.charts.append(chart_view)

        chart_view = QChartView(self.create_line_chart("Line chart 2"))
        chart_view.setRenderHint(QPainter.Antialiasing, True)
        self.ui.gridLayout.addWidget(chart_view, 1, 1)
        self.charts.append(chart_view)

    def create_line_chart(self, chartname):
        chart = QChart()
        self._series = QLineSeries()
        chart.addSeries(self._series)
        chart.setTitle(chartname)
        chart.legend().hide()
        axis_x = QValueAxis()
        axis_x.setRange(0, SAMPLE_RATE)
        axis_y = QValueAxis()
        axis_y.setRange(-200, 200)
        chart.setAxisX(axis_x, self._series)
        chart.setAxisY(axis_y, self._series)

        self._buffer = [QPointF(x, 0) for x in range(SAMPLE_RATE)]
        self._series.append(self._buffer)

        return chart

    def capture_execute(self, progress_callback):
        self.eeg.start_stream()
        self.eeg.buffer_fill(progress_callback)
        self.ui.ButtonStop.setEnabled(True)
        self.eeg.work = True
        self.eeg.capture(progress_callback)

    def progress_fn(self, n):
        data = n[:, 10]
        for s, value in enumerate(data):
            self._buffer[s].setY(value)
        self._series.replace(self._buffer)

    def thread_complite(self):
        pass

    def connect_toBB(self, progress_callback):
        self.eeg = Eeg(BOARD_ID)

    def result_connect_toBB(self):
        self.ui.ButtonStart.setEnabled(True)
        self.ui.ButtonDisconnect.setEnabled(True)

    # -------BUTTONS-------
    def _connect(self):
        self.ui.ButtonConnect.setEnabled(False)
        self.ui.ButtonDisconnect.setEnabled(True)

        worker = Worker(self.connect_toBB)
        worker.signals.result.connect(self.result_connect_toBB)
        self.threadpool.start(worker)

    def _start_capture(self):
        self.ui.ButtonStart.setEnabled(False)
        self.ui.ButtonDisconnect.setEnabled(False)

        worker = Worker(self.capture_execute)
        worker.signals.progress.connect(self.progress_fn)
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


def main():
    print('\n\n\n')

    # Create the Qt application
    app = QApplication(sys.argv)
    # Create window
    window = MainWindow()
    window.show()

    # Run the main Qt loop
    # app.exec()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
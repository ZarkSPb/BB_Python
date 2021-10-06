import sys
from time import sleep
import threading

import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, LogLevels
import matplotlib.pyplot as plt

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCharts import QChartView, QChart, QLineSeries, QValueAxis
from PySide6.QtCore import QPointF

from ui_mainwindow import Ui_MainWindow

# configuring BB
BOARD_ID = BoardIds.SYNTHETIC_BOARD.value
# BOARD_ID = BoardIds.BRAINBIT_BOARD.value
SAMPLE_RATE = 250
AVERAGE_LENGTH = 7 * SAMPLE_RATE


def get_fft(signal):
    amps = np.absolute(np.fft.rfft(signal))
    return amps / signal.shape[0]


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.charts = []

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.ButtonConnect.clicked.connect(self.connect)
        self.ui.ButtonStart.clicked.connect(self.start_capture)
        self.ui.ButtonStop.clicked.connect(self.stop_capture)

        chart_view = QChartView(self.create_line_chart("Line chart 1"))
        self.ui.gridLayout.addWidget(chart_view, 0, 1)
        self.charts.append(chart_view)

        chart_view = QChartView(self.create_line_chart("Line chart 2"))
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
        # axis_x.setTitleVisible(False)
        axis_y = QValueAxis()
        axis_y.setRange(-200, 200)
        chart.setAxisX(axis_x, self._series)
        chart.setAxisY(axis_y, self._series)

        self._buffer = [QPointF(x, 0) for x in range(SAMPLE_RATE)]
        self._series.append(self._buffer)

        return chart

    def connect(self):
        BoardShim.enable_dev_board_logger()
        params = BrainFlowInputParams()

        try:
            self.board_shim = BoardShim(BOARD_ID, params)
            self.board_shim.prepare_session()
            # self.board_shim.start_stream(45000)
        finally:
            # энаблим кнопку старт
            self.ui.ButtonStart.setEnabled(True)
            self.ui.ButtonConnect.setEnabled(False)

    def start_capture(self):
        try:
            self.board_shim.start_stream(45000)
            eeg = Eeg(self.board_shim)

            data = eeg.buff[:, 10]
            for s, value in enumerate(data):
                self._buffer[s].setY(value)
            self._series.replace(self._buffer)

            eeg.capture()

        finally:
            if self.board_shim.is_prepared():
                self.board_shim.release_session()

    def stop_capture(self):
        print("STOP")


class Eeg:
    def __init__(self, board_shim):
        self.board_id = board_shim.get_board_id()
        self.board_shim = board_shim
        self.num_channel = BoardShim.get_package_num_channel(self.board_id)
        self.exg_channels = BoardShim.get_exg_channels(self.board_id)

        # create buffer
        BUFFER_SIZE = SAMPLE_RATE
        self.buff = np.zeros((BUFFER_SIZE, len(self.exg_channels)))

        # print(f'{BoardShim.get_board_descr(self.board_id)}\n')
        # print(f'num channel = {self.num_channel}')
        # print(self.exg_channels, end='\n\n')

        # Filling the buffer
        self.buffer_fill()

    def buffer_fill(self):
        i = 0
        while i < SAMPLE_RATE:
            data = self.board_shim.get_board_data(1)
            if np.any(data):
                # current_num = data[self.num_channel]
                self.current_exg = data[self.exg_channels]
                self.buff[i, :] = self.current_exg[:, 0]
                i += 1
                print(i)

    def capture(self):
        i = 0
        while i < 500:
            data = self.board_shim.get_board_data(1)
            if np.any(data):
                self.current_exg = data[self.exg_channels]
                self.buff = np.roll(self.buff, -1, axis=0)
                self.buff[-1] = self.current_exg[:, 0]
                i += 1
                print(i)


def main():
    print('\n\n\n')

    # Create the Qt application
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    # Run the main Qt loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
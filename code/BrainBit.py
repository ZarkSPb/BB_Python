import sys
from time import sleep
import threading

import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, LogLevels
import matplotlib.pyplot as plt

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCharts import QChartView, QChart, QLineSeries, QValueAxis

from ui_mainwindow import Ui_MainWindow

# configuring BB
BOARD_ID = BoardIds.SYNTHETIC_BOARD.value
# BOARD_ID = BoardIds.BRAINBIT_BOARD.value
SAMPLERATE = 250
AVERAGE_LENGTH = 7 * SAMPLERATE


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

        # self._series = QLineSeries()
        chart_view = QChartView(self.create_line_chart("Line chart 1"))
        self.ui.gridLayout.addWidget(chart_view, 0, 1)
        self.charts.append(chart_view)

        chart_view = QChartView(self.create_line_chart("Line chart 2"))
        self.ui.gridLayout.addWidget(chart_view, 1, 1)
        self.charts.append(chart_view)

        chart_view = QChartView(self.create_line_chart("Line chart 3"))
        self.ui.gridLayout.addWidget(chart_view, 2, 1)
        self.charts.append(chart_view)

    def create_line_chart(self, chartname):
        chart = QChart()
        chart.setTitle(chartname)
        axis_x = QValueAxis()
        axis_x.setRange(0, SAMPLERATE)
        axis_y = QValueAxis()
        axis_y.setRange(-100, 100)
        chart.setAxisX(axis_x)
        chart.setAxisY(axis_y)

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
        BoardShim.enable_dev_board_logger()
        params = BrainFlowInputParams()

        try:
            # board_shim = BoardShim(BOARD_ID, params)
            # self.board_shim.prepare_session()
            self.board_shim.start_stream(45000)
            eeg = Eeg(self.board_shim)
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

        # print(f'{BoardShim.get_board_descr(self.board_id)}\n')
        # print(f'num channel = {self.num_channel}')
        # print(self.exg_channels, end='\n\n')

        self.capture()

    def capture(self):
        BUFFER_SIZE = SAMPLERATE
        self.buff = np.zeros((BUFFER_SIZE, len(self.exg_channels)))

        # Filling the buffer
        t_thread = threading.Thread(target=self._buffer_fill)
        t_thread.daemon = True
        t_thread.start()

        # Waiting for filling SAMPLERATE count
        while t_thread.is_alive():
            sleep(0.002)

        # make and start main thread
        t_thread = threading.Thread(target=self._capture)
        t_thread.daemon = True
        t_thread.start()

        # # !!! Включить интерактивный режим для анимации
        # plt.ion()
        # # Создание окна и осей для графика
        # fig, ax = plt.subplots()
        # # Отобразить график фукнции в начальный момент времени
        # buff_spectrum = get_fft(self.buff[:, 9])
        # self.line, = ax.plot(buff_spectrum[:41])

        while t_thread.is_alive():
            # plotting data
            # self.plotting()
            sleep(0.1)

        # # Отключить интерактивный режим по завершению анимации
        # plt.ioff()
        # # Нужно, чтобы график не закрывался после завершения анимации
        # plt.show()

    def plotting(self):
        buff_spectrum = get_fft(self.buff[:, 9])
        self.line.set_ydata(buff_spectrum[:41])
        # !!! Следующие два вызова требуются для обновления графика
        plt.draw()
        plt.gcf().canvas.flush_events()

    def _buffer_fill(self):
        i = 0
        while i < SAMPLERATE:
            data = self.board_shim.get_board_data(1)
            if np.any(data):
                # current_num = data[self.num_channel]
                self.current_exg = data[self.exg_channels]
                self.buff[i, :] = self.current_exg[:, 0]
                i += 1
                print(i)

    def _capture(self):
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
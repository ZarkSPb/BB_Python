# import numpy as np

# x = np.arange(9)

# print(x)

# # x[:-1] = x[1:]
# # x[-1] = 9

# x = np.roll(x, -1)
# x[-1] = 9

# print(x)

# x = np.array([[],[]])
# print(x.shape)

# import time

# import matplotlib.pyplot as plt
# import numpy

# def gaussian(x, delay, sigma):
#     '''
#     Функция, график которой будет отображаться процессе анимации
#     '''
#     return numpy.exp(-((x - delay) / sigma) ** 2)

# if __name__ == '__main__':
#     # Параметры отображаемой функции
#     maxSize = 200
#     sigma = 10.0

#     # Диапазон точек для расчета графика функции
#     x = numpy.arange(maxSize)

#     # Значения графика функции
#     y = numpy.zeros(maxSize)

#     # !!! Включить интерактивный режим для анимации
#     plt.ion()

#     # У функции gaussian будет меняться параметр delay (задержка)
#     for delay in numpy.arange(-50.0, 200.0, 1.0):
#         y = gaussian(x, delay, sigma)

#         # !!! Очистить текущую фигуру
#         plt.clf()

#         # Отобразить график
#         plt.plot(x, y)

#         # Установка отображаемых интервалов по осям
#         plt.xlim(0, maxSize)
#         plt.ylim(-1.1, 1.1)

#         # !!! Следующие два вызова требуются для обновления графика
#         plt.draw()
#         plt.gcf().canvas.flush_events()

#         # Задержка перед следующим обновлением
#         time.sleep(0.005)

#     # Отключить интерактивный режим по завершению анимации
#     plt.ioff()

#     # Нужно, чтобы график не закрывался после завершения анимации
#     plt.show()

# import time

# import matplotlib.pyplot as plt
# import numpy

# def gaussian(x, delay, sigma):
#     '''
#     Функция, график которой будет отображаться процессе анимации
#     '''
#     return numpy.exp(-((x - delay) / sigma) ** 2)

# if __name__ == '__main__':
#     # Параметры отображаемой функции
#     maxSize = 200
#     sigma = 10.0

#     # Диапазон точек для расчета графика функции
#     x = numpy.arange(maxSize)

#     # Значения графика функции
#     y = numpy.zeros(maxSize)

#     # !!! Включить интерактивный режим для анимации
#     plt.ion()

#     # Создание окна и осей для графика
#     fig, ax = plt.subplots()

#     # Установка отображаемых интервалов по осям
#     ax.set_xlim(0, maxSize)
#     ax.set_ylim(-1.1, 1.1)

#     # Отобразить график фукнции в начальный момент времени
#     line, = ax.plot(x, y)

#     # У функции gaussian будет меняться параметр delay (задержка)
#     for delay in numpy.arange(-50.0, 200.0, 1.0):
#         y = gaussian(x, delay, sigma)

#         # Обновить данные на графике
#         line.set_ydata(y)

#         # Отобразить новые данный
#         fig.canvas.draw()
#         fig.canvas.flush_events()

#         # Задержка перед следующим обновлением
#         time.sleep(0.001)

#     # Отключить интерактивный режим по завершению анимации
#     plt.ioff()
#     plt.show()

# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# import numpy


# def gaussian(x, delay, sigma):
#     '''
#     Функция, график которой будет отображаться процессе анимации.
#     '''
#     return numpy.exp(-((x - delay) / sigma)**2)


# # Функция, вызываемая для каждого кадра
# def main_func(frame, line, x, sigma):
#     '''
#     frame - параметр, который изменяется от кадра к кадру.
#     line - кривая, для которой изменяются данные.
#     x - список точек по оси X, для которых рассчитывается функция Гаусса.
#     sigma - отвечает за ширину функции Гаусса.
#     '''
#     y = gaussian(x, frame, sigma)
#     line.set_ydata(y)
#     return [line]


# if __name__ == '__main__':
#     # Параметры отображаемой функции
#     maxSize = 200
#     sigma = 10.0

#     # Диапазон точек для расчета графика функции
#     x = numpy.arange(maxSize)

#     # Значения графика функции
#     y = numpy.zeros(maxSize)

#     # Создание окна для графика
#     fig, ax = plt.subplots()

#     # Установка отображаемых интервалов по осям
#     ax.set_xlim(0, maxSize)
#     ax.set_ylim(-1.1, 1.1)

#     # Создание линии, которую будем анимировать
#     line, = ax.plot(x, y)

#     # !!! Параметр, который будет меняться от кадра к кадру
#     frames = numpy.arange(-50.0, 200.0, 1.0)

#     # !!! Задержка между кадрами в мс
#     interval = 30

#     # !!! Использовать ли буферизацию для устранения мерцания
#     blit = True

#     # !!! Будет ли анимация циклической
#     repeat = False

#     # !!! Создание анимации
#     animation = FuncAnimation(fig,
#                               func=main_func,
#                               frames=frames,
#                               fargs=(line, x, sigma),
#                               interval=interval,
#                               blit=blit,
#                               repeat=repeat)
#     plt.show()



import sys
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import QPointF, Slot
from PySide6.QtMultimedia import (QAudioDevice, QAudioFormat,
        QAudioSource, QMediaDevices)
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox


SAMPLE_COUNT = 2000


RESOLUTION = 4


class MainWindow(QMainWindow):
    def __init__(self, device):
        super().__init__()

        self._series = QLineSeries()
        self._chart = QChart()
        self._chart.addSeries(self._series)
        self._axis_x = QValueAxis()
        self._axis_x.setRange(0, SAMPLE_COUNT)
        self._axis_x.setLabelFormat("%g")
        self._axis_x.setTitleText("Samples")
        self._axis_y = QValueAxis()
        self._axis_y.setRange(-1, 1)
        self._axis_y.setTitleText("Audio level")
        self._chart.setAxisX(self._axis_x, self._series)
        self._chart.setAxisY(self._axis_y, self._series)
        self._chart.legend().hide()
        name = device.description()
        self._chart.setTitle(f"Data from the microphone ({name})")

        format_audio = QAudioFormat()
        format_audio.setSampleRate(8000)
        format_audio.setChannelCount(1)
        format_audio.setSampleFormat(QAudioFormat.UInt8)

        self._audio_input = QAudioSource(device, format_audio, self)
        self._io_device = self._audio_input.start()
        self._io_device.readyRead.connect(self._readyRead)

        self._chart_view = QChartView(self._chart)
        self.setCentralWidget(self._chart_view)

        self._buffer = [QPointF(x, 0) for x in range(SAMPLE_COUNT)]
        self._series.append(self._buffer)

    def closeEvent(self, event):
        if self._audio_input is not None:
            self._audio_input.stop()
        event.accept()

    @Slot()
    def _readyRead(self):
        data = self._io_device.readAll()
        available_samples = data.size() // RESOLUTION
        start = 0
        if (available_samples < SAMPLE_COUNT):
            start = SAMPLE_COUNT - available_samples
            for s in range(start):
                self._buffer[s].setY(self._buffer[s + available_samples].y())

        data_index = 0
        for s in range(start, SAMPLE_COUNT):
            value = (ord(data[data_index]) - 128) / 128
            self._buffer[s].setY(value)
            data_index = data_index + RESOLUTION
        self._series.replace(self._buffer)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    input_devices = QMediaDevices.audioInputs()
    if not input_devices:
        QMessageBox.warning(None, "audio", "There is no audio input device available.")
        sys.exit(-1)
    main_win = MainWindow(input_devices[0])
    main_win.setWindowTitle("audio")
    available_geometry = main_win.screen().availableGeometry()
    size = available_geometry.height() * 3 / 4
    main_win.resize(size, size)
    main_win.show()
    sys.exit(app.exec())
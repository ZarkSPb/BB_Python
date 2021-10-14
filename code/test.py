# from brainflow.board_shim import BoardIds, BoardShim, BrainFlowInputParams
# from PySide6.QtCore import QTimer
# from PySide6 import QtGui

# BOARD_ID = BoardIds.SYNTHETIC_BOARD.value
# # BOARD_ID = BoardIds.BRAINBIT_BOARD.value

# class Gr:
#     def __init__(self, board):
#         self.board = board

#         self.app = QtGui.QGuiApplication([])
#         self.app.setQuitOnLastWindowClosed(False)

#         timer = QTimer()
#         timer.timeout.connect(self.update)
#         timer.start(20)

#         self.i = 0

#         self.app.exec()

#     def update(self):
#         while self.i < 3000:
#             data = self.board.get_board_data_count()
#             print(self.i, data)
#             self.i += 1

# def main():
#     BoardShim.enable_dev_board_logger()
#     params = BrainFlowInputParams()
#     try:
#         board = BoardShim(BOARD_ID, params)
#         board.prepare_session()
#         board.start_stream(450000)

#         g = Gr(board)

#     finally:
#         if board.is_prepared():
#             board.release_session()

# if __name__ == "__main__":
#     main()

# i = 0
# while i < 10:
#     data = board.get_current_board_data(2)
#     if np.any(data):
#         i += 1
#         # print(i, j, data, "\n\n")
#         # data = np.array([[]])
#         print(i, data)
#         print('---------', j)
#         j = 0
#     j += 1

# import sys

# from PySide6.QtCore import QTimer
# from PySide6.QtGui import QGuiApplication

# app = QGuiApplication(sys.argv)
# app.setQuitOnLastWindowClosed(False)

# def tick():
#     print('tick')

# timer = QTimer()
# timer.timeout.connect(tick)
# timer.start(1000)

# # run event loop so python doesn't exit
# app.exec()

# from brainflow.board_shim import BoardIds, BoardShim, BrainFlowInputParams
# from time import sleep

# # BOARD_ID = BoardIds.SYNTHETIC_BOARD.value
# BOARD_ID = BoardIds.BRAINBIT_BOARD.value

# BoardShim.enable_dev_board_logger()
# params = BrainFlowInputParams()
# board = BoardShim(BOARD_ID, params)
# board.prepare_session()
# board.start_stream(450000)
# sleep(10)

# num_samples = board.get_board_data_count()
# data = board.get_current_board_data(450000)
# print(
#     f"\n\nData shape: {data.shape}, Num of elements in ringbuffer: {num_samples}\n\n"
# )

# board.stop_stream()

# board.start_stream(450000)

# num_samples = board.get_board_data_count()
# data = board.get_current_board_data(450000)
# print(
#     f"\n\nData shape: {data.shape}, Num of elements in ringbuffer: {num_samples}\n\n"
# )

# board.stop_stream()

# if board.is_prepared():
#     board.release_session()




# numvar = 56.255656596595959

# st = f"{numvar:.0f}"

# print(st)


# import sys
# from PySide6.QtCore import *
# from PySide6.QtGui import *
 
# class SubWindow(object):
#     def __init__(self, parent = None):
#         super(SubWindow, self).__init__(parent)

 
#     def closeEvent(self, event):
#         self.deleteLater()
#         event.accept()
 
# class MainWindow(object):
#     def __init__(self, parent = None):
#         super(MainWindow, self).__init__(parent)
 
#     def openSub(self):
#         self.sub = SubWindow()
#         self.sub.show()
 
#     def closeEvent(self, event):
#         widgetList = QGuiApplication.topLevelWidgets()
#         numWindows = len(widgetList)
#         if numWindows > 1:
#             event.ignore()
#         else:
#             event.accept()
 
# app = QGuiApplication(sys.argv)
# mainWin =MainWindow()
# mainWin.show()
# sys.exit(app.exec())

# from datetime import datetime

# t = datetime.now()

# print(t.strftime("%Y-%m-%d_%H-%M-%S"))


# import sys
# from random import randrange

# from PySide6.QtCore import QAbstractTableModel, QModelIndex, QRect, Qt
# from PySide6.QtGui import QColor, QPainter
# from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView,
#     QTableView, QWidget)
# from PySide6.QtCharts import QChart, QChartView, QLineSeries, QVXYModelMapper


# class CustomTableModel(QAbstractTableModel):
#     def __init__(self):
#         super().__init__()
#         self.input_data = []
#         self.mapping = {}
#         self.column_count = 4
#         self.row_count = 15

#         for i in range(self.row_count):
#             data_vec = [0] * self.column_count
#             for k in range(len(data_vec)):
#                 if k % 2 == 0:
#                     data_vec[k] = i * 50 + randrange(30)
#                 else:
#                     data_vec[k] = randrange(100)
#             self.input_data.append(data_vec)

#     def rowCount(self, parent=QModelIndex()):
#         return len(self.input_data)

#     def columnCount(self, parent=QModelIndex()):
#         return self.column_count

#     def headerData(self, section, orientation, role):
#         if role != Qt.DisplayRole:
#             return None

#         if orientation == Qt.Horizontal:
#             if section % 2 == 0:
#                 return "x"
#             else:
#                 return "y"
#         else:
#             return str(section + 1)

#     def data(self, index, role=Qt.DisplayRole):
#         if role == Qt.DisplayRole:
#             return self.input_data[index.row()][index.column()]
#         elif role == Qt.EditRole:
#             return self.input_data[index.row()][index.column()]
#         elif role == Qt.BackgroundRole:
#             for color, rect in self.mapping.items():
#                 if rect.contains(index.column(), index.row()):
#                     return QColor(color)
#             # cell not mapped return white color
#             return QColor(Qt.white)
#         return None

#     def setData(self, index, value, role=Qt.EditRole):
#         if index.isValid() and role == Qt.EditRole:
#             self.input_data[index.row()][index.column()] = float(value)
#             self.dataChanged.emit(index, index)
#             return True
#         return False

#     def flags(self, index):
#         return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

#     def add_mapping(self, color, area):
#         self.mapping[color] = area

#     def clear_mapping(self):
#         self.mapping = {}


# class TableWidget(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.model = CustomTableModel()

#         self.table_view = QTableView()
#         self.table_view.setModel(self.model)
#         self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#         self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

#         self.chart = QChart()
#         self.chart.setAnimationOptions(QChart.AllAnimations)

#         self.series = QLineSeries()
#         self.series.setName("Line 1")
#         self.mapper = QVXYModelMapper(self)
#         self.mapper.setXColumn(0)
#         self.mapper.setYColumn(1)
#         self.mapper.setSeries(self.series)
#         self.mapper.setModel(self.model)
#         self.chart.addSeries(self.series)

#         # for storing color hex from the series
#         seriesColorHex = "#000000"

#         # get the color of the series and use it for showing the mapped area
#         self.model.add_mapping(self.series.pen().color().name(),
#                                QRect(0, 0, 2, self.model.rowCount()))

#         # series 2
#         self.series = QLineSeries()
#         self.series.setName("Line 2")

#         self.mapper = QVXYModelMapper(self)
#         self.mapper.setXColumn(2)
#         self.mapper.setYColumn(3)
#         self.mapper.setSeries(self.series)
#         self.mapper.setModel(self.model)
#         self.chart.addSeries(self.series)

#         # get the color of the series and use it for showing the mapped area
#         self.model.add_mapping(self.series.pen().color().name(),
#                                QRect(2, 0, 2, self.model.rowCount()))

#         self.chart.createDefaultAxes()
#         self.chart_view = QChartView(self.chart)
#         self.chart_view.setRenderHint(QPainter.Antialiasing)
#         self.chart_view.setMinimumSize(640, 480)

#         # create main layout
#         self.main_layout = QGridLayout()
#         self.main_layout.addWidget(self.table_view, 1, 0)
#         self.main_layout.addWidget(self.chart_view, 1, 1)
#         self.main_layout.setColumnStretch(1, 1)
#         self.main_layout.setColumnStretch(0, 0)
#         self.setLayout(self.main_layout)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     w = TableWidget()
#     w.show()
#     sys.exit(app.exec())





# import sys
# from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
# from PySide6.QtCore import QPointF, Slot
# from PySide6.QtMultimedia import (QAudioDevice, QAudioFormat,
#         QAudioSource, QMediaDevices)
# from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox


# SAMPLE_COUNT = 2000


# RESOLUTION = 4


# class MainWindow(QMainWindow):
#     def __init__(self, device):
#         super().__init__()

#         self._series = QLineSeries()
#         self._chart = QChart()
#         self._chart.addSeries(self._series)
#         self._axis_x = QValueAxis()
#         self._axis_x.setRange(0, SAMPLE_COUNT)
#         self._axis_x.setLabelFormat("%g")
#         self._axis_x.setTitleText("Samples")
#         self._axis_y = QValueAxis()
#         self._axis_y.setRange(-1, 1)
#         self._axis_y.setTitleText("Audio level")
#         self._chart.setAxisX(self._axis_x, self._series)
#         self._chart.setAxisY(self._axis_y, self._series)
#         self._chart.legend().hide()
#         name = device.description()
#         self._chart.setTitle(f"Data from the microphone ({name})")

#         format_audio = QAudioFormat()
#         format_audio.setSampleRate(8000)
#         format_audio.setChannelCount(1)
#         format_audio.setSampleFormat(QAudioFormat.UInt8)

#         self._audio_input = QAudioSource(device, format_audio, self)
#         self._io_device = self._audio_input.start()
#         self._io_device.readyRead.connect(self._readyRead)

#         self._chart_view = QChartView(self._chart)
#         self.setCentralWidget(self._chart_view)

#         self._buffer = [QPointF(x, 0) for x in range(SAMPLE_COUNT)]
#         self._series.append(self._buffer)

#     def closeEvent(self, event):
#         if self._audio_input is not None:
#             self._audio_input.stop()
#         event.accept()

#     @Slot()
#     def _readyRead(self):
#         data = self._io_device.readAll()
#         available_samples = data.size() // RESOLUTION
#         start = 0
#         if (available_samples < SAMPLE_COUNT):
#             start = SAMPLE_COUNT - available_samples
#             for s in range(start):
#                 self._buffer[s].setY(self._buffer[s + available_samples].y())

#         data_index = 0
#         for s in range(start, SAMPLE_COUNT):
#             value = (ord(data[data_index]) - 128) / 128
#             self._buffer[s].setY(value)
#             data_index = data_index + RESOLUTION
#         self._series.replace(self._buffer)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)

#     input_devices = QMediaDevices.audioInputs()
#     if not input_devices:
#         QMessageBox.warning(None, "audio", "There is no audio input device available.")
#         sys.exit(-1)
#     main_win = MainWindow(input_devices[0])
#     main_win.setWindowTitle("audio")
#     available_geometry = main_win.screen().availableGeometry()
#     size = available_geometry.height() * 3 / 4
#     main_win.resize(size, size)
#     main_win.show()
#     sys.exit(app.exec())


# print(list(range(2, 0, -1)))

print('1'*5)
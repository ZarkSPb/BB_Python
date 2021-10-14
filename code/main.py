import enum
import sys
import PySide6
from PySide6 import QtCore

import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from PySide6 import QtWidgets
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QCategoryAxis
from PySide6.QtCore import QPointF, QThreadPool, QTimer
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QMainWindow

from buff import Buffer
from patient import Patient
from session import Session
from settings import *
from ui_mainwindow import Ui_MainWindow
from utils import file_name_constructor, save_file, signal_filtering
from worker import Worker

np.set_printoptions(precision=1, suppress=True)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.threadpool = QThreadPool()

        self.charts = []

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # --------------------Impedance label fill--------------------
        self.ui.LabelCh0.setText(EEG_CHANNEL_NAMES[0])
        self.ui.LabelCh1.setText(EEG_CHANNEL_NAMES[1])
        self.ui.LabelCh2.setText(EEG_CHANNEL_NAMES[2])
        self.ui.LabelCh3.setText(EEG_CHANNEL_NAMES[3])

        # --------------------CHART MAKE--------------------
        self.channel_names = BoardShim.get_board_descr(
            BOARD_ID)['eeg_names'].split(',')

        # serieses fill
        self.serieses = []
        self.chart_buffers = []

        chart = QChart()
        chart.legend().hide()

        axis_x = QValueAxis()
        axis_x.setRange(0, MAX_CHART_SIGNAL_DURATION)
        axis_x.setTickCount(MAX_CHART_SIGNAL_DURATION + 1)
        axis_x.setMinorTickCount(1)
        axis_x.setLabelFormat('%i')

        axis_y = QValueAxis()
        axis_y.setRange(0, 400)
        axis_y.setTickCount(9)
        axis_y.setMinorTickCount(1)
        axis_y.setLabelsVisible(False)

        axis_c = QCategoryAxis()
        axis_c.setRange(0, 4)
        # axis_c.setGridLineColor('black')
        self.channel_names[NUM_CHANNELS - 1::-1]
        for i, ch_name in enumerate(self.channel_names[NUM_CHANNELS - 1::-1]):
            axis_c.append(ch_name, i + 1)

        chart.addAxis(axis_x, QtCore.Qt.AlignBottom)
        chart.addAxis(axis_y, QtCore.Qt.AlignRight)
        chart.addAxis(axis_c, QtCore.Qt.AlignLeft)

        for i in range(NUM_CHANNELS):
            series = QLineSeries()
            # series.setColor('#209fdf')
            self.chart_buffers.append([
                QPointF(x / SAMPLE_RATE, 20 + (NUM_CHANNELS - 1 - i) * 40)
                for x in range(MAX_CHART_SIGNAL_DURATION * SAMPLE_RATE)
            ])
            series.append(self.chart_buffers[-1])
            self.serieses.append(series)
            chart.addSeries(self.serieses[-1])
            self.serieses[-1].attachAxis(axis_x)
            self.serieses[-1].attachAxis(axis_y)
            # self.serieses[-1].setUseOpenGL(True)

        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing, True)
        self.ui.LayoutCharts.addWidget(self.chart_view)

        self.ui.SliderDuration.setMaximum(MAX_CHART_SIGNAL_DURATION)
        self.ui.SliderDuration.setValue(MAX_CHART_SIGNAL_DURATION)
        self.ui.SliderDuration.setSliderPosition(MAX_CHART_SIGNAL_DURATION)

        self.update_ui()

        # --------------------UPDATE UI--------------------
    def update_ui(self):
        # Read slider params
        self.chart_duration = self.ui.SliderDuration.value()
        self.chart_amplitude = self.ui.SliderAmplitude.value()

        # Duration slider
        text = "Duration (sec): " + str(self.chart_duration)
        self.ui.LabelDuration.setText(text)
        self.chart_view.chart().axisX().setTickCount(self.chart_duration + 1)
        self.chart_view.chart().axisX().setRange(0, self.chart_duration)
        self.chart_buffer_update()

        # Amplitude slider
        text = "Amplitude (uV): " + str(self.chart_amplitude)
        self.ui.LabelAmplitude.setText(text)
        self.chart_view.chart().axisY().setRange(0, 8 * self.chart_amplitude)
        self.chart_buffer_update()

        # Autosave checkbox
        self.save_flag = self.ui.CheckBoxAutosave.isChecked()
        # Filtered save checkbox
        self.save_filtered_flag = self.ui.CheckBoxFiltered.isChecked()
        # Filtered chart checkbox
        self.chart_filtering_flag = self.ui.CheckBoxFilterChart.isChecked()

    def chart_buffer_update(self):
        self.chart_buffers = []
        for i in range(NUM_CHANNELS):
            self.chart_buffers.append([
                QPointF(x / SAMPLE_RATE,
                        self.chart_amplitude + (NUM_CHANNELS - 1 - i) * 2 * self.chart_amplitude)
                for x in range(self.chart_duration * SAMPLE_RATE)
            ])

    def redraw_charts(self):
        data = self.main_buffer.get_buff_last(
            (self.chart_duration + SIGNAL_CLIPPING_SEC) * SAMPLE_RATE)

        if np.any(data):
            for channel in range(NUM_CHANNELS):
                if self.chart_filtering_flag:
                    signal_filtering(data[channel])
                r_data = data[channel, SIGNAL_CLIPPING_SEC * SAMPLE_RATE:]
                for i in range(r_data.shape[0]):
                    self.chart_buffers[channel][i].setY(
                        r_data[i] + 50 + (NUM_CHANNELS - 1 - channel) * 100)
                self.serieses[channel].replace(self.chart_buffers[channel])

    def impedance_update(self):
        data = self.board.get_current_board_data(1)

        if np.any(data) > 0:
            data = data[RESISTANCE_CHANNELS, 0]
            self.ui.ProgressBarCh0.setValue(
                int(data[0]) if data[0] <= 100000 else 100000)
            self.ui.ProgressBarCh1.setValue(
                int(data[1]) if data[1] <= 100000 else 100000)
            if len(RESISTANCE_CHANNELS) > 2:
                self.ui.ProgressBarCh2.setValue(
                    int(data[2]) if data[2] <= 100000 else 100000)
                self.ui.ProgressBarCh3.setValue(
                    int(data[3]) if data[3] <= 100000 else 100000)

    def connect_toBB(self):
        params = BrainFlowInputParams()
        params.timeout = 10
        self.board = BoardShim(BOARD_ID, params)
        self.board.prepare_session()

    def result_connect_toBB(self):
        self.ui.ButtonStart.setEnabled(True)
        self.ui.ButtonDisconnect.setEnabled(True)
        self.ui.ButtonImpedanceStart.setEnabled(True)
        self.ui.ButtonSave.setEnabled(False)

    def update_buff(self):
        data = self.board.get_board_data()[EXG_CHANNELS, :]
        if np.any(data):
            self.main_buffer.add(data)

    def save_file_periodic(self):
        data = self.main_buffer.get_buff_from(self.last_save_index)
        if self.save_filtered_flag:
            for channel in range(NUM_CHANNELS):
                signal_filtering(data[channel])
        self.last_save_index += data.shape[1]

        save_file(data, self.file_name)

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
        self.ui.CheckBoxAutosave.setEnabled(False)
        self.ui.CheckBoxFiltered.setEnabled(False)
        self.ui.LinePatientFirstName.setEnabled(False)
        self.ui.LinePatientLastName.setEnabled(False)
        self.ui.ButtonSave.setEnabled(False)

        self.session = Session()

        if self.save_flag:
            self.patient = Patient(self.ui.LinePatientFirstName.text(),
                                   self.ui.LinePatientLastName.text())
            self.file_name = file_name_constructor(self.patient, self.session)
            self.ui.statusbar.showMessage(f'Saved in: {self.file_name}')
        else:
            self.ui.statusbar.showMessage(f'No saved')

        # main bufer init
        self.main_buffer = Buffer(buffer_size=10000, channels_num=NUM_CHANNELS)

        # timer to save file
        self.save_timer = QTimer()
        self.save_timer.timeout.connect(self.save_file_periodic)
        self.last_save_index = 0
        if self.save_flag:
            self.save_timer.start(SAVE_INTERVAL_MS)

        # board timer init and start
        self.board_timer = QTimer()
        self.board_timer.timeout.connect(self.update_buff)
        self.board_timer.start(UPDATE_BUFFER_SPEED_MS)

        # CHART buffer renew
        self.chart_buffer_update()

        # board start eeg stream
        self.board.start_stream(1000)
        self.board.config_board('CommandStartSignal')

        # Start timer for chart redraw
        self.chart_redraw_timer = QTimer()
        self.chart_redraw_timer.timeout.connect(self.redraw_charts)
        self.chart_redraw_timer.start(UPDATE_CHART_SPEED_MS)

    def _stop_capture(self):
        # stop timers
        self.chart_redraw_timer.stop()
        self.board_timer.stop()
        self.save_timer.stop()

        self.board.stop_stream()

        self.session.stop_session()

        self.ui.ButtonStart.setEnabled(True)
        self.ui.ButtonDisconnect.setEnabled(True)
        self.ui.ButtonStop.setEnabled(False)
        self.ui.ButtonImpedanceStart.setEnabled(True)
        self.ui.CheckBoxAutosave.setEnabled(True)
        self.ui.CheckBoxFiltered.setEnabled(True)
        self.ui.LinePatientFirstName.setEnabled(True)
        self.ui.LinePatientLastName.setEnabled(True)
        self.ui.ButtonSave.setEnabled(True)

    def _disconnect(self):
        # Release all BB resources
        if self.board.is_prepared():
            self.board.release_session()

        self.ui.ButtonDisconnect.setEnabled(False)
        self.ui.ButtonConnect.setEnabled(True)
        self.ui.ButtonImpedanceStart.setEnabled(False)
        self.ui.ButtonStart.setEnabled(False)

    def _start_impedance(self):
        self.board.start_stream(100)
        self.board.config_board('CommandStartResist')

        # Start timer for impedance renew
        self.impedance_update_timer = QTimer()
        self.impedance_update_timer.timeout.connect(self.impedance_update)
        self.impedance_update_timer.start(UPDATE_IMPEDANCE_SPEED_MS)

        self.ui.ButtonImpedanceStart.setEnabled(False)
        self.ui.ButtonImpedanceStop.setEnabled(True)
        self.ui.ButtonStart.setEnabled(False)
        self.ui.ButtonDisconnect.setEnabled(False)
        self.ui.ButtonSave.setEnabled(False)

    def _stop_impedance(self):
        self.board.config_board('CommandStopResist')
        self.board.stop_stream()
        self.impedance_update_timer.stop()

        self.ui.ButtonImpedanceStart.setEnabled(True)
        self.ui.ButtonImpedanceStop.setEnabled(False)
        self.ui.ButtonStart.setEnabled(True)
        self.ui.ButtonDisconnect.setEnabled(True)

    def _save_data(self):
        self.patient = Patient(self.ui.LinePatientFirstName.text(),
                               self.ui.LinePatientLastName.text())
        fileName = file_name_constructor(self.patient, self.session)
        file_name = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save eeg data (*.csv)', f'{fileName}')

        data = self.main_buffer.get_buff_last()

        if file_name[0]:
            save_file(data, file_name[0])

    def closeEvent(self, event):
        # Release all BB resources
        try:
            self.chart_redraw_timer.stop()
            self.board.stop_stream()
            if self.board.is_prepared():
                self.board.release_session()
        except:
            pass


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

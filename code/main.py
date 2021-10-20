import sys
from re import findall
from time import sleep
# import PySide6

import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from PySide6 import QtCore, QtWidgets
from PySide6.QtCharts import (QCategoryAxis, QChart, QChartView, QDateTimeAxis,
                              QLineSeries, QValueAxis)
from PySide6.QtCore import QDateTime, QPointF, QRectF, QThreadPool, QTimer
from PySide6.QtGui import QBrush, QColor, QPainter, QPen
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QProgressBar

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

        self.chart_duration = MAX_CHART_SIGNAL_DURATION
        self.chart_amp = self.ui.SliderAmplitude.value()
        self.session = Session()

        # bufers init
        self.buffer_main = Buffer(buffer_size=10000,
                                  channels_num=len(SAVE_CHANNEL))
        self.buffer_main.add(
            np.array([[0], [0], [0], [0],
                      [self.session.time_init.toMSecsSinceEpoch() / 1000],
                      [0]]))
        self.buffer_filtered = Buffer(buffer_size=10000,
                                      channels_num=len(SAVE_CHANNEL))
        self.buffer_filtered.add(
            np.array([[0], [0], [0], [0],
                      [self.session.time_init.toMSecsSinceEpoch() / 1000],
                      [0]]))

        self.battery_value = 0

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
        chart.legend().setVisible(False)

        # ////////////////////////////////////////////////////////////////axis_x
        axis_x = QValueAxis()
        axis_x.setRange(0, MAX_CHART_SIGNAL_DURATION * SAMPLE_RATE)
        axis_x.setVisible(False)
        axis_x.setLabelFormat('%i')
        chart.addAxis(axis_x, QtCore.Qt.AlignTop)
        # //////////////////////////////////////////////////////////////////////

        # ////////////////////////////////////////////////////////////////axis_y
        axis_y = QValueAxis()
        axis_y.setRange(0, self.chart_amp * NUM_CHANNELS * 2)
        axis_y.setTickCount(9)
        axis_y.setMinorTickCount(1)
        axis_y.setLabelsVisible(False)
        chart.addAxis(axis_y, QtCore.Qt.AlignRight)
        # //////////////////////////////////////////////////////////////////////

        # ////////////////////////////////////////////////////////////////axis_t
        axis_t = QCategoryAxis()
        axis_t.setRange(0, self.chart_duration * 1000)
        axis_t.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        axis_t.setTruncateLabels(False)
        axis_t = self.update_time_axis(axis_t)
        chart.addAxis(axis_t, QtCore.Qt.AlignBottom)
        # //////////////////////////////////////////////////////////////////////

        # ////////////////////////////////////////////////////////////////axis_c
        axis_c = QCategoryAxis()
        axis_c.setRange(0, 4)
        axis_c.setGridLineVisible(False)
        axis_c.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        self.update_channels_axis(axis_c)
        chart.addAxis(axis_c, QtCore.Qt.AlignLeft)
        # //////////////////////////////////////////////////////////////////////

        for i in range(NUM_CHANNELS):
            series = QLineSeries()
            series.setName(f'{EEG_CHANNEL_NAMES[i]}')
            # series.setColor('#209fdf')
            self.chart_buffers.append([
                QPointF(x, 20 + (NUM_CHANNELS - 1 - i) * 40)
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

        self.statusBar_main = QLabel()

        self.progressBar_battery = QProgressBar()
        self.progressBar_battery.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar_battery.setMaximumWidth(100)
        self.progressBar_battery.setMaximumHeight(18)

        self.ui.statusbar.addPermanentWidget(self.progressBar_battery)
        self.ui.statusbar.addWidget(self.statusBar_main)

        self.update_ui()

    # ///////////////////////////////////////////////////////// Update TIME axis
    def update_time_axis(self, axis_t, start_time=0):
        if start_time == 0:
            start_time = QDateTime.currentDateTime()

        offset = 1000 - int(start_time.toString('zzz'))
        labels = axis_t.categoriesLabels()
        for label in labels:
            axis_t.remove(label)

        axis_t.append(start_time.toString('hh:mm:ss.zzz'), 0)
        axis_t.append(' ', offset)

        for i in range(1, self.chart_duration - 1):
            shifted_time = start_time.addSecs(i + 1)
            axis_t.append(shifted_time.toString(':ss'), offset + i * 1000)

        axis_t.append('  ', (self.chart_duration - 1) * 1000 + offset)
        axis_t.append(
            start_time.addSecs(self.chart_duration).toString('hh:mm:ss.zzz'),
            self.chart_duration * 1000)

        return axis_t

    # ///////////////////////////////////////////////////// Update CHANNELS axis
    def update_channels_axis(self, axis_c):
        labels = axis_c.categoriesLabels()
        for i in range(len(labels)):
            axis_c.remove(labels[i])

        axis_c.append(f'{-self.chart_amp}', 0)
        for i, ch_name in enumerate(self.channel_names[NUM_CHANNELS - 1::-1]):
            axis_c.append(f'{-self.chart_amp // 2}' + i * ' ', i + 0.25)
            axis_c.append(f'--{ch_name}--', i + 0.5)
            axis_c.append(f'{self.chart_amp // 2}' + i * ' ', i + 0.75)
            if i < NUM_CHANNELS - 1:
                axis_c.append(f'({self.chart_amp})' + i * ' ', i + 1)
            else:
                axis_c.append(f'{self.chart_amp}', i + 1)

    # //////////////////////////////////////////////////////////////// UPDATE UI
    def update_ui(self):
        # Autosave checkbox
        self.save_flag = self.ui.CheckBoxAutosave.isChecked()
        # Filtered chart checkbox
        self.chart_filtering_flag = self.ui.CheckBoxFilterChart.isChecked()
        # Save fitered data flag
        self.save_filtered_flag = self.ui.CheckBoxSaveFiltered.isChecked()

        self.chart_buffer_update()
        self.timer_redraw_charts()

    def chart_buffer_update(self):
        self.chart_buffers = []
        for i in range(NUM_CHANNELS):
            self.chart_buffers.append([
                QPointF(
                    x, self.chart_amp +
                    (NUM_CHANNELS - 1 - i) * 2 * self.chart_amp)
                for x in range(self.chart_duration * SAMPLE_RATE)
            ])

    def timer_redraw_charts(self):
        if self.chart_filtering_flag:
            data = self.buffer_filtered.get_buff_last(self.chart_duration *
                                                      SAMPLE_RATE)
        else:
            data = self.buffer_main.get_buff_last(self.chart_duration *
                                                  SAMPLE_RATE)

        if np.any(data):
            self.redraw_charts(data)

    def redraw_charts(self, data):
        start_time = data[-2, 0]
        axis_t = self.chart_view.chart().axes()[2]
        self.update_time_axis(axis_t,
                              start_time=QDateTime.fromMSecsSinceEpoch(
                                  int(start_time * 1000)))
        for channel in range(NUM_CHANNELS):
            r_data = data[channel]
            for i in range(r_data.shape[0]):
                self.chart_buffers[channel][i].setY(
                    r_data[i] + self.chart_amp +
                    (NUM_CHANNELS - 1 - channel) * 2 * self.chart_amp)
            self.serieses[channel].replace(self.chart_buffers[channel])

    def timer_impedance(self):
        data = self.board.get_current_board_data(1)

        if np.any(data) > 0:
            data = data[RESISTANCE_CHANNELS, 0] / 1000
            self.ui.ProgressBarCh0.setValue(
                int(data[0]) if data[0] <= 500 else 500)
            self.ui.ProgressBarCh1.setValue(
                int(data[1]) if data[1] <= 500 else 500)
            if len(RESISTANCE_CHANNELS) > 2:
                self.ui.ProgressBarCh2.setValue(
                    int(data[2]) if data[2] <= 500 else 500)
                self.ui.ProgressBarCh3.setValue(
                    int(data[3]) if data[3] <= 500 else 500)

    def connect_toBB(self):
        params = BrainFlowInputParams()
        params.timeout = 5
        self.board = BoardShim(BOARD_ID, params)

        self.statusBar_main.setText('Connecting...')
        try:
            self.board.prepare_session()
        except BaseException as e:
            self.statusBar_main.setText(
                'Do not connect. Trying to connect again. ' +
                f'Exception: {e}.')
            exception = True
        else:
            exception = False

        if exception:
            sleep(3)
            self.statusBar_main.setText('Connecting...')
            try:
                self.board.prepare_session()
            except BaseException as exception:
                self.statusBar_main.setText(
                    f'Do not connect. Exception: {exception}.')
                self.ui.ButtonConnect.setEnabled(True)
                exception = True
            else:
                exception = False

        if not exception:
            self.statusBar_main.setText('Connected.')
            self.ui.ButtonStart.setEnabled(True)
            self.ui.ButtonDisconnect.setEnabled(True)
            self.ui.ButtonImpedanceStart.setEnabled(True)
            self.ui.ButtonSave.setEnabled(False)

    def timer_update_buff(self):
        data = self.board.get_board_data()
        if np.any(data):
            self.buffer_main.add(data[SAVE_CHANNEL, :])

            bat_val = np.ceil(np.mean(data[BATTERY_CHANNEL, -1]))
            if self.battery_value != bat_val:
                self.battery_value = bat_val
                self.progressBar_battery.setValue(self.battery_value)

        add_sample = data.shape[1]
        if add_sample != 0:
            self.filtered_buffer_update(add_sample)

    def filtered_buffer_update(self, add_sample):
        data = self.buffer_main.get_buff_last(SIGNAL_CLIPPING_SEC *
                                              SAMPLE_RATE + add_sample)
        for channel in range(NUM_CHANNELS):
            signal_filtering(data[channel])
        self.buffer_filtered.add(data[:, -add_sample:])

    def timer_save_file(self):
        if self.session.save_filtered:
            data = self.buffer_filtered.get_buff_from(self.last_save_index)
        else:
            data = self.buffer_main.get_buff_from(self.last_save_index)

        save_file(data, self.patient, self.session, self.file_name,
                  self.save_first)

        self.last_save_index += data.shape[1]
        self.save_first = False

    # ///////////////////////////////////////////////////////////////UI BEHAVIOR
    def _connect(self):
        self.ui.ButtonConnect.setEnabled(False)

        worker = Worker(self.connect_toBB)
        self.threadpool.start(worker)

    def _start_capture(self):
        self.ui.ButtonStart.setEnabled(False)
        self.ui.ButtonDisconnect.setEnabled(False)
        self.ui.ButtonStop.setEnabled(True)
        self.ui.ButtonImpedanceStart.setEnabled(False)
        self.ui.CheckBoxAutosave.setEnabled(False)
        self.ui.CheckBoxSaveFiltered.setEnabled(False)
        self.ui.LinePatientFirstName.setEnabled(False)
        self.ui.LinePatientLastName.setEnabled(False)
        self.ui.ButtonSave.setEnabled(False)
        self.ui.SliderChart.setEnabled(False)

        self.save_first = True

        self.session = Session(self.save_filtered_flag)
        self.session.session_start()

        if self.save_flag:
            self.patient = Patient(self.ui.LinePatientFirstName.text(),
                                   self.ui.LinePatientLastName.text())

            self.file_name = '(f)' if self.session.save_filtered else ''
            self.file_name += file_name_constructor(self.patient, self.session)
            self.statusBar_main.setText(f'Saved in: {self.file_name}')
            # timer to save file
            self.save_timer = QTimer()
            self.save_timer.timeout.connect(self.timer_save_file)
            self.save_timer.start(SAVE_INTERVAL_MS)
            self.last_save_index = 0
        else:
            self.statusBar_main.setText(f'No saved')

        # bufers init
        self.buffer_main = Buffer(buffer_size=10000,
                                  channels_num=len(SAVE_CHANNEL))
        self.buffer_filtered = Buffer(buffer_size=10000,
                                      channels_num=len(SAVE_CHANNEL))

        # board timer init and start
        self.board_timer = QTimer()
        self.board_timer.timeout.connect(self.timer_update_buff)
        self.board_timer.start(UPDATE_BUFFER_SPEED_MS)

        # CHART buffer renew
        self.chart_buffer_update()
        self.timer_redraw_charts()

        # board start eeg stream
        self.board.start_stream(1000)
        self.board.config_board('CommandStartSignal')
        self.board.get_board_data()

        # Start timer for chart redraw
        self.chart_redraw_timer = QTimer()
        self.chart_redraw_timer.timeout.connect(self.timer_redraw_charts)
        self.chart_redraw_timer.start(UPDATE_CHART_SPEED_MS)

    def _stop_capture(self):
        # stop timers
        self.chart_redraw_timer.stop()
        self.save_timer.stop()
        self.board_timer.stop()

        self.board.stop_stream()

        self.session.stop_session()

        if self.save_flag:
            self.timer_save_file()

        self.ui.ButtonStart.setEnabled(True)
        self.ui.ButtonDisconnect.setEnabled(True)
        self.ui.ButtonStop.setEnabled(False)
        self.ui.ButtonImpedanceStart.setEnabled(True)
        self.ui.CheckBoxAutosave.setEnabled(True)
        self.ui.CheckBoxSaveFiltered.setEnabled(True)
        self.ui.LinePatientFirstName.setEnabled(True)
        self.ui.LinePatientLastName.setEnabled(True)
        self.ui.ButtonSave.setEnabled(True)
        self.ui.SliderChart.setEnabled(True)

        buff_size = self.buffer_filtered.get_last_num()
        slider_maximum = buff_size - self.chart_duration * SAMPLE_RATE
        if slider_maximum < 0:
            slider_maximum = 0
        self.ui.SliderChart.setMaximum(slider_maximum)
        self.ui.SliderChart.setValue(slider_maximum)

    def _disconnect(self):
        # Release all BB resources
        if self.board.is_prepared():
            self.board.release_session()

        self.statusBar_main.setText('Disсonnected.')

        self.ui.ButtonDisconnect.setEnabled(False)
        self.ui.ButtonConnect.setEnabled(True)
        self.ui.ButtonImpedanceStart.setEnabled(False)
        self.ui.ButtonStart.setEnabled(False)

    def _start_impedance(self):
        self.board.start_stream(100)
        self.board.config_board('CommandStartResist')

        # Start timer for impedance renew
        self.impedance_update_timer = QTimer()
        self.impedance_update_timer.timeout.connect(self.timer_impedance)
        self.impedance_update_timer.start(UPDATE_IMPEDANCE_SPEED_MS)

        self.ui.ButtonImpedanceStart.setEnabled(False)
        self.ui.ButtonImpedanceStop.setEnabled(True)
        self.ui.ButtonStart.setEnabled(False)
        self.ui.ButtonDisconnect.setEnabled(False)
        self.ui.ButtonSave.setEnabled(False)

    def _stop_impedance(self):
        self.impedance_update_timer.stop()
        self.board.config_board('CommandStopResist')
        self.board.stop_stream()

        self.ui.ButtonImpedanceStart.setEnabled(True)
        self.ui.ButtonImpedanceStop.setEnabled(False)
        self.ui.ButtonStart.setEnabled(True)
        self.ui.ButtonDisconnect.setEnabled(True)

    def _save_data(self):
        self.patient = Patient(self.ui.LinePatientFirstName.text(),
                               self.ui.LinePatientLastName.text())

        fileName = '(f)' if self.save_filtered_flag else ''
        fileName += file_name_constructor(self.patient, self.session)
        file_name = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save eeg data (*.csv)', f'{fileName}')

        if self.save_filtered_flag:
            data = self.buffer_filtered.get_buff_last()
        else:
            data = self.buffer_main.get_buff_last()

        if file_name[0]:
            save_file(data, file_name[0])

    def _sliderDuration_cnd(self):
        self.chart_duration = self.ui.SliderDuration.value()
        text = "Duration (sec): " + str(self.chart_duration)
        self.ui.LabelDuration.setText(text)

        axis_x = self.chart_view.chart().axisX()
        axis_x.setRange(0, self.chart_duration * SAMPLE_RATE)

        axis_t = self.chart_view.chart().axes()[2]
        axis_t.setRange(0, self.chart_duration * 1000)

        if self.session.status:
            buff_size = self.buffer_filtered.get_last_num()
            slider_maximum = buff_size - self.chart_duration * SAMPLE_RATE
            if slider_maximum < 0:
                slider_maximum = 0

            if self.ui.SliderChart.value() > slider_maximum:
                self.ui.SliderChart.setValue(slider_maximum)
            self.ui.SliderChart.setMaximum(slider_maximum)
            self._slider_value_cnd()
        else:
            self.update_time_axis(axis_t, self.session.time_init)
            self.chart_buffer_update()
            self.timer_redraw_charts()

    def _sliderAmplitude_cnd(self):
        self.chart_amp = self.ui.SliderAmplitude.value()
        text = "Amplitude (uV): " + str(self.chart_amp)
        self.ui.LabelAmplitude.setText(text)

        self.chart_view.chart().axisY().setRange(0, 8 * self.chart_amp)

        axis_c = self.chart_view.chart().axes()[3]
        self.update_channels_axis(axis_c)

        self.chart_buffer_update()
        self.timer_redraw_charts()

    def _slider_value_cnd(self):
        start_index = self.ui.SliderChart.value()
        end_index = start_index + self.chart_duration * SAMPLE_RATE

        if self.chart_filtering_flag:
            data = self.buffer_filtered.get_buff_from(start_index, end_index)
        else:
            data = self.buffer_main.get_buff_from(start_index, end_index)

        self.chart_buffer_update()
        self.redraw_charts(data)

    def _firstName_edit(self):
        text = self.ui.LinePatientFirstName.text()
        result = ''.join(findall(REG_KERNEL, text))
        if text != result:
            self.ui.LinePatientFirstName.setText(''.join(result))

    def _lastName_edit(self):
        text = self.ui.LinePatientLastName.text()
        result = ''.join(findall(REG_KERNEL, text))
        if text != result:
            self.ui.LinePatientLastName.setText(''.join(result))

    def closeEvent(self, event):
        # Release all BB resources
        try:
            self.chart_redraw_timer.stop()
            self.board_timer.stop()
            self.save_timer.stop()
            # this is poor
            self.session.stop_session()
        except:
            pass

        try:
            self.board.stop_stream()
        except:
            pass

        try:
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

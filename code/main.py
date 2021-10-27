import sys
from re import findall
from time import sleep

import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from PySide6 import QtCore, QtWidgets
from PySide6.QtCharts import (QCategoryAxis, QChart, QChartView, QLineSeries,
                              QValueAxis)
from PySide6.QtCore import QDateTime, QPointF, QThreadPool, QTimer
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QProgressBar

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

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.SliderDuration.setMaximum(MAX_CHART_SIGNAL_DURATION)
        self.ui.SliderDuration.setValue(MAX_CHART_SIGNAL_DURATION)
        self.ui.SliderDuration.setSliderPosition(MAX_CHART_SIGNAL_DURATION)
        self.chart_duration = MAX_CHART_SIGNAL_DURATION
        self.battery_value = 0
        self.chart_filtering_flag = True
        self.chart_detrend_flag = False
        self.redraw_charts_request = False
        self.chart_amp = self.ui.SliderAmplitude.value()
        self.session = Session(buffer_size=10)
        self.charts = []

        # ////////////////////////////////////////////////////// BUFFERS FILLING
        self.session.add(
            np.array([[0], [0], [0], [0],
                      [self.session.time_init.toMSecsSinceEpoch() / 1000],
                      [0]]))

        # ///////////////////////////////////////////////// IMPEDANSE LABEL FILL
        self.ui.LabelCh0.setText(EEG_CHANNEL_NAMES[0])
        self.ui.LabelCh1.setText(EEG_CHANNEL_NAMES[1])
        self.ui.LabelCh2.setText(EEG_CHANNEL_NAMES[2])
        self.ui.LabelCh3.setText(EEG_CHANNEL_NAMES[3])

        # /////////////////////////////////////////////////////////// CHART MAKE
        self.channel_names = BoardShim.get_board_descr(
            BOARD_ID)['eeg_names'].split(',')
        chart = QChart()
        chart.legend().setVisible(False)
        # /////////////////////////////////////////////////////////////// axis_x
        axis_x = QValueAxis()
        axis_x.setRange(0, MAX_CHART_SIGNAL_DURATION * SAMPLE_RATE)
        axis_x.setVisible(False)
        axis_x.setLabelFormat('%i')
        chart.addAxis(axis_x, QtCore.Qt.AlignTop)
        # /////////////////////////////////////////////////////////////// axis_y
        axis_y = QValueAxis()
        axis_y.setRange(0, self.chart_amp * NUM_CHANNELS * 2)
        axis_y.setTickCount(9)
        axis_y.setMinorTickCount(1)
        axis_y.setLabelsVisible(False)
        chart.addAxis(axis_y, QtCore.Qt.AlignRight)
        # /////////////////////////////////////////////////////////////// axis_t
        axis_t = QCategoryAxis()
        axis_t.setRange(0, self.chart_duration * 1000)
        axis_t.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        axis_t.setTruncateLabels(False)
        axis_t = self.update_time_axis(axis_t)
        chart.addAxis(axis_t, QtCore.Qt.AlignBottom)
        # /////////////////////////////////////////////////////////////// axis_c
        axis_c = QCategoryAxis()
        axis_c.setRange(0, 4)
        axis_c.setGridLineVisible(False)
        axis_c.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        self.update_channels_axis(axis_c)
        chart.addAxis(axis_c, QtCore.Qt.AlignLeft)
        # //////////////////////////////////////////////////////// serieses fill
        self.serieses = []
        self.chart_buffers_update()
        for i in range(NUM_CHANNELS):
            series = QLineSeries()
            series.setName(f'{EEG_CHANNEL_NAMES[i]}')
            series.append(self.chart_buffers[i])
            self.serieses.append(series)
            chart.addSeries(self.serieses[-1])
            self.serieses[-1].attachAxis(axis_x)
            self.serieses[-1].attachAxis(axis_y)
        # //////////////////////////////////////////////////// Chart viev create
        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing, True)
        self.ui.LayoutCharts.addWidget(self.chart_view)

        # ////////////////////////////////////////////////////// STATUS BAR MAKE
        self.statusBar_main = QLabel()
        self.progressBar_battery = QProgressBar()
        self.progressBar_battery.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar_battery.setMaximumWidth(100)
        self.progressBar_battery.setMaximumHeight(18)
        self.ui.statusbar.addPermanentWidget(self.progressBar_battery)
        self.ui.statusbar.addWidget(self.statusBar_main)

        # //////////////////////////////////////////////////////////// MAIN MENU

        self.update_ui()

    # //////////////////////////////////////////////////////////////// UPDATE UI
    def update_ui(self):
        # Autosave checkbox
        self.save_flag = self.ui.CheckBoxAutosave.isChecked()
        # Save fitered data flag
        self.save_filtered_flag = self.ui.CheckBoxSaveFiltered.isChecked()

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
            axis_t.append(shifted_time.toString('ss'), offset + i * 1000)

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

    def chart_buffers_update(self):
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
            data = self.session.buffer_filtered.get_buff_last(
                self.chart_duration * SAMPLE_RATE)
        else:
            data = self.session.buffer_main.get_buff_last(self.chart_duration *
                                                          SAMPLE_RATE)

            if self.chart_detrend_flag:
                for channel in range(NUM_CHANNELS):
                    signal_filtering(data[channel], filtering=False)

        if np.any(data):
            self.redraw_charts(data)


    def request_realisation(self):
        # Slider AMPLITUDE
        self.chart_amp = self.ui.SliderAmplitude.value()
        text = "Amplitude (uV): " + str(self.chart_amp)
        self.ui.LabelAmplitude.setText(text)
        self.chart_view.chart().axisY().setRange(0, 8 * self.chart_amp)
        axis_c = self.chart_view.chart().axes()[3]
        self.update_channels_axis(axis_c)
        self.chart_buffers_update()

        # Slider DURATION
        self.chart_duration = self.ui.SliderDuration.value()
        text = "Duration (sec): " + str(self.chart_duration)
        self.ui.LabelDuration.setText(text)
        axis_x = self.chart_view.chart().axisX()
        axis_x.setRange(0, self.chart_duration * SAMPLE_RATE)
        axis_t = self.chart_view.chart().axes()[2]
        axis_t.setRange(0, self.chart_duration * 1000)

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

        for channel in range(NUM_CHANNELS):
            self.serieses[channel].replace(self.chart_buffers[channel])
            
        if self.redraw_charts_request:
            self.redraw_charts_request = False
            self.request_realisation()
            self.timer_redraw_charts()

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

    def timer_long_events(self):
        def sf(self):
            if self.session.save_filtered:
                data = self.session.buffer_filtered.get_buff_from(
                    self.last_save_index)
            else:
                data = self.session.buffer_main.get_buff_from(
                    self.last_save_index)
            save_file(data, self.session, self.file_name, self.save_first)
            self.last_save_index += data.shape[1]
            self.save_first = False

        if self.save_flag:
            sf(self)

        self.progressBar_battery.setValue(self.session.get_battery_value())

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

    # ////////////////////////////////////////////////////////////// UI BEHAVIOR
    # ////////////////////////////////////////////////////////////////// CONNECT
    def _connect(self):
        self.ui.ButtonConnect.setEnabled(False)
        self.worker_connect = Worker(self.connect_toBB)
        self.worker_connect.start()

    # //////////////////////////////////////////////////////////////////// START
    def _start_capture(self):
        self.save_first = True

        # CHART buffer renew
        self.chart_buffers_update()

        self.session = Session(self.save_filtered_flag,
                               first_name=self.ui.LinePatientFirstName.text(),
                               last_name=self.ui.LinePatientLastName.text())

        self.session.session_start(self.board)

        self.long_timer = QTimer()
        self.long_timer.timeout.connect(self.timer_long_events)
        self.long_timer.start(LONG_TIMER_INTERVAL_MS)

        if self.save_flag:
            self.file_name = '(f)' if self.session.get_filtered_status(
            ) else ''
            self.file_name += file_name_constructor(self.session)
            self.statusBar_main.setText(f'Saved in: {self.file_name}')
            self.last_save_index = 0
        else:
            self.statusBar_main.setText(f'No saved')

        # board start eeg stream
        self.board.start_stream(1000)
        self.board.config_board('CommandStartSignal')

        # INIT and START timer_redraw_charts
        self.chart_redraw_timer = QTimer()
        self.chart_redraw_timer.timeout.connect(self.timer_redraw_charts)
        self.chart_redraw_timer.start(UPDATE_CHART_SPEED_MS)

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

    # ///////////////////////////////////////////////////////////////////// STOP
    def _stop_capture(self):
        # stop timers
        self.chart_redraw_timer.stop()
        self.session.session_stop()
        self.long_timer.stop()
        self.board.stop_stream()
        if self.save_flag:
            self.timer_long_events()

        buff_size = self.session.buffer_filtered.get_last_num()
        slider_maximum = buff_size - self.chart_duration * SAMPLE_RATE
        if slider_maximum < 0:
            slider_maximum = 0
        self.ui.SliderChart.setMaximum(slider_maximum)
        self.ui.SliderChart.setValue(slider_maximum)

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
        fileName = '(f)' if self.save_filtered_flag else ''
        fileName += file_name_constructor(self.session)
        file_name = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save eeg data (*.csv)', f'{fileName}')

        if self.save_filtered_flag:
            data = self.session.buffer_filtered.get_buff_last()
        else:
            data = self.session.buffer_main.get_buff_last()

        if file_name[0]:
            save_file(data, file_name[0])

    def _sliderDuration_cnd(self):
        self._chart_redraw_request()

        # self.chart_duration = self.ui.SliderDuration.value()
        # text = "Duration (sec): " + str(self.chart_duration)
        # self.ui.LabelDuration.setText(text)

        # axis_x = self.chart_view.chart().axisX()
        # axis_x.setRange(0, self.chart_duration * SAMPLE_RATE)

        # axis_t = self.chart_view.chart().axes()[2]
        # axis_t.setRange(0, self.chart_duration * 1000)

        # if not self.session.status:
        #     buff_size = self.session.buffer_filtered.get_last_num()
        #     slider_maximum = buff_size - self.chart_duration * SAMPLE_RATE
        #     if slider_maximum < 0:
        #         slider_maximum = 0

        #     if self.ui.SliderChart.value() > slider_maximum:
        #         self.ui.SliderChart.setValue(slider_maximum)

        #     self.ui.SliderChart.setMaximum(slider_maximum)
        #     self._slider_value_cnd()

        #     self.update_time_axis(axis_t, self.session.time_init)
        #     self.chart_buffers_update()
        #     self.timer_redraw_charts()

    def _chart_redraw_request(self):
        if self.session.get_status():
            self.redraw_charts_request = True
        else:
            self.request_realisation()
            self.timer_redraw_charts()

    def _slider_value_cnd(self):
        start_index = self.ui.SliderChart.value()
        end_index = start_index + self.chart_duration * SAMPLE_RATE

        if self.chart_filtering_flag:
            data = self.session.buffer_filtered.get_buff_from(
                start_index, end_index)
        else:
            data = self.session.buffer_main.get_buff_from(
                start_index, end_index)

        # print(data.shape)

        self.chart_buffers_update()
        self.redraw_charts(data)

    def _checkBoxFilteredChart(self):
        self.chart_filtering_flag = self.ui.CheckBoxFilterChart.isChecked()
        self.ui.CheckBoxDetrendChart.setEnabled(not self.chart_filtering_flag)

        if self.chart_filtering_flag:
            self.ui.CheckBoxDetrendChart.setChecked(False)

        self._chart_redraw_request()

    def _checkBoxDetrendChart(self):
        self.chart_detrend_flag = self.ui.CheckBoxDetrendChart.isChecked()
        if self.chart_detrend_flag:
            self.ui.SliderAmplitude.setMaximum(400000)
        else:
            self.ui.SliderAmplitude.setMaximum(200)

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

    # ////////////////////////////////////////////////////////////// MENU ACTION
    def _open_file(self):
        delimiter = ';'

        file_name = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open eeg data (*.csv)', filter="CSV file (*.csv)")
        file_name = file_name[0]

        with open(file_name) as file_object:
            first_name = file_object.readline().rstrip().lstrip('#')
            last_name = file_object.readline().rstrip().lstrip('#')
            data = file_object.readline().rstrip().lstrip('#')
            time = file_object.readline().rstrip().lstrip('#')
            header = file_object.readline().rstrip().lstrip('#').split(
                delimiter)

        print('\n', first_name, last_name, data, time, '\n', header, '\n')

        data = np.loadtxt(file_name, delimiter=delimiter).T

        print(data[0])

    def closeEvent(self, event):
        # Release all BB resources
        try:
            self.long_timer.stop()
            self.session.session_stop()
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

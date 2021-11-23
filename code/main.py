import sys
from re import findall
from time import sleep

import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from PySide6 import QtCore, QtWidgets
from PySide6.QtCharts import QChartView, QLineSeries
from PySide6.QtCore import QDateTime, QTimer
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QProgressBar

import fileio
from board import Board
import chart as ch
from main_uiinteraction import *
from rhytmwindow import RhytmWindow
from session import Session
from settings import *
from ui_mainwindow import Ui_MainWindow
from utils import file_name_constructor, save_CSV, save_EDF, signal_filtering
from worker import Worker

np.set_printoptions(precision=1, suppress=True)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.SliderDuration.setMaximum(MAX_CHART_SIGNAL_DURATION)
        self.ui.SliderDuration.setValue(MAX_CHART_SIGNAL_DURATION)
        self.ui.SliderDuration.setSliderPosition(MAX_CHART_SIGNAL_DURATION)
        self.chart_duration = MAX_CHART_SIGNAL_DURATION
        self.redraw_charts_request = False
        self.battery_value = 0
        self.chart_filt_flag = True
        self.chart_detrend_flag = False
        self.chart_amp = self.ui.SliderAmplitude.value()
        self.filtered = False
        self.charts = []

        self.r_window = None

        self.session = Session(buffer_size=10)
        self.set_eeg_ch_names()

        # //////////////////////////////////////////////////////////////// CHART
        chart, axis_x, axis_y = ch.init(self.session, self.chart_amp,
                                        NUM_CHANNELS)
        self.serieses = []
        self.chart_buffers = ch.buffers_update(self.chart_amp,
                                               self.session.get_eeg_ch_names(),
                                               self.chart_duration,
                                               self.session.get_sample_rate())
        for i in range(NUM_CHANNELS):
            series = QLineSeries()
            series.append(self.chart_buffers[i])
            self.serieses.append(series)
            chart.addSeries(self.serieses[-1])
            self.serieses[-1].attachAxis(axis_x)
            self.serieses[-1].attachAxis(axis_y)

        # //////////////////////////////////////////////////// Chart view create
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

        self.update_ui()

    # //////////////////////////////////////////////////////////////// UPDATE UI
    def update_ui(self):
        # Autosave checkbox
        self.save_flag = self.ui.CheckBoxAutosave.isChecked()
        # Save fitered data flag
        self.save_filtered_flag = self.ui.CheckBoxSaveFiltered.isChecked()

    def timer_redraw_charts(self):
        if self.ui.CheckBoxRenew.isChecked():
            if self.chart_filt_flag:
                data = self.session.buffer_filtered.get_buff_last(
                    self.chart_duration * self.session.get_sample_rate())
            else:
                data = self.session.buffer_main.get_buff_last(
                    self.chart_duration * self.session.get_sample_rate())

                if (self.chart_detrend_flag and np.any(data)
                        and data.shape[1] != 0):
                    for channel in range(NUM_CHANNELS):
                        signal_filtering(data[channel],
                                         self.session.get_sample_rate(),
                                         filtering=False)

            if data.shape[1] > 0: self.redraw_charts(data)

        if self.r_window and not self.r_window.redraw_pause:
            self.r_window.event_redraw_charts()

    def request_realisation(self):
        # Slider AMPLITUDE
        self.chart_amp = self.ui.SliderAmplitude.value()
        text = "Amplitude (uV): " + str(self.chart_amp)
        self.ui.LabelAmplitude.setText(text)
        self.chart_view.chart().axisY().setRange(0, 8 * self.chart_amp)
        axis_c = self.chart_view.chart().axes()[3]
        ch.update_channels_axis(axis_c, self.session, self.chart_amp,
                                NUM_CHANNELS)

        # Slider DURATION
        self.chart_duration = self.ui.SliderDuration.value()
        text = "Duration (sec): " + str(self.chart_duration)
        self.ui.LabelDuration.setText(text)
        axis_x = self.chart_view.chart().axisX()
        axis_x.setRange(0,
                        self.chart_duration * self.session.get_sample_rate())
        axis_t = self.chart_view.chart().axes()[2]
        axis_t.setRange(0, self.chart_duration * 1000)

        self.chart_buffers = ch.buffers_update(self.chart_amp,
                                               self.session.get_eeg_ch_names(),
                                               self.chart_duration,
                                               self.session.get_sample_rate())

    def redraw_charts(self, data):
        start_tick = data[-2, 0]
        if start_tick != 0:
            start_time = QDateTime.fromMSecsSinceEpoch(int(start_tick * 1000))
        else:
            start_time = QDateTime.currentDateTime()

        axis_t = self.chart_view.chart().axes()[2]
        ch.update_time_axis(self.chart_duration, axis_t, start_time=start_time)
        for channel in range(NUM_CHANNELS):
            r_data = data[channel]
            for i in range(r_data.shape[0]):
                self.chart_buffers[channel][i].setY(
                    r_data[i] + self.chart_amp +
                    (NUM_CHANNELS - 1 - channel) * 2 * self.chart_amp)
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

    def timer_long(self):

        if not self.file_name:
            self.file_name = file_name_constructor(self.session)
            self.file_name += '.csv'
            self.statusBar_main.setText(f'Saved in: {self.file_name}')

        if self.save_flag:
            self.last_save_index += save_CSV(
                self.session,
                self.file_name,
                FOLDER,
                self.save_first,
                self.last_save_index,
            )
            self.save_first = False

        self.progressBar_battery.setValue(self.session.get_battery_value())

    def timer_short(self):
        if self.r_window and self.r_window.ui.splitter.sizes()[1] > 0:
            self.r_window.new_analyze_data()

    def connect_toBB(self):
        params = BrainFlowInputParams()
        params.timeout = BOARD_TIMEOUT
        self.board = BoardShim(BOARD_ID, params)

        self.statusBar_main.setText('Connecting...')

        exception = True
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
            except BaseException as e:
                self.statusBar_main.setText(f'Do not connect. Exception: {e}.')
                connect_1(self.ui)
                exception = True
            else:
                exception = False

        if not exception:
            self.session.connect()
            self.statusBar_main.setText('Connected.')
            connect_2(self.ui)

            if self.r_window: self.r_window.ui.ButtonStart.setEnabled(True)

            self.filtered = False

    # ////////////////////////////////////////////////////////////// UI BEHAVIOR
    # ////////////////////////////////////////////////////////////////// CONNECT
    def _connect(self):
        connect_0(self.ui)

        self.worker_connect = Worker(self.connect_toBB)
        self.worker_connect.start()

        # self.board = Board()

        self.session = Session(self.save_filtered_flag,
                               first_name=self.ui.LinePatientFirstName.text(),
                               last_name=self.ui.LinePatientLastName.text())
        self.set_eeg_ch_names()
        self._chart_redraw_request()

    # //////////////////////////////////////////////////////////////////// START
    def _start_capture(self):
        self.session = Session(self.save_filtered_flag,
                               first_name=self.ui.LinePatientFirstName.text(),
                               last_name=self.ui.LinePatientLastName.text())
        self.set_eeg_ch_names()

        self.save_first = True

        # CHART buffer renew
        self.chart_buffers = ch.buffers_update(self.chart_amp,
                                               self.session.get_eeg_ch_names(),
                                               self.chart_duration,
                                               self.session.get_sample_rate())

        # board start eeg stream
        self.board.start_stream(1000)
        self.board.config_board('CommandStartSignal')
        self.session.session_start(self.board)

        # INIT and START timer_long_events
        self.long_timer = QTimer()
        self.long_timer.timeout.connect(self.timer_long)
        self.long_timer.start(LONG_TIMER_INTERVAL_MS)

        # INIT and START timer_short_events
        self.short_timer = QTimer()
        self.short_timer.timeout.connect(self.timer_short)
        self.short_timer.start(LONG_TIMER_INTERVAL_MS / 2)

        self.file_name = None
        self.last_save_index = 0
        if not self.save_flag: self.statusBar_main.setText(f'No saved')

        # INIT and START timer_redraw_charts
        self.chart_redraw_timer = QTimer()
        self.chart_redraw_timer.timeout.connect(self.timer_redraw_charts)
        self.chart_redraw_timer.start(UPDATE_CHART_SPEED_MS)

        start(self.ui)

        # if not self.ui.CheckBoxRenew.isChecked():
        #     self._chart_redraw_request()

        if self.r_window:
            self.r_window.data = self.session.buffer_main
            self.r_window.start()

    # ///////////////////////////////////////////////////////////////////// STOP
    def _stop_capture(self):
        self.chart_redraw_timer.stop()
        self.session.session_stop()
        self.long_timer.stop()
        self.short_timer.stop()
        self.board.stop_stream()
        if self.save_flag: self.timer_long()

        if not self.ui.CheckBoxRenew.isChecked():
            self._chart_redraw_request()

        self.slider_chart_prepare()
        self.ui.SliderChart.setValue(self.ui.SliderChart.maximum())

        stop(self.ui)

        if self.r_window: self.r_window._stop()

    def _disconnect(self):
        # Release all BB resources
        if self.board.is_prepared(): self.board.release_session()

        self.session.disconnect()

        self.statusBar_main.setText('Disсonnected.')
        disconnect(self.ui)

        if self.r_window:
            self.r_window._stop()
            self.r_window.ui.ButtonStart.setEnabled(False)

    def _start_impedance(self):
        self.board.start_stream(100)
        self.board.config_board('CommandStartResist')

        # Start timer for impedance renew
        self.impedance_update_timer = QTimer()
        self.impedance_update_timer.timeout.connect(self.timer_impedance)
        self.impedance_update_timer.start(UPDATE_IMPEDANCE_SPEED_MS)

        start_impedance(self.ui)

    def _stop_impedance(self):
        self.impedance_update_timer.stop()
        self.board.config_board('CommandStopResist')
        self.board.stop_stream()

        stop_impedance(self.ui)

    def _save_file(self):
        fileName = file_name_constructor(self.session)
        if self.ui.CheckBoxSaveFiltered.isChecked():
            fileName = '(f)' + fileName

        file_name = QtWidgets.QFileDialog.getSaveFileName(
            self,
            caption='Save eeg data',
            dir=f'{FOLDER}/{fileName}',
            filter='EDF file (*.edf);;CSV file (*.csv)')[0]

        if file_name:
            end_f = file_name.rfind('.')
            if end_f != -1: extension = file_name[end_f + 1:]

            if extension.upper() == 'CSV':
                save_CSV(self.session, file_name, auto=False)
            elif extension.upper() == 'EDF':
                save_EDF(self.session, file_name)

        file_name_str = file_name.replace('/', '\\')
        self.statusBar_main.setText(f'Saved in: {file_name_str}')

    def _chart_redraw_request(self):
        if self.session.get_status() and self.ui.CheckBoxRenew.isChecked():
            self.redraw_charts_request = True
        else:
            self.request_realisation()
            self._slider_value_cnd()

    def _slider_value_cnd(self):
        self.slider_chart_prepare()

        start_ind = self.ui.SliderChart.value()
        sample_rate = self.session.get_sample_rate()
        end_ind = start_ind + self.chart_duration * sample_rate

        if self.chart_filt_flag:
            data = self.session.buffer_filtered.get_buff_from(
                start_ind, end_ind)
        else:
            data = self.session.buffer_main.get_buff_from(start_ind, end_ind)

        self.chart_buffers = ch.buffers_update(self.chart_amp,
                                               self.session.get_eeg_ch_names(),
                                               self.chart_duration,
                                               sample_rate)
        self.redraw_charts(data)

    def slider_chart_prepare(self):
        buff_s = self.session.buffer_filtered.get_last_num()
        sl_max = buff_s - self.chart_duration * self.session.get_sample_rate()
        if sl_max < 0: sl_max = 0
        self.ui.SliderChart.setMaximum(sl_max)

    def _checkBoxFilteredChart(self):
        self.chart_filt_flag = self.ui.CheckBoxFilterChart.isChecked()
        self.ui.CheckBoxDetrendChart.setEnabled(not self.chart_filt_flag)

        if self.chart_filt_flag: self.ui.CheckBoxDetrendChart.setChecked(False)

        self._chart_redraw_request()

    def _checkBoxDetrendChart(self):
        self.chart_detrend_flag = self.ui.CheckBoxDetrendChart.isChecked()
        self.ui.SliderAmplitude.setMaximum(
            20000 if self.chart_detrend_flag else 200)

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
        file_name = QtWidgets.QFileDialog.getOpenFileName(
            self,
            'Open eeg data (*.csv)',
            dir=FOLDER,
            filter="EEG file (*.csv *.edf)")

        file_name = file_name[0]

        if file_name != '':
            end_f = file_name.rfind('.')
            if end_f != -1: extension = file_name[end_f + 1:]
            if extension.upper() == 'CSV':
                f_struct = fileio.read_CSV(file_name)
            elif extension.upper() == 'EDF':
                f_struct = fileio.read_EDF(file_name)

            table = f_struct['table']
            self.filtered = f_struct['filtered_flag']
            self.session = Session(buffer_size=table.shape[1],
                                   first_name=f_struct['first_name'],
                                   last_name=f_struct['last_name'],
                                   eeg_channel_names=f_struct['ch_names'],
                                   sample_rate=f_struct.get(
                                       's_rate', SAMPLE_RATE))
            self.session.add(table)

            f_struct.clear()

            self.ui.CheckBoxFilterChart.setEnabled(not self.filtered)
            self.set_eeg_ch_names()
            file_name = file_name.replace('/', '\\')
            self.statusBar_main.setText(f'Open file: {file_name}')
            self.ui.LinePatientFirstName.setText(
                self.session.patient.get_first_name())
            self.ui.LinePatientLastName.setText(
                self.session.patient.get_last_name())
            self.slider_chart_prepare()
            self._chart_redraw_request()

            if self.r_window:
                if self.filtered:
                    self.r_window.data = self.session.buffer_filtered
                else:
                    self.r_window.data = self.session.buffer_main

                self.r_window.buffer_index = self.r_window.data.get_last_num()
                self.r_window._chart_redraw_request()
                self.r_window.event_redraw_charts()

            open_file(self.ui)

    def _control_panel(self):
        self.ui.WidgetControl.setMaximumWidth(
            180 if self.ui.actionControl_panel.isChecked() else 0)

    def _rhytms_window(self):
        if self.ui.actionRhytm_window.isChecked():
            if self.r_window is None: self.r_window = RhytmWindow(self)
            if self.filtered:
                self.r_window.data = self.session.buffer_filtered
            else:
                self.r_window.data = self.session.buffer_main
            self.r_window.update_ui()
            self.r_window.show()
            if not self.r_window.redraw_pause:
                self.r_window.event_redraw_charts()
            self.ui.CheckBoxRenew.setChecked(False)
        else:
            self.r_window.hide()
            self.ui.CheckBoxRenew.setChecked(True)

    def set_eeg_ch_names(self):
        channel_names = self.session.get_eeg_ch_names()
        self.ui.LabelCh0.setText(channel_names[0])
        self.ui.LabelCh1.setText(channel_names[1])
        self.ui.LabelCh2.setText(channel_names[2])
        self.ui.LabelCh3.setText(channel_names[3])

    def closeEvent(self, event):
        # Release all BB resources
        try:
            self.long_timer.stop()
            self.short_timer.stop()
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

        if self.r_window:
            self.r_window.hide()


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

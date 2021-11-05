import sys
from re import findall
from time import sleep

import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from PySide6 import QtCore, QtWidgets
from PySide6.QtCharts import (QCategoryAxis, QChart, QChartView, QLineSeries,
                              QValueAxis)
from PySide6.QtCore import QDateTime, QPointF, QTimer
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QProgressBar

from board import Board
from rhytmwindow import RhytmWindow
from session import Session
from settings import *
from ui_mainwindow import Ui_MainWindow
from utils import file_name_constructor, save_file, signal_filtering
from worker import Worker
from uiinteraction import *

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
        self.battery_value = 0
        self.chart_filtering_flag = True
        self.chart_detrend_flag = False
        self.redraw_charts_request = False
        self.chart_amp = self.ui.SliderAmplitude.value()
        self.charts = []

        self.rhytm_Window = None

        self.session = Session(buffer_size=10)
        self.set_eeg_ch_names()

        # /////////////////////////////////////////////////////////// CHART MAKE
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
        axis_t = self.update_time_axis(axis_t, QDateTime.currentDateTime())
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

    # ///////////////////////////////////////////////////////// Update TIME axis
    def update_time_axis(self, axis_t, start_time):
        # start_time = QDateTime.currentDateTime()
        end_time = start_time.addSecs(self.chart_duration)

        # print(start_time.toString('hh:mm:ss.zzz'),
        #       end_time.toString('hh:mm:ss.zzz'))
        # print()

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
        axis_t.append(end_time.toString('hh:mm:ss.zzz'),
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

        # Slider DURATION
        self.chart_duration = self.ui.SliderDuration.value()
        text = "Duration (sec): " + str(self.chart_duration)
        self.ui.LabelDuration.setText(text)
        axis_x = self.chart_view.chart().axisX()
        axis_x.setRange(0, self.chart_duration * SAMPLE_RATE)
        axis_t = self.chart_view.chart().axes()[2]
        axis_t.setRange(0, self.chart_duration * 1000)

        self.chart_buffers_update()

    def redraw_charts(self, data):
        start_tick = data[-2, 0]
        if start_tick != 0:
            start_time = QDateTime.fromMSecsSinceEpoch(int(start_tick * 1000))
        else:
            start_time = QDateTime.currentDateTime()

        # end_time = QDateTime.fromMSecsSinceEpoch(int(data[-2, -1] * 1000))
        # print(start_time.toString('hh:mm:ss.zzz'),
        #       end_time.toString('hh:mm:ss.zzz'), ' - original time')

        axis_t = self.chart_view.chart().axes()[2]
        self.update_time_axis(axis_t, start_time=start_time)
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
        params.timeout = BOARD_TIMEOUT
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
                connect_1(self.ui)
                exception = True
            else:
                exception = False

        if not exception:
            self.statusBar_main.setText('Connected.')
            connect_2(self.ui)

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
        self.chart_buffers_update()

        self.session.session_start(self.board)

        # INIT and START timer_long_events
        self.long_timer = QTimer()
        self.long_timer.timeout.connect(self.timer_long)
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

        start(self.ui)

    # ///////////////////////////////////////////////////////////////////// STOP
    def _stop_capture(self):
        self.chart_redraw_timer.stop()
        self.session.session_stop()
        self.long_timer.stop()
        self.board.stop_stream()
        if self.save_flag:
            self.timer_long()

        self.slider_chart_prepare()
        self.ui.SliderChart.setValue(self.ui.SliderChart.maximum())

        stop(self.ui)

    def _disconnect(self):
        # Release all BB resources
        if self.board.is_prepared():
            self.board.release_session()

        self.statusBar_main.setText('Disсonnected.')
        disconnect(self.ui)

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

    def _chart_redraw_request(self):
        if self.session.get_status():
            self.redraw_charts_request = True
        else:
            self.request_realisation()
            self._slider_value_cnd()

    def _slider_value_cnd(self):
        self.slider_chart_prepare()

        start_index = self.ui.SliderChart.value()
        end_index = start_index + self.chart_duration * SAMPLE_RATE

        # print(start_index, end_index, end_index - start_index)

        if self.chart_filtering_flag:
            data = self.session.buffer_filtered.get_buff_from(
                start_index, end_index)
        else:
            data = self.session.buffer_main.get_buff_from(
                start_index, end_index)

        self.chart_buffers_update()
        self.redraw_charts(data)

    def slider_chart_prepare(self):
        buff_size = self.session.buffer_filtered.get_last_num()
        slider_maximum = buff_size - self.chart_duration * SAMPLE_RATE
        if slider_maximum < 0:
            slider_maximum = 0
        self.ui.SliderChart.setMaximum(slider_maximum)

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

        if file_name != '':
            with open(file_name) as file_object:
                first_name = file_object.readline().rstrip().lstrip('#')
                last_name = file_object.readline().rstrip().lstrip('#')
                data = file_object.readline().rstrip().lstrip('#')
                time = file_object.readline().rstrip().lstrip('#')
                filtered_flag = file_object.readline().rstrip().lstrip('#')
                header = file_object.readline().rstrip().lstrip('#').split(
                    delimiter)

            filtered_flag = True if filtered_flag == 'filtered' else False

            table = np.loadtxt(file_name, delimiter=delimiter).T

            of_eeg_channel_names = [i.split(',')[0] for i in header[:-2]]

            self.session = Session(buffer_size=table.shape[1],
                                   first_name=first_name,
                                   last_name=last_name,
                                   eeg_channel_names=of_eeg_channel_names)

            if filtered_flag:
                self.session.buffer_filtered.add(table)
            else:
                self.session.add(table)

            del table

            self.ui.CheckBoxFilterChart.setEnabled(not filtered_flag)

            self.set_eeg_ch_names()

            file_name = file_name.replace('/', '\\')
            self.statusBar_main.setText(f'Open file: {file_name}')

            self.ui.LinePatientFirstName.setText(first_name)
            self.ui.LinePatientLastName.setText(last_name)

            self.slider_chart_prepare()
            self._chart_redraw_request()

            open_file(self.ui)

    def _control_panel(self):
        if self.ui.actionControl_panel.isChecked():
            self.ui.WidgetControl.setMaximumWidth(180)
        else:
            self.ui.WidgetControl.setMaximumWidth(0)

    def _rhytms_window(self):
        if self.ui.actionRhytm_window.isChecked():
            if self.rhytm_Window is None:
                self.rhytm_Window = RhytmWindow(self.ui)
            self.rhytm_Window.show()
        else:
            self.rhytm_Window.hide()

    def set_eeg_ch_names(self):
        self.channel_names = self.session.get_eeg_ch_names()
        self.ui.LabelCh0.setText(self.channel_names[0])
        self.ui.LabelCh1.setText(self.channel_names[1])
        self.ui.LabelCh2.setText(self.channel_names[2])
        self.ui.LabelCh3.setText(self.channel_names[3])

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
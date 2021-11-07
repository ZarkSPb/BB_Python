from PySide6 import QtCore
from PySide6.QtCharts import (QCategoryAxis, QChart, QChartView, QLineSeries,
                              QValueAxis)
from PySide6.QtCore import QDateTime, QPointF
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from settings import (MAX_CHART_SIGNAL_DURATION, NUM_CHANNELS, RHYTMS,
                      SAMPLE_RATE, SIGNAL_CLIPPING_SEC)
from ui_rhytmwindow import Ui_RhytmWindow
from utils import rhytm_constructor, signal_filtering
from session import Buffer
from rhytmwindow_uiinteraction import *


class RhytmWindow(QWidget):
    def __init__(self, parent):
        super(RhytmWindow, self).__init__()
        self.ui = Ui_RhytmWindow()
        self.ui.setupUi(self)

        self.parent = parent

        self.ui.SliderDuration.setMaximum(MAX_CHART_SIGNAL_DURATION)
        self.ui.SliderDuration.setValue(MAX_CHART_SIGNAL_DURATION)
        self.ui.SliderDuration.setSliderPosition(MAX_CHART_SIGNAL_DURATION)
        self.chart_duration = MAX_CHART_SIGNAL_DURATION
        self.chart_amp = self.ui.SliderAmplitude.value()
        self.redraw_charts_request = False
        self.redraw_pause = False
        self.buffer_index = self.parent.session.buffer_main.get_last_num()
        self.rhytms = RHYTMS.copy()
        self.channel_names = self.parent.session.get_eeg_ch_names()

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
        axis_c.setTruncateLabels(False)
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

        self.event_redraw_charts()

    def update_ui(self):
        self.ui.ButtonStart.setEnabled(self.parent.ui.ButtonStart.isEnabled())
        self.ui.ButtonStop.setEnabled(self.parent.ui.ButtonStop.isEnabled())

        if self.parent.session.get_status():
            if self.redraw_pause:
                pause(self.ui)
            else:
                resume(self.ui)
        else:
            open_session_norun(self.ui)

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

    # ///////////////////////////////////////////////////////// Update TIME axis
    def update_time_axis(self, axis_t, start_time):
        end_time = start_time.addSecs(self.chart_duration)
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

    def chart_buffers_update(self):
        self.chart_buffers = []
        for i in range(NUM_CHANNELS):
            self.chart_buffers.append([
                QPointF(
                    x, self.chart_amp +
                    (NUM_CHANNELS - 1 - i) * 2 * self.chart_amp)
                for x in range(self.chart_duration * SAMPLE_RATE)
            ])

    def _chart_redraw_request(self):
        if self.parent.session.get_status() and not self.redraw_pause:
            self.redraw_charts_request = True
        else:
            self.request_realisation()
            self._slider_value_cnd()

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

    def _rhytms_param_cnd(self):
        rhytms_param_cnd(self.ui)

        self.rhytms['delta'] = [
            self.ui.SpinBox1_1.value(),
            self.ui.SpinBox1_2.value(),
            self.ui.CheckBox1.isChecked()
        ]
        self.rhytms['theta'] = [
            self.ui.SpinBox2_1.value(),
            self.ui.SpinBox2_2.value(),
            self.ui.CheckBox2.isChecked()
        ]
        self.rhytms['alpha'] = [
            self.ui.SpinBox3_1.value(),
            self.ui.SpinBox3_2.value(),
            self.ui.CheckBox3.isChecked()
        ]
        self.rhytms['betha'] = [
            self.ui.SpinBox4_1.value(),
            self.ui.SpinBox4_2.value(),
            self.ui.CheckBox4.isChecked()
        ]
        self.rhytms['gamma'] = [
            self.ui.SpinBox5_1.value(),
            self.ui.SpinBox5_2.value(),
            self.ui.CheckBox5.isChecked()
        ]

        self._slider_value_cnd()

    def _reset(self):
        self.ui.SpinBox1_1.setValue(RHYTMS['delta'][0])
        self.ui.SpinBox2_1.setValue(RHYTMS['theta'][0])
        self.ui.SpinBox3_1.setValue(RHYTMS['alpha'][0])
        self.ui.SpinBox4_1.setValue(RHYTMS['betha'][0])
        self.ui.SpinBox5_1.setValue(RHYTMS['gamma'][0])

        self.ui.SpinBox1_2.setValue(RHYTMS['delta'][1])
        self.ui.SpinBox2_2.setValue(RHYTMS['theta'][1])
        self.ui.SpinBox3_2.setValue(RHYTMS['alpha'][1])
        self.ui.SpinBox4_2.setValue(RHYTMS['betha'][1])
        self.ui.SpinBox5_2.setValue(RHYTMS['gamma'][1])

        self._rhytms_param_cnd()

    def _pause(self):
        self.redraw_pause = True
        self.buffer_index = self.parent.session.buffer_main.get_last_num()
        self.slider_chart_prepare()
        self.ui.SliderChart.setValue(self.ui.SliderChart.maximum())
        pause(self.ui)

    def _resume(self):
        self.redraw_pause = False
        resume(self.ui)

    def _start(self):
        if not self.parent.session.get_status():
            self.parent._start_capture()
        if self.redraw_pause:
            self._resume()
        self.chart_buffers_update()
        start(self.ui)

    def _stop(self):
        if self.parent.session.get_status():
            self.parent._stop_capture()
        self._pause()
        stop(self.ui)

    def _slider_value_cnd(self):
        self.slider_chart_prepare()

        start_index = (self.ui.SliderChart.value() -
                       SIGNAL_CLIPPING_SEC * SAMPLE_RATE)
        if start_index < 0:
            start_index = 0

        end_index = start_index + (self.chart_duration +
                                   SIGNAL_CLIPPING_SEC) * SAMPLE_RATE

        if end_index > self.buffer_index:
            end_index = self.buffer_index

        data = self.parent.session.buffer_main.get_buff_from(
            start_index, end_index)

        if data.shape[1] > 0:
            for channel in range(NUM_CHANNELS):
                signal_filtering(data[channel], filtering=False)
                data[channel] = rhytm_constructor(data[channel], self.rhytms)

            data = data[:, SIGNAL_CLIPPING_SEC * SAMPLE_RATE:]
            if data.shape[1] > 0:
                self.redraw_charts(data)

        # self.chart_buffers_update()
        # self.redraw_charts(data)

    def slider_chart_prepare(self):
        buff_size = self.buffer_index

        slider_max = buff_size - (self.chart_duration +
                                  SIGNAL_CLIPPING_SEC) * SAMPLE_RATE
        slider_max = 0 if slider_max == 0 else slider_max

        slider_min = SIGNAL_CLIPPING_SEC * SAMPLE_RATE
        slider_min = slider_max if slider_min > slider_max else slider_min

        self.ui.SliderChart.setMinimum(slider_min)
        self.ui.SliderChart.setMaximum(slider_max)

    def redraw_charts(self, data):
        start_tick = data[-2, 0]
        if start_tick != 0:
            start_time = QDateTime.fromMSecsSinceEpoch(int(start_tick * 1000))
        else:
            start_time = QDateTime.currentDateTime()

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
            self.event_redraw_charts()

    def event_redraw_charts(self):
        data = self.parent.session.buffer_main.get_buff_last(
            (self.chart_duration + SIGNAL_CLIPPING_SEC) * SAMPLE_RATE)

        if data.shape[1] > 0:
            for channel in range(NUM_CHANNELS):
                signal_filtering(data[channel], filtering=False)
                data[channel] = rhytm_constructor(data[channel], self.rhytms)

            data = data[:, SIGNAL_CLIPPING_SEC * SAMPLE_RATE:]
            if data.shape[1] > 0:
                self.redraw_charts(data)

    def closeEvent(self, event):
        self.parent.ui.actionRhytm_window.setChecked(False)

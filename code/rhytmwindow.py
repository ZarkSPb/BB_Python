import brainflow
from brainflow.data_filter import (DataFilter, DetrendOperations,
                                   WindowFunctions)

from PySide6.QtCharts import QLineSeries
from PySide6.QtCore import QDateTime
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

import chart as ch
from chart_analize import ChartAn
from chart_filtered import ChartFiltered
import rhytmwindow_uiinteraction as ui
from settings import MAX_CHART_SIGNAL_DURATION, RHYTMS, SIGNAL_CLIPPING_SEC, RHYTMS_ANALISE
from ui_rhytmwindow import Ui_RhytmWindow
from utils import rhytm_constructor, signal_filtering
import time
from session import Buffer
import numpy as np


class RhytmWindow(QWidget):
    def __init__(self, parent):
        super(RhytmWindow, self).__init__()
        self.ui = Ui_RhytmWindow()
        self.ui.setupUi(self)

        self.parent = parent

        s_rate = self.parent.session.get_sample_rate()
        ch_names = self.parent.session.get_eeg_ch_names()
        ch_num = len(ch_names)

        self.ui.SliderDuration.setMaximum(MAX_CHART_SIGNAL_DURATION)
        self.ui.SliderDuration.setValue(MAX_CHART_SIGNAL_DURATION)
        self.ui.SliderDuration.setSliderPosition(MAX_CHART_SIGNAL_DURATION)
        self.chart_duration = MAX_CHART_SIGNAL_DURATION
        self.redraw_charts_request = False
        self.chart_amp = self.ui.SliderAmplitude.value()
        self.redraw_pause = False
        self.rhytms = RHYTMS.copy()
        self.ui.SliderChart.setMinimum(SIGNAL_CLIPPING_SEC * s_rate)
        self.data = None
        self.buffer_index = 0

        self.last_analyse_index = 0

        # //////////////////////////////////////////////////////////////// CHART
        chart, axis_x, axis_y = ch.init(self.parent.session, self.chart_amp,
                                        ch_num)
        self.serieses = []
        self.chart_buffers = ch.buffers_update(self.chart_amp, ch_names,
                                               self.chart_duration, s_rate)
        for i in range(ch_num):
            series = QLineSeries()
            series.append(self.chart_buffers[i])
            self.serieses.append(series)
            chart.addSeries(self.serieses[-1])
            self.serieses[-1].attachAxis(axis_x)
            self.serieses[-1].attachAxis(axis_y)
        # //////////////////////////////////////////////////// Chart view create
        self.chart_view = ChartFiltered(chart, self._chart_filtered_dclick)
        self.chart_view.setRenderHint(QPainter.Antialiasing, True)
        self.ui.LayoutCharts.addWidget(self.chart_view)

        self.chart_view_analise = ChartAn(self.parent.session,
                                          self._chart_rhytm_dclick)

        self.ui.splitter.setSizes((1, 0))
        # self.ui.radioButton_1.setChecked(True)

    def update_ui(self):
        self.buffer_index = self.data.get_last_num()

        self.ui.ButtonStart.setEnabled(self.parent.ui.ButtonStart.isEnabled())
        self.ui.ButtonStop.setEnabled(self.parent.ui.ButtonStop.isEnabled())

        if self.parent.session.get_status():
            if self.redraw_pause:
                ui.pause(self.ui)
            else:
                ui.resume(self.ui)
        else:
            ui.open_session_norun(self.ui)

    def _chart_rhytm_dclick(self):
        size = self.ui.splitter.sizes()[0]
        if size == 0:
            self.ui.splitter.setSizes((500, 500))
        else:
            self.ui.splitter.setSizes((0, 1))

    def _chart_filtered_dclick(self):
        if self.ui.radioButton_off.isChecked():
            self.ui.radioButton_1.setChecked(True)
            self._rhytms_on()
        else:
            size = self.ui.splitter.sizes()[1]
            if size == 0:
                self.ui.splitter.setSizes((500, 500))
            else:
                self.ui.splitter.setSizes((1, 0))

    def _chart_redraw_request(self):
        if self.parent.session.get_status() and not self.redraw_pause:
            self.redraw_charts_request = True
        else:
            self.request_realisation()
            self._slider_value_cnd()

    def request_realisation(self):
        ch_names = self.parent.session.get_eeg_ch_names()
        s_rate = self.parent.session.get_sample_rate()
        ch_num = len(ch_names)

        # Slider AMPLITUDE
        self.chart_amp = self.ui.SliderAmplitude.value()
        text = "Amplitude (uV): " + str(self.chart_amp)
        self.ui.LabelAmplitude.setText(text)
        self.chart_view.chart().axisY().setRange(0, 8 * self.chart_amp)
        axis_c = self.chart_view.chart().axes()[3]
        ch.update_channels_axis(axis_c, self.parent.session, self.chart_amp,
                                ch_num)

        # Slider DURATION
        self.chart_duration = self.ui.SliderDuration.value()
        text = "Duration (sec): " + str(self.chart_duration)
        self.ui.LabelDuration.setText(text)
        axis_x = self.chart_view.chart().axisX()
        axis_x.setRange(0, self.chart_duration * s_rate)
        axis_t = self.chart_view.chart().axes()[2]
        axis_t.setRange(0, self.chart_duration * 1000)

        self.chart_buffers = ch.buffers_update(self.chart_amp, ch_names,
                                               self.chart_duration, s_rate)

    def _rhytms_param_cnd(self):
        self.rhytms = ui.rhytms_param_cnd(self.ui)
        self._slider_value_cnd()

    def _reset(self):
        ui.reset(self.ui, RHYTMS)
        self._rhytms_param_cnd()

    def _pause(self):
        self.redraw_pause = True
        self.buffer_index = self.parent.session.buffer_main.get_last_num()
        self.slider_chart_prepare()
        self.ui.SliderChart.setValue(self.ui.SliderChart.maximum())
        ui.pause(self.ui)

    def _resume(self):
        self.redraw_pause = False
        ui.resume(self.ui)

    def _start(self):
        if not self.parent.session.get_status(): self.parent._start_capture()

    def start(self):
        ch_name = self.parent.session.get_eeg_ch_names()
        s_rate = self.parent.session.get_sample_rate()
        if self.redraw_pause: self._resume()
        self.chart_buffers = ch.buffers_update(self.chart_amp, ch_name,
                                               self.chart_duration, s_rate)

        self.last_analyse_index = 0
        self.chart_view_analise.buffer_clear()

        ui.start(self.ui)

    def _stop(self):
        if self.parent.session.get_status(): self.parent._stop_capture()
        self._pause()
        ui.stop(self.ui)

    def _slider_value_cnd(self):
        s_rate = self.parent.session.get_sample_rate()
        ch_names = self.parent.session.get_eeg_ch_names()

        self.slider_chart_prepare()

        start_index = (self.ui.SliderChart.value() -
                       SIGNAL_CLIPPING_SEC * s_rate)
        if start_index < 0: start_index = 0

        end_index = start_index + (self.chart_duration +
                                   SIGNAL_CLIPPING_SEC) * s_rate
        if end_index > self.buffer_index: end_index = self.buffer_index

        data = self.data.get_buff_from(start_index, end_index)

        ch_num = len(ch_names)
        if data.shape[1] > 0:
            for channel in range(ch_num):
                signal_filtering(data[channel], s_rate, filtering=False)
                data[channel] = rhytm_constructor(data[channel], self.rhytms,
                                                  s_rate)
            data = data[:, SIGNAL_CLIPPING_SEC * s_rate:]

        if data.shape[1] > 0: self.redraw_charts(data)
        else:
            start_time = QDateTime.currentDateTime()
            axis_t = self.chart_view.chart().axes()[2]
            ch.update_time_axis(self.chart_duration,
                                axis_t,
                                start_time=start_time)
            self.chart_buffers = ch.buffers_update(self.chart_amp, ch_names,
                                                   self.chart_duration, s_rate)
            for channel in range(ch_num):
                self.serieses[channel].replace(self.chart_buffers[channel])

    def slider_chart_prepare(self):
        s_rate = self.parent.session.get_sample_rate()

        slider_min = self.ui.SliderChart.minimum()
        slider_max = self.buffer_index - (self.chart_duration) * s_rate
        if slider_max < slider_min: slider_max = slider_min

        self.ui.SliderChart.setMaximum(slider_max)

    def redraw_charts(self, data):
        start_tick = data[-2, 0]
        if start_tick != 0:
            start_time = QDateTime.fromMSecsSinceEpoch(int(start_tick * 1000))
        else:
            start_time = QDateTime.currentDateTime()

        axis_t = self.chart_view.chart().axes()[2]
        ch.update_time_axis(self.chart_duration, axis_t, start_time=start_time)
        ch_num = len(self.parent.session.get_eeg_ch_names())
        for channel in range(ch_num):
            r_data = data[channel]
            for i in range(r_data.shape[0]):
                self.chart_buffers[channel][i].setY(r_data[i] +
                                                    self.chart_amp +
                                                    (ch_num - 1 - channel) *
                                                    2 * self.chart_amp)
            self.serieses[channel].replace(self.chart_buffers[channel])

        if self.redraw_charts_request:
            self.redraw_charts_request = False
            self.request_realisation()
            self.event_redraw_charts()

    def event_redraw_charts(self):
        s_rate = self.parent.session.get_sample_rate()

        data = self.data.get_buff_last(
            (self.chart_duration + SIGNAL_CLIPPING_SEC) * s_rate)

        ch_num = len(self.parent.session.get_eeg_ch_names())
        if data.shape[1] > 0:
            for channel in range(ch_num):
                signal_filtering(data[channel], s_rate, filtering=False)
                data[channel] = rhytm_constructor(data[channel], self.rhytms,
                                                  s_rate)

            data = data[:, SIGNAL_CLIPPING_SEC * s_rate:]
            if data.shape[1] > 0: self.redraw_charts(data)

    def new_analyze_data(self):
        s_rate = self.parent.session.get_sample_rate()
        ch_names = self.parent.session.get_eeg_ch_names()
        ch_num = len(ch_names)
        nfft = DataFilter.get_nearest_power_of_two(s_rate)
        data_num = self.data.get_last_num()

        def cycle_buff(datas):
            buff_result = []
            for data in datas:
                DataFilter.detrend(data, DetrendOperations.LINEAR.value)
                psd = DataFilter.get_psd_welch(
                    data, nfft, nfft // 2, s_rate,
                    WindowFunctions.BLACKMAN_HARRIS.value)
                buff = []
                for rhytm in RHYTMS_ANALISE:
                    buff.append(
                        DataFilter.get_band_power(psd, RHYTMS[rhytm][0],
                                                  RHYTMS[rhytm][1]))

                # buff[0] = buff[0] / 2 # <----------------------------------------------------------------

                coeff = 100 / sum(buff)
                buff_result.extend([int(i * coeff) for i in buff])
            return buff_result

        # timestart = time.time_ns()

        buff_for_send = []
        while data_num - self.last_analyse_index >= nfft:
            datas = self.data.get_buff_from(self.last_analyse_index,
                                            self.last_analyse_index +
                                            nfft)[:ch_num]
            if datas[-1, -1] != 0:
                buff_for_send.append(cycle_buff(datas))
            self.last_analyse_index += s_rate

        # timeend = time.time_ns()
        # print((timeend - timestart) // 1000)

        if len(buff_for_send) > 0:
            self.buffer_rhytms.add(np.asarray(buff_for_send).T)
            self.chart_view_analise.buffers_add(buff_for_send)
            self.chart_view_analise.chart_renew()

    # //////////////////////////////////////////////////////////// CHART ANALYSE
    def _rhytms_on(self):
        ch_num = len(self.parent.session.get_eeg_ch_names())
        self.buffer_rhytms = Buffer(buffer_size=120,
                                    channels_num=ch_num * len(RHYTMS_ANALISE))

        self.ui.LayoutChartsAnalyse.addWidget(self.chart_view_analise)
        self.ui.splitter.setSizes((500, 500))

    def _period_on(self):
        pass

    def _pattern_on(self):
        pass

    def _corellation_on(self):
        pass

    def _relax_on(self):
        pass

    def _off(self):
        self.ui.splitter.setSizes((1, 0))

    def closeEvent(self, event):
        self.parent.ui.actionRhytm_window.setChecked(False)

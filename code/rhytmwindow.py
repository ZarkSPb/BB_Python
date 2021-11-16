from PySide6.QtCharts import QChartView, QLineSeries
from PySide6.QtCore import QDateTime
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

import chart as ch
from rhytmwindow_uiinteraction import *
from settings import MAX_CHART_SIGNAL_DURATION, RHYTMS, SIGNAL_CLIPPING_SEC
from ui_rhytmwindow import Ui_RhytmWindow
from utils import rhytm_constructor, signal_filtering
from chart_analize import ChartAn


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
        self.redraw_charts_request = False
        self.chart_amp = self.ui.SliderAmplitude.value()
        self.redraw_pause = False
        self.rhytms = RHYTMS.copy()
        self.ui.SliderChart.setMinimum(SIGNAL_CLIPPING_SEC *
                                       self.parent.session.get_sample_rate())
        self.data = None
        self.buffer_index = 0

        # //////////////////////////////////////////////////////////////// CHART
        ch_num = len(self.parent.session.get_eeg_ch_names())
        chart, axis_x, axis_y = ch.init(self.parent.session, self.chart_amp,
                                        ch_num)
        self.serieses = []
        self.chart_buffers = ch.buffers_update(
            self.chart_amp, self.parent.session.get_eeg_ch_names(),
            self.chart_duration, self.parent.session.get_sample_rate())
        for i in range(ch_num):
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

        # # //////////////////////////////////////////////////////// CHART ANALYSE
        # ch_num = len(self.parent.session.get_eeg_ch_names())
        # chart, axis_x, axis_y = ch.init(self.parent.session, self.chart_amp,
        #                                 ch_num)
        # self.serieses_analise = []
        # self.chart_buffers_analise = ch.buffers_update(
        #     self.chart_amp, self.parent.session.get_eeg_ch_names(),
        #     self.chart_duration, self.parent.session.get_sample_rate())
        # for i in range(ch_num):
        #     series = QLineSeries()
        #     series.append(self.chart_buffers[i])
        #     self.serieses_analise.append(series)
        #     chart.addSeries(self.serieses[-1])
        #     self.serieses_analise[-1].attachAxis(axis_x)
        #     self.serieses_analise[-1].attachAxis(axis_y)
        # # //////////////////////////////////////////////////// Chart view create
        # self.chart_view_analise = QChartView(chart)
        # self.chart_view_analise.setRenderHint(QPainter.Antialiasing, True)
        # self.ui.LayoutChartsAnalyse.addWidget(self.chart_view_analise)

        self.chart_view_analise = ChartAn(self.parent.session)
        self.ui.LayoutChartsAnalyse.addWidget(self.chart_view_analise)

        # self.ui.splitter.setSizes((1, 0))

    def update_ui(self):
        self.buffer_index = self.data.get_last_num()

        self.ui.ButtonStart.setEnabled(self.parent.ui.ButtonStart.isEnabled())
        self.ui.ButtonStop.setEnabled(self.parent.ui.ButtonStop.isEnabled())

        if self.parent.session.get_status():
            if self.redraw_pause:
                pause(self.ui)
            else:
                resume(self.ui)
        else:
            open_session_norun(self.ui)

    def _chart_redraw_request(self):
        if self.parent.session.get_status() and not self.redraw_pause:
            self.redraw_charts_request = True
        else:
            self.request_realisation()
            self._slider_value_cnd()

    def request_realisation(self):
        ch_num = len(self.parent.session.get_eeg_ch_names())

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
        axis_x.setRange(
            0, self.chart_duration * self.parent.session.get_sample_rate())
        axis_t = self.chart_view.chart().axes()[2]
        axis_t.setRange(0, self.chart_duration * 1000)

        self.chart_buffers = ch.buffers_update(
            self.chart_amp, self.parent.session.get_eeg_ch_names(),
            self.chart_duration, self.parent.session.get_sample_rate())

    def _rhytms_param_cnd(self):
        self.rhytms = rhytms_param_cnd(self.ui)
        self._slider_value_cnd()

    def _reset(self):
        reset(self.ui, RHYTMS)
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
        if not self.parent.session.get_status(): self.parent._start_capture()
        if self.redraw_pause: self._resume()
        self.chart_buffers = ch.buffers_update(
            self.chart_amp, self.parent.session.get_eeg_ch_names(),
            self.chart_duration, self.parent.session.get_sample_rate())
        start(self.ui)

    def _stop(self):
        if self.parent.session.get_status(): self.parent._stop_capture()
        self._pause()
        stop(self.ui)

    def _slider_value_cnd(self):
        self.slider_chart_prepare()

        start_index = (
            self.ui.SliderChart.value() -
            SIGNAL_CLIPPING_SEC * self.parent.session.get_sample_rate())
        if start_index < 0: start_index = 0

        end_index = start_index + (self.chart_duration + SIGNAL_CLIPPING_SEC
                                   ) * self.parent.session.get_sample_rate()
        if end_index > self.buffer_index: end_index = self.buffer_index

        data = self.data.get_buff_from(start_index, end_index)

        ch_num = len(self.parent.session.get_eeg_ch_names())
        if data.shape[1] > 0:
            for channel in range(ch_num):
                signal_filtering(data[channel],
                                 self.parent.session.get_sample_rate(),
                                 filtering=False)
                data[channel] = rhytm_constructor(
                    data[channel], self.rhytms,
                    self.parent.session.get_sample_rate())
            data = data[:, SIGNAL_CLIPPING_SEC *
                        self.parent.session.get_sample_rate():]

        if data.shape[1] > 0: self.redraw_charts(data)
        else:
            start_time = QDateTime.currentDateTime()
            axis_t = self.chart_view.chart().axes()[2]
            ch.update_time_axis(self.chart_duration,
                                axis_t,
                                start_time=start_time)
            self.chart_buffers = ch.buffers_update(
                self.chart_amp, self.parent.session.get_eeg_ch_names(),
                self.chart_duration, self.parent.session.get_sample_rate())
            for channel in range(ch_num):
                self.serieses[channel].replace(self.chart_buffers[channel])

    def slider_chart_prepare(self):
        slider_min = self.ui.SliderChart.minimum()
        slider_max = self.buffer_index - (
            self.chart_duration) * self.parent.session.get_sample_rate()
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
        data = self.data.get_buff_last(
            (self.chart_duration + SIGNAL_CLIPPING_SEC) *
            self.parent.session.get_sample_rate())

        ch_num = len(self.parent.session.get_eeg_ch_names())
        if data.shape[1] > 0:
            for channel in range(ch_num):
                signal_filtering(data[channel],
                                 self.parent.session.get_sample_rate(),
                                 filtering=False)
                data[channel] = rhytm_constructor(
                    data[channel], self.rhytms,
                    self.parent.session.get_sample_rate())

            data = data[:, SIGNAL_CLIPPING_SEC *
                        self.parent.session.get_sample_rate():]
            if data.shape[1] > 0: self.redraw_charts(data)

    def closeEvent(self, event):
        self.parent.ui.actionRhytm_window.setChecked(False)

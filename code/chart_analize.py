from PySide6.QtCharts import QChartView, QChart, QLineSeries, QValueAxis, QCategoryAxis
from PySide6 import QtCore
from PySide6.QtCore import QDateTime, QPointF
from settings import RHYTMS, RHYTMS_ANALISE, RHYTMS_COLOR


class ChartAn(QChartView):
    def __init__(self, ch_names, maximize_func, start_time):
        chart = QChart()
        # SUPER INIT
        super(ChartAn, self).__init__(chart)

        self.ch_names = ch_names
        self.ch_num = len(self.ch_names)
        self.tick_nums = 5
        self.chart_percent_max = 100
        self.chart_duration_min = 0
        self.current_index = 0
        self.maximize_func = maximize_func
        self.start_time = start_time

        chart.legend().setVisible(True)

        # /////////////////////////////////////////////////////////////// axis_x
        self.axis_x = QValueAxis()
        self.axis_x.setTickType(QValueAxis.TicksDynamic)
        self.axis_x.setTickInterval(60)  # 60 second in minute
        self.axis_x.setTickCount(self.chart_duration_min + 1)
        self.axis_x.setMinorTickCount(3)
        self.axis_x.setLabelsVisible(False)
        chart.addAxis(self.axis_x, QtCore.Qt.AlignTop)
        # /////////////////////////////////////////////////////////////// axis_c
        axis_c = QCategoryAxis()
        axis_c.setGridLineVisible(False)
        axis_c.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        axis_c.setTruncateLabels(False)
        self.update_channels_axis(axis_c, self.ch_names,
                                  self.chart_percent_max)
        chart.addAxis(axis_c, QtCore.Qt.AlignLeft)
        # /////////////////////////////////////////////////////////////// axis_t
        self.axis_t = QCategoryAxis()
        self.axis_t.rangeChanged.connect(self.range_cnd)
        self.axis_t.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        self.axis_t.setTruncateLabels(False)
        chart.addAxis(self.axis_t, QtCore.Qt.AlignBottom)
        # /////////////////////////////////////////////////////////////// axis_y
        axis_y = QValueAxis()
        axis_y.setRange(0, self.ch_num * self.chart_percent_max)
        axis_y.setTickCount(self.ch_num + 1)
        axis_y.setGridLineColor('black')
        axis_y.setMinorTickCount(self.tick_nums - 1)
        axis_y.setLabelsVisible(False)
        chart.addAxis(axis_y, QtCore.Qt.AlignRight)

        # ////////////////////////////////////////////////////////////// BUFFERS
        self.serieses = []
        self.buffer_clear()

        rhytms_name = list(RHYTMS.keys())
        rhytms_analise_num = len(RHYTMS_ANALISE)
        for series_num in range(self.ch_num * rhytms_analise_num):
            series = QLineSeries()
            series.append(self.chart_buffers[series_num])
            self.serieses.append(series)
            chart.addSeries(self.serieses[-1])
            self.serieses[-1].attachAxis(self.axis_x)
            self.serieses[-1].attachAxis(axis_y)

            if series_num < rhytms_analise_num:
                self.serieses[-1].setName(rhytms_name[series_num])
            else:
                self.serieses[-1].setMarkerSize(50)

            self.serieses[-1].setColor(RHYTMS_COLOR[series_num %
                                                    rhytms_analise_num])

        # /////////////////////////////// remove unnecessary markers from legend
        for marker in chart.legend().markers()[rhytms_analise_num:]:
            marker.setVisible(False)

        # self.chart_renew()

    # //////////////////////////////////////////////////////////// RANGE CHANGED
    def range_cnd(self, min, max):
        self.chart_duration_min = int((max - min) // 60)
        self.axis_x.setRange(0, self.chart_duration_min * 60)
        self.update_time_axis()

    # ///////////////////////////////////////////////////// Update CHANNELS axis
    def update_channels_axis(self, axis_c, ch_names, amp):
        num_ch = len(ch_names)
        axis_range_max = num_ch * amp
        axis_c.setRange(0, axis_range_max)
        interval = amp // self.tick_nums

        # clear ticks
        labels = axis_c.categoriesLabels()
        for i in range(len(labels)):
            axis_c.remove(labels[i])

        # Add new ticks
        for i, ch_name in enumerate(ch_names[num_ch - 1::-1]):
            start = i * amp
            axis_c.append(f'--{ch_name}--', start)
            for j in range(interval, amp, interval):
                axis_c.append(i * ' ' + str(j), j + start)
        axis_c.append(str(amp), axis_range_max)

    def update_time_axis(self):
        if self.start_time:
            end_time = self.start_time.addSecs(self.chart_duration_min * 60)
            offset = 60 - int(self.start_time.toString('ss'))

            self.axis_x.setTickAnchor(offset)

            labels = self.axis_t.categoriesLabels()
            for label in labels:
                self.axis_t.remove(label)

            self.axis_t.append(self.start_time.toString('hh:mm:ss'), 0)
            self.axis_t.append(' ', offset)

            for i in range(1, self.chart_duration_min - 1):
                shifted_time = self.start_time.addSecs(i * 60 + offset)
                time_string = shifted_time.toString('mm')
                self.axis_t.append(time_string, offset + i * 60)

            self.axis_t.append('  ',
                               (self.chart_duration_min - 1) * 60 + offset)
            self.axis_t.append(end_time.toString('hh:mm:ss'),
                               self.chart_duration_min * 60)

    # //////////////////////////////////////////////////////////// BUFFER UPDATE
    def buffers_add(self, new_data):
        datas = len(new_data)
        if datas > 0: rhytms = len(new_data[0])
        rhytms_analise_num = len(RHYTMS_ANALISE)

        if datas > 0 and rhytms == len(self.chart_buffers):
            for data in new_data:
                channel = 0
                for i in range(rhytms):
                    if i % rhytms_analise_num == 0 and i > 0: channel += 1

                    new_point = QPointF(
                        self.current_index,
                        data[i] + channel * self.chart_percent_max)
                    self.chart_buffers[i].append(new_point)

                self.current_index += 1

    # ////////////////////////////////////////////////////////////// CHART RENEW
    def chart_renew(self):
        buff_len = len(self.chart_buffers[0])
        if self.chart_duration_min * 60 < buff_len:
            self.chart_duration_min = 1 + buff_len // 60
        self.axis_t.setRange(0, self.chart_duration_min * 60)

        rhytms_analise_num = len(RHYTMS_ANALISE)
        for i in range(self.ch_num * rhytms_analise_num):
            self.serieses[i].replace(self.chart_buffers[i])

    # ///////////////////////////////////////////////////////////// BUFFER CLEAR
    def buffer_clear(self):
        rhytms_analise_num = len(RHYTMS_ANALISE)
        self.current_index = 0
        self.chart_buffers = [[]
                              for i in range(self.ch_num * rhytms_analise_num)]
        self.chart_duration_min = 0
        # self.start_time = QDateTime.currentDateTime()

        self.axis_t.setRange(0, 60)
        self.range_cnd(0, 60)

    def mouseDoubleClickEvent(self, event):
        self.maximize_func()

    def set_start_time(self, start_time):
        self.start_time = start_time
        self.update_time_axis()

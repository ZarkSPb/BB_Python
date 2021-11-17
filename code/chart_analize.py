from PySide6.QtCharts import QChartView, QChart, QLineSeries, QValueAxis, QCategoryAxis
from PySide6 import QtCore
from PySide6.QtCore import QDateTime, QPointF


class ChartAn(QChartView):
    def __init__(self, session):
        chart = QChart()
        # SUPER INIT
        super(ChartAn, self).__init__(chart)

        self.ch_names = session.get_eeg_ch_names()
        self.ch_num = len(self.ch_names)
        self.tick_nums = 5
        self.chart_percent_max = 100
        self.chart_duration_min = 5
        self.rhytm_num = 5
        self.current_index = 0

        chart.legend().setVisible(False)

        # /////////////////////////////////////////////////////////////// axis_x
        axis_x = QValueAxis()
        axis_x.setTickType(QValueAxis.TicksDynamic)
        axis_x.setTickInterval(60)  # 60 second in minute
        axis_x.setRange(0, self.chart_duration_min * 60)
        axis_x.setTickCount(self.chart_duration_min + 1)
        axis_x.setMinorTickCount(3)
        axis_x.setLabelsVisible(False)
        chart.addAxis(axis_x, QtCore.Qt.AlignTop)
        # /////////////////////////////////////////////////////////////// axis_c
        axis_c = QCategoryAxis()
        axis_c.setGridLineVisible(False)
        axis_c.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        axis_c.setTruncateLabels(False)
        self.update_channels_axis(axis_c, self.ch_names,
                                  self.chart_percent_max)
        chart.addAxis(axis_c, QtCore.Qt.AlignLeft)
        # /////////////////////////////////////////////////////////////// axis_t
        axis_t = QCategoryAxis()
        axis_t.setRange(0, self.chart_duration_min * 60)
        axis_t.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        axis_t.setTruncateLabels(False)
        axis_t = self.update_time_axis(self.chart_duration_min, axis_t,
                                       QDateTime.currentDateTime(), axis_x)
        chart.addAxis(axis_t, QtCore.Qt.AlignBottom)
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
        self.chart_buffers = [[] for i in range(self.ch_num * self.rhytm_num)]

        for chart_num in range(self.ch_num * self.rhytm_num):
            series = QLineSeries()
            series.append(self.chart_buffers[chart_num])
            self.serieses.append(series)
            chart.addSeries(self.serieses[-1])
            self.serieses[-1].attachAxis(axis_x)
            self.serieses[-1].attachAxis(axis_y)

        for i in range(self.ch_num * self.rhytm_num):
            self.serieses[i].replace(self.chart_buffers[i])

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

    def update_time_axis(self, chart_duration, axis_t, start_time, axis_x):
        end_time = start_time.addSecs(chart_duration * 60)
        offset = 60 - int(start_time.toString('ss'))

        axis_x.setTickAnchor(offset)

        labels = axis_t.categoriesLabels()
        for label in labels:
            axis_t.remove(label)

        axis_t.append(start_time.toString('hh:mm:ss'), 0)
        axis_t.append(' ', offset)

        for i in range(1, chart_duration - 1):
            shifted_time = start_time.addSecs(i * 60 + offset)
            time_string = shifted_time.toString('mm')
            axis_t.append(time_string, offset + i * 60)

        axis_t.append('  ', (chart_duration - 1) * 60 + offset)
        axis_t.append(end_time.toString('hh:mm:ss'), chart_duration * 60)

        return axis_t

    # //////////////////////////////////////////////////////////// BUFFER UPDATE
    def buffers_add(self, new_data):
        len_data = len(new_data)

        print()

        if len_data == len(self.chart_buffers):
            channel = 0
            for i in range(len_data):

                print(channel)

                new_point = QPointF(
                    self.current_index,
                    new_data[i] + channel * self.chart_percent_max)
                self.chart_buffers[i].append(new_point)

                if i % self.rhytm_num == 0 and i > 0: channel += 1

            self.current_index += 1
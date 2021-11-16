from PySide6.QtCharts import QChartView, QChart, QValueAxis, QCategoryAxis
from PySide6 import QtCore
from PySide6.QtCore import QDateTime


class ChartAn(QChartView):
    def __init__(self, session):
        self.ch_names = session.get_eeg_ch_names()
        self.num_ch = len(self.ch_names)
        self.tick_nums = 5
        self.percent = 100
        self.chart_duration_min = 5

        chart = QChart()
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
        # /////////////////////////////////////////////////////////////// axis_y
        axis_y = QValueAxis()
        axis_y.setRange(0, self.num_ch * self.percent)
        axis_y.setTickCount(self.num_ch + 1)
        axis_y.setMinorTickCount(self.tick_nums - 1)
        axis_y.setLabelsVisible(False)
        chart.addAxis(axis_y, QtCore.Qt.AlignRight)
        # /////////////////////////////////////////////////////////////// axis_c
        axis_c = QCategoryAxis()
        axis_c.setGridLineVisible(False)
        axis_c.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        axis_c.setTruncateLabels(False)
        self.update_channels_axis(axis_c, self.ch_names, self.percent)
        chart.addAxis(axis_c, QtCore.Qt.AlignLeft)
        # /////////////////////////////////////////////////////////////// axis_t
        axis_t = QCategoryAxis()
        axis_t.setRange(0, self.chart_duration_min * 60)
        axis_t.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        axis_t.setTruncateLabels(False)
        axis_t = self.update_time_axis(self.chart_duration_min, axis_t,
                                       QDateTime.currentDateTime(), axis_x)
        chart.addAxis(axis_t, QtCore.Qt.AlignBottom)

        # SUPER INIT
        super(ChartAn, self).__init__(chart)

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
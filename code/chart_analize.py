from PySide6.QtCharts import QChartView, QChart, QValueAxis, QCategoryAxis
from PySide6 import QtCore


class ChartAn(QChartView):
    def __init__(self, session):
        self.ch_names = session.get_eeg_ch_names()
        self.num_ch = len(self.ch_names)
        self.tick_nums = 5
        self.percent = 100

        chart = QChart()
        chart.legend().setVisible(False)

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

        super(ChartAn, self).__init__(chart)

    # ///////////////////////////////////////////////////// Update CHANNELS axis
    def update_channels_axis(self, axis_c, ch_names, amp):
        num_ch = len(ch_names)
        axis_range_max = num_ch * amp
        axis_c.setRange(0, axis_range_max)

        labels = axis_c.categoriesLabels()
        for i in range(len(labels)):
            axis_c.remove(labels[i])

        interval = amp // self.tick_nums
        for i, ch_name in enumerate(ch_names[num_ch - 1::-1]):
            start = i * amp
            axis_c.append(f'--{ch_name}--', start)
            for j in range(interval, amp, interval):
                axis_c.append(i * ' ' + str(j), j + start)
        axis_c.append(str(amp), axis_range_max)
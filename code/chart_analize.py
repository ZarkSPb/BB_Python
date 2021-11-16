from PySide6.QtCharts import QChartView, QChart, QValueAxis, QCategoryAxis
from PySide6 import QtCore


class ChartAn(QChartView):
    def __init__(self, session):
        self.ch_names = session.get_eeg_ch_names()
        self.num_ch = len(self.ch_names)

        chart = QChart()
        chart.legend().setVisible(False)

        # /////////////////////////////////////////////////////////////// axis_y
        axis_y = QValueAxis()
        axis_y.setRange(0, self.num_ch * 100)
        # axis_y.setTickCount(9)
        # axis_y.setMinorTickCount(1)
        axis_y.setLabelsVisible(False)
        chart.addAxis(axis_y, QtCore.Qt.AlignRight)

        # /////////////////////////////////////////////////////////////// axis_c
        axis_c = QCategoryAxis()
        axis_c.setRange(0, self.num_ch)
        axis_c.setGridLineVisible(False)
        axis_c.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        axis_c.setTruncateLabels(False)
        self.update_channels_axis(axis_c, session, (100, 100, 100, 100), self.num_ch)
        chart.addAxis(axis_c, QtCore.Qt.AlignLeft)

        super(ChartAn, self).__init__(chart)

    # ///////////////////////////////////////////////////////// Update CHANNELS axis
    def update_channels_axis(axis_c, session, amps, num_ch):
        labels = axis_c.categoriesLabels()
        for i in range(len(labels)):
            axis_c.remove(labels[i])

        axis_c.append(f'{-amps[0]}', 0)
        channel_names = session.get_eeg_ch_names()
        for i, ch_name in enumerate(channel_names[num_ch - 1::-1]):
            axis_c.append(f'{-amps[i] // 2}' + i * ' ', i + 0.25)
            axis_c.append(f'--{ch_name}--', i + 0.5)
            axis_c.append(f'{amps // 2}' + i * ' ', i + 0.75)
            if i < num_ch - 1:
                axis_c.append(f'({amps})' + i * ' ', i + 1)
            else:
                axis_c.append(f'{amps}', i + 1)
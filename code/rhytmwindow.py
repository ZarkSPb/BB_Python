from PySide6 import QtCore
from PySide6.QtCharts import (QCategoryAxis, QChart, QChartView, QLineSeries,
                              QValueAxis)
from PySide6.QtCore import QDateTime
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from settings import MAX_CHART_SIGNAL_DURATION, NUM_CHANNELS, SAMPLE_RATE
from ui_rhytmwindow import Ui_RhytmWindow


class RhytmWindow(QWidget):
    def __init__(self, parent_ui):
        super(RhytmWindow, self).__init__()
        self.ui = Ui_RhytmWindow()
        self.ui.setupUi(self)

        self.parent_ui = parent_ui

        self.ui.SliderDuration.setMaximum(MAX_CHART_SIGNAL_DURATION)
        self.ui.SliderDuration.setValue(MAX_CHART_SIGNAL_DURATION)
        self.ui.SliderDuration.setSliderPosition(MAX_CHART_SIGNAL_DURATION)
        self.chart_duration = MAX_CHART_SIGNAL_DURATION
        self.chart_amp = self.ui.SliderAmplitude.value()

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
        # axis_t = self.update_time_axis(axis_t, QDateTime.currentDateTime())
        chart.addAxis(axis_t, QtCore.Qt.AlignBottom)
        # /////////////////////////////////////////////////////////////// axis_c
        axis_c = QCategoryAxis()
        axis_c.setRange(0, 4)
        axis_c.setGridLineVisible(False)
        axis_c.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        # self.update_channels_axis(axis_c)
        chart.addAxis(axis_c, QtCore.Qt.AlignLeft)
        # //////////////////////////////////////////////////////// serieses fill
        self.serieses = []
        # self.chart_buffers_update()
        for i in range(NUM_CHANNELS):
            series = QLineSeries()
            # series.append(self.chart_buffers[i])
            self.serieses.append(series)
            chart.addSeries(self.serieses[-1])
            self.serieses[-1].attachAxis(axis_x)
            self.serieses[-1].attachAxis(axis_y)
        # //////////////////////////////////////////////////// Chart view create
        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing, True)
        self.ui.LayoutCharts.addWidget(self.chart_view)

    def closeEvent(self, event):
        self.parent_ui.actionRhytm_window.setChecked(False)

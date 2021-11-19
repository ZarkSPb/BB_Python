from PySide6.QtCharts import QChartView


class ChartFiltered(QChartView):
    def __init__(self, chart, maximize_func):
        # SUPER INIT
        super(ChartFiltered, self).__init__(chart)

        self.maximize_func = maximize_func

    def mouseDoubleClickEvent(self, event):
        self.maximize_func()

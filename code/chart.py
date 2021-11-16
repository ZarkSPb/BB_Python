from PySide6.QtCharts import QCategoryAxis, QChart, QValueAxis
from PySide6 import QtCore
from PySide6.QtCore import QDateTime, QPointF
from settings import MAX_CHART_SIGNAL_DURATION


# /////////////////////////////////////////////////////////////////// CHART MAKE
def init(session, amp, num_ch):
    chart_duration = MAX_CHART_SIGNAL_DURATION

    chart = QChart()
    chart.legend().setVisible(False)
    # /////////////////////////////////////////////////////////////////// axis_x
    axis_x = QValueAxis()
    axis_x.setRange(0, MAX_CHART_SIGNAL_DURATION * session.get_sample_rate())
    axis_x.setVisible(False)
    axis_x.setLabelFormat('%i')
    chart.addAxis(axis_x, QtCore.Qt.AlignTop)
    # /////////////////////////////////////////////////////////////////// axis_y
    axis_y = QValueAxis()
    axis_y.setRange(0, amp * num_ch * 2)
    axis_y.setTickCount(9)
    axis_y.setMinorTickCount(1)
    axis_y.setLabelsVisible(False)
    chart.addAxis(axis_y, QtCore.Qt.AlignRight)
    # /////////////////////////////////////////////////////////////////// axis_t
    axis_t = QCategoryAxis()
    axis_t.setRange(0, chart_duration * 1000)
    axis_t.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
    axis_t.setTruncateLabels(False)
    axis_t = update_time_axis(chart_duration, axis_t,
                              QDateTime.currentDateTime())
    chart.addAxis(axis_t, QtCore.Qt.AlignBottom)
    # /////////////////////////////////////////////////////////////////// axis_c
    axis_c = QCategoryAxis()
    axis_c.setRange(0, len(session.get_eeg_ch_names()))
    axis_c.setGridLineVisible(False)
    axis_c.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
    axis_c.setTruncateLabels(False)
    update_channels_axis(axis_c, session, amp, num_ch)
    chart.addAxis(axis_c, QtCore.Qt.AlignLeft)

    return chart, axis_x, axis_y


def buffers_update(amp, ch_name, chart_duration, sample_rate):
    ch_buffers = []
    num_ch = len(ch_name)
    for i in range(num_ch):
        ch_buffers.append([
            QPointF(x, amp + (num_ch - 1 - i) * 2 * amp)
            for x in range(chart_duration * sample_rate)
        ])

    return ch_buffers


# ///////////////////////////////////////////////////////////// Update TIME axis
def update_time_axis(chart_duration, axis_t, start_time):
    end_time = start_time.addSecs(chart_duration)
    offset = 1000 - int(start_time.toString('zzz'))
    labels = axis_t.categoriesLabels()
    for label in labels:
        axis_t.remove(label)

    axis_t.append(start_time.toString('hh:mm:ss.zzz'), 0)
    axis_t.append(' ', offset)

    for i in range(1, chart_duration - 1):
        shifted_time = start_time.addSecs(i + 1)
        time_string = shifted_time.toString('ss')
        if ((time_string == '00') or (time_string == '20')
                or (time_string == '40')):
            time_string = shifted_time.toString('hh:mm:ss')
        axis_t.append(time_string, offset + i * 1000)

    axis_t.append('  ', (chart_duration - 1) * 1000 + offset)
    axis_t.append(end_time.toString('hh:mm:ss'), chart_duration * 1000)

    return axis_t


# ///////////////////////////////////////////////////////// Update CHANNELS axis
def update_channels_axis(axis_c, session, chart_amp, num_ch):
    labels = axis_c.categoriesLabels()
    for i in range(len(labels)):
        axis_c.remove(labels[i])

    axis_c.append(f'{-chart_amp}', 0)
    channel_names = session.get_eeg_ch_names()
    for i, ch_name in enumerate(channel_names[num_ch - 1::-1]):
        axis_c.append(f'{-chart_amp // 2}' + i * ' ', i + 0.25)
        axis_c.append(f'--{ch_name}--', i + 0.5)
        axis_c.append(f'{chart_amp // 2}' + i * ' ', i + 0.75)
        if i < num_ch - 1:
            axis_c.append(f'({chart_amp})' + i * ' ', i + 1)
        else:
            axis_c.append(f'{chart_amp}', i + 1)
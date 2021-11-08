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
    axis_t.append(end_time.toString('hh:mm:ss.zzz'), chart_duration * 1000)

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
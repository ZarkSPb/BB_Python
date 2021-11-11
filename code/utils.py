# import numpy as np
from brainflow.data_filter import DataFilter, DetrendOperations, FilterTypes
from numpy import savetxt, zeros
import os

from settings import *


def save_file(session,
              file_name='eeg.csv',
              folder='',
              save_first=True,
              start_index=0,
              auto=True):
    def save(filtered=False):
        h = header
        h += 'filtered\n' if filtered else 'no filtered\n'
        for channel_names in EEG_CHANNEL_NAMES:
            h += f'{channel_names}, uV;'
        h += 'LinuxTime, sec.;BoardIndex, 0-255'

        file_name_full = f'{folder}/{file_name}' if folder != '' else file_name
        open_regim = 'a' if auto else 'w'
        with open(file_name_full, open_regim) as file_object:
            if save_first:
                savetxt(file_object,
                        data.T,
                        fmt=format,
                        delimiter=';',
                        header=h,
                        comments='#')
            else:
                savetxt(file_object, data.T, fmt=format, delimiter=';')

    # ////////////////////////////////////////////////////////////// MAKE HEADER
    first_name = session.patient.get_first_name()
    last_name = session.patient.get_last_name()
    header = first_name if first_name != '' else 'no_first_name' + '\n'
    header += last_name if last_name != '' else 'no_last_name' + '\n'
    header += session.time_init.toString('dd.MM.yyyy') + '\n'
    header += session.time_init.toString('hh:mm:ss.zzz') + '\n'

    format = ['%.3f', '%.3f', '%.3f', '%.3f', '%.3f', '%3.0f']

    if (folder != '') and not os.path.exists(folder):
        os.makedirs(folder)

    end_index = session.buffer_main.get_last_num()
    if start_index:
        # data = session.buffer_main.get_buff_from(last_index)
        data = session.buffer_main.get_buff_from(start_index, end_index)
    else:
        data = session.buffer_main.get_buff_last()
    last_save_index = data.shape[1]

    end_f = file_name.rfind('\\')
    if end_f == -1: end_f = file_name.rfind('/')

    if end_f != -1:
        f_name = file_name[end_f + 1:]
        if f_name[:3] == '(f)':
            f_name = f_name[3:]
            file_name = file_name[:end_f + 1] + f_name

    save()

    if session.get_save_filtered_status():
        data = session.buffer_filtered.get_buff_from(start_index, end_index)

        end_f = file_name.rfind('\\')
        if end_f == -1: end_f = file_name.rfind('/')
        if end_f != -1:
            file_name = file_name[:end_f + 1] + '(f)' + file_name[end_f + 1:]
        else:
            file_name = '(f)' + file_name

        save(True)

    return last_save_index


def signal_filtering(data, filtering=True):
    DataFilter.detrend(data, DetrendOperations.CONSTANT.value)

    if filtering:
        DataFilter.perform_bandpass(data, SAMPLE_RATE, 16.0, 28.0, 4,
                                    FilterTypes.BUTTERWORTH.value, 0)
        DataFilter.perform_bandpass(data, SAMPLE_RATE, 16.0, 28.0, 4,
                                    FilterTypes.BUTTERWORTH.value, 0)

    DataFilter.perform_bandstop(data, SAMPLE_RATE, 50.0, 4.0, 4,
                                FilterTypes.BUTTERWORTH.value, 0)
    DataFilter.perform_bandstop(data, SAMPLE_RATE, 60.0, 4.0, 4,
                                FilterTypes.BUTTERWORTH.value, 0)


def rhytm_constructor(data, rhytms):
    data_res = zeros(data.shape)
    for value in rhytms.values():
        if value[-1]:
            center = (value[0] + value[1]) / 2
            width = float(value[1] - value[0])
            data_c = data.copy()
            DataFilter.perform_bandpass(data_c, SAMPLE_RATE, center, width, 4,
                                        FilterTypes.BUTTERWORTH.value, 0)
            data_res += data_c
    return data_res


def file_name_constructor(session):
    file_name = session.time_start.toString('yyyy-MM-dd__hh-mm-ss')
    patient_name = session.patient.get_full_name()
    if patient_name:
        file_name += '__' + patient_name
    file_name += '.csv'

    return file_name
# import numpy as np
from brainflow.data_filter import DataFilter, DetrendOperations, FilterTypes
from numpy import savetxt, zeros
import os
from settings import FOLDER

from settings import *


def save_file(session, file_name='eeg.csv', save_first=True, save_index=None):
    def save():
        with open(f'{FOLDER}/{file_name}', 'a') as file_object:
            if save_first:
                savetxt(file_object,
                        data.T,
                        fmt=format,
                        delimiter=';',
                        header=header + 'no filtered\n',
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
    for channel_names in EEG_CHANNEL_NAMES:
        header += f'{channel_names}, uV;'
    header += 'LinuxTime, sec.;BoardIndex, 0-255'

    format = ['%.3f', '%.3f', '%.3f', '%.3f', '%.3f', '%3.0f']

    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    if save_index:
        data = session.buffer_main.get_buff_from(save_index)
    else:
        data = session.buffer_main.get_buff_last()
    save_index = data.shape[1]
    save()

    if session.get_save_filtered_status():
        data = session.buffer_filtered.get_buff_from(save_index)
        file_name = '(f)' + file_name
        save()

    return save_index


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
    # file_name = '(f)' if session.save_filtered else ''
    file_name = session.time_start.toString('yyyy-MM-dd__hh-mm-ss')
    patient_name = session.patient.get_full_name()
    if patient_name:
        file_name += '__' + patient_name
    file_name += '.csv'

    return file_name

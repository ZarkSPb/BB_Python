# import numpy as np
from brainflow.data_filter import DataFilter, DetrendOperations, FilterTypes
from numpy import savetxt, zeros
import os
from settings import FOLDER

from settings import *


def save_file(data, session, file_name='eeg.csv', save_first=True):
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)
    with open(f'{FOLDER}/{file_name}', 'a') as file_object:
        first_name = session.patient.get_first_name()
        last_name = session.patient.get_last_name()

        if save_first:

            header = ''
            header += first_name if first_name != '' else 'no_first_name'
            header += '\n'
            header += last_name if last_name != '' else 'no_last_name'
            header += '\n'
            header += session.time_init.toString('dd.MM.yyyy') + '\n'
            header += session.time_init.toString('hh:mm:ss.zzz') + '\n'
            header += 'filtered\n' if session.get_filtered_status(
            ) else 'no filtered\n'

            for channel_names in EEG_CHANNEL_NAMES:
                header += f'{channel_names}, uV;'
            header += 'LinuxTime, sec.;BoardIndex, 0-255'
            savetxt(file_object,
                    data.T,
                    fmt=['%.3f', '%.3f', '%.3f', '%.3f', '%.3f', '%3.0f'],
                    delimiter=';',
                    header=header,
                    comments='#')
        else:
            savetxt(file_object, data.T, fmt='%6.3f', delimiter=';')


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

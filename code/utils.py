import numpy as np
from brainflow.data_filter import DataFilter, DetrendOperations, FilterTypes

from settings import *


def save_file(data, file_name='eeg.csv', save_first=True):
    with open(file_name, 'a') as file_object:
        if save_first:
            header = ''
            for channel_names in EEG_CHANNEL_NAMES:
                header += f'{channel_names};'
            header += 'LinuxTime;BoardIndex'
            np.savetxt(file_object,
                       data.T,
                       fmt=['%.3f', '%.3f', '%.3f', '%.3f', '%.3f', '%3.0f'],
                       delimiter=';',
                       header=header,
                       comments='')
        else:
            np.savetxt(file_object, data.T, fmt='%6.3f', delimiter=';')


def signal_filtering(data):
    DataFilter.detrend(data, DetrendOperations.CONSTANT.value)
    DataFilter.perform_bandpass(data, SAMPLE_RATE, 16.0, 28.0, 4,
                                FilterTypes.BUTTERWORTH.value, 0)
    DataFilter.perform_bandpass(data, SAMPLE_RATE, 16.0, 28.0, 4,
                                FilterTypes.BUTTERWORTH.value, 0)
    DataFilter.perform_bandstop(data, SAMPLE_RATE, 50.0, 4.0, 4,
                                FilterTypes.BUTTERWORTH.value, 0)
    DataFilter.perform_bandstop(data, SAMPLE_RATE, 60.0, 4.0, 4,
                                FilterTypes.BUTTERWORTH.value, 0)


def file_name_constructor(patient, session):
    # file_name = '(f)' if session.save_filtered else ''
    file_name = session.time_start.strftime('%Y-%m-%d__%H-%M-%S')
    patient_name = patient.get_full_name()
    if patient_name:
        file_name += '__' + patient_name
    file_name += '.csv'

    return file_name
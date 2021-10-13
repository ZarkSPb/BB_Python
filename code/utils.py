import numpy as np
from brainflow.data_filter import DataFilter, DetrendOperations, FilterTypes

from settings import *


def save_file(data, file_name='eeg.csv'):
    with open(file_name, 'a') as file_object:
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
    file_name = session.start_time.strftime("%Y-%m-%d__%H-%M-%S")
    patient_name = patient.get_full_name()
    if patient_name:
        file_name += '__' + patient_name
    file_name += '.csv'

    return file_name

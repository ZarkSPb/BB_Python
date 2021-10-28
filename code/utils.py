# import numpy as np
from brainflow.data_filter import DataFilter, DetrendOperations, FilterTypes
from numpy import savetxt

from settings import *


def save_file(data, session, file_name='eeg.csv', save_first=True):
    with open(file_name, 'a') as file_object:

        first_name = session.patient.get_first_name()
        last_name = session.patient.get_last_name()

        if save_first:

            header = ''
            if first_name != '':
                header += first_name + '\n'
            else:
                header += 'no_first_name\n'

            if last_name != '':
                header += last_name + '\n'
            else:
                header += 'no_last_name\n'

            header += session.time_init.toString('dd.MM.yyyy') + '\n'
            header += session.time_init.toString('hh:mm:ss.zzz') + '\n'

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


def file_name_constructor(session):
    # file_name = '(f)' if session.save_filtered else ''
    file_name = session.time_start.toString('yyyy-MM-dd__hh-mm-ss')
    patient_name = session.patient.get_full_name()
    if patient_name:
        file_name += '__' + patient_name
    file_name += '.csv'

    return file_name

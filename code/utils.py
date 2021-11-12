# import numpy as np
from brainflow.data_filter import DataFilter, DetrendOperations, FilterTypes
from numpy import savetxt, zeros
import os
import pyedflib
from datetime import datetime

from settings import *


def save_CSV(session,
             file_name='eeg.csv',
             folder='',
             save_first=True,
             start_index=0,
             auto=True):
    def save(filtered=False):
        h = header
        h += 'filtered\n' if filtered else 'no filtered\n'
        ch_names = session.get_eeg_ch_names()
        for ch_name in ch_names:
            h += f'{ch_name}, uV;'
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


def save_EDF(session, file_name='eeg.edf'):
    filtered = False
    end_f = file_name.rfind('\\')
    if end_f == -1: end_f = file_name.rfind('/')
    if end_f != -1:
        f_name = file_name[end_f + 1:]
        if f_name[:3] == '(f)': filtered = True

    f = pyedflib.EdfWriter(file_name, 1, file_type=pyedflib.FILETYPE_EDFPLUS)

    patient_name = session.patient.get_first_name(
    ) + '_' + session.patient.get_last_name()
    header = {
        'technician': '',
        'recording_additional': '',
        'patientname': patient_name,
        'patient_additional': '',
        'patientcode': '',
        'equipment': '',
        'admincode': '',
        'gender': '',
        'startdate': session.time_start.toPython(),
        'birthdate': '',
    }
    f.setHeader(header)

    ch_names = session.get_eeg_ch_names()
    for i in range(len(ch_names)):
        print(ch_names[i])
        ch_names[i] = 'EEG ' + ch_names[i]
    signal_headers = []
    for ch_name in ch_names:
        signal_header = {
            'label': ch_name,
            'dimension': 'uV',
            'sample_rate': float(SAMPLE_RATE),
            'physical_max': 0.4 * 10**6,
            'physical_min': -0.4 * 10**6,
            'digital_max': 400000,
            'digital_min': -4000000,
            'transducer': 'AuCl',
            'prefilter': str(filtered)
        }

        signal_headers.append(signal_header)
    f.setSignalHeaders(signal_headers)

    # print()
    # for s in signal_headers:
    #     print(s)
    # print()

    f.close()


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

    return file_name
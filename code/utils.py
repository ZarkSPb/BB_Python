# import numpy as np
from brainflow.data_filter import DataFilter, DetrendOperations, FilterTypes
from numpy import savetxt, zeros, min, max
import os
import pyedflib
from datetime import datetime
from math import floor, ceil


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
    header = first_name if first_name != '' else 'no_first_name'
    header += '\n'
    header += last_name if last_name != '' else 'no_last_name'
    header += '\n'
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
    def save(filtered=False):
        pref_ann = 'HP:100mHZ N:50000mHZ N:60000mHZ'
        if filtered: pref_ann = pref_ann + ' HP:2000mHZ LP:30000mHZ'

        signal_headers = []
        for ch_name in ch_names:
            signal_header = {
                'label': ch_name,
                'dimension': 'uV',
                'sample_rate': session.get_sample_rate(),
                'physical_max': ceil(max(data)),
                'physical_min': floor(min(data)),
                'digital_max': 32767,
                'digital_min': -32768,
                'transducer': 'AuCl electrode',
                'prefilter': pref_ann
            }
            signal_headers.append(signal_header)

        f = pyedflib.EdfWriter(file_name,
                               len(ch_names),
                               file_type=pyedflib.FILETYPE_EDFPLUS)
        f.setHeader(header)
        f.setSignalHeaders(signal_headers)
        f.writeSamples(data)
        f.close()

    header = {
        'technician': '',
        'recording_additional': 'BrainBit',
        'patientname': session.patient.get_last_name(),
        'patient_additional': session.patient.get_first_name(),
        'patientcode': '',
        'equipment': '',
        'admincode': '',
        'gender': '',
        'startdate': session.time_start.toPython(),
        'birthdate': ''  # datetime.now().strftime('%d %b %Y')
    }
    ch_names = session.get_eeg_ch_names()
    for i in range(len(ch_names)):
        ch_names[i] = 'EEG ' + ch_names[i]

    filtered = False
    end_f = file_name.rfind('\\')
    if end_f == -1: end_f = file_name.rfind('/')
    if end_f != -1:
        f_name = file_name[end_f + 1:]
        if f_name[:3] == '(f)': filtered = True

    if filtered:
        data = session.buffer_filtered.get_buff_last()[:len(ch_names)]
        save(True)
        file_name = file_name[:end_f + 1] + f_name[3:]
        data = session.buffer_main.get_buff_last()[:len(ch_names)]
        save()
    else:
        data = session.buffer_main.get_buff_last()[:len(ch_names)]
        save()
        file_name = file_name[:end_f + 1] + '(f)' + f_name
        save(True)


def signal_filtering(data, sample_rate, filtering=True):
    DataFilter.detrend(data, DetrendOperations.CONSTANT.value)

    if filtering:
        DataFilter.perform_bandpass(data, sample_rate, 16.0, 28.0, 4,
                                    FilterTypes.BUTTERWORTH.value, 0)
        DataFilter.perform_bandpass(data, sample_rate, 16.0, 28.0, 4,
                                    FilterTypes.BUTTERWORTH.value, 0)

    DataFilter.perform_bandstop(data, sample_rate, 50.0, 4.0, 4,
                                FilterTypes.BUTTERWORTH.value, 0)
    DataFilter.perform_bandstop(data, sample_rate, 60.0, 4.0, 4,
                                FilterTypes.BUTTERWORTH.value, 0)


def rhytm_constructor(data, rhytms, sample_rate):
    data_res = zeros(data.shape)
    for value in rhytms.values():
        if value[-1]:
            center = (value[0] + value[1]) / 2
            width = float(value[1] - value[0])
            data_c = data.copy()
            DataFilter.perform_bandpass(data_c, sample_rate, center, width, 4,
                                        FilterTypes.BUTTERWORTH.value, 0)
            data_res += data_c
    return data_res


def file_name_constructor(session):
    file_name = session.time_start.toString('yyyy-MM-dd__hh-mm-ss')
    patient_name = session.patient.get_full_name()
    if patient_name:
        file_name += '__' + patient_name

    return file_name
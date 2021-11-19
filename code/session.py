import numpy as np
from PySide6.QtCore import QDateTime, QThread

from settings import (BATTERY_CHANNEL, NUM_CHANNELS, SAMPLE_RATE, SAVE_CHANNEL,
                      SIGNAL_CLIPPING_SEC, UPDATE_BUFFER_SPEED_MS,
                      EEG_CHANNEL_NAMES)
from utils import signal_filtering
from worker import Worker


class Patient:
    def __init__(self, first_name='', last_name=''):
        self.first_name = first_name
        self.last_name = last_name

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_full_name(self):
        fullname = ''
        if self.first_name:
            fullname = self.first_name
            if self.last_name:
                fullname += '_' + self.last_name
        elif self.last_name:
            fullname = self.last_name

        return fullname


class Buffer:
    def __init__(self, buffer_size=450000, channels_num=4):
        self.buffer_size = buffer_size
        self.channels_num = channels_num
        self.buff = np.zeros((self.channels_num, self.buffer_size))
        self.last = 0

    def add(self, add_sample):
        if type(add_sample) != np.ndarray:
            add_sample = np.asarray(add_sample)

        add_size = add_sample.shape[1]

        if add_size + self.last < int(self.buff.shape[1] * 3 / 4):
            self.buff[:, self.last:self.last + add_size] = add_sample
            self.last = self.last + add_size
        else:
            # increase buffer size
            self.buff = np.hstack((self.buff, np.zeros(self.buff.shape)))
            self.buff[:, self.last:self.last + add_size] = add_sample
            self.last = self.last + add_size

    def get_buff_last(self, count=0):
        if (count == 0) or (count > self.last):
            return self.buff[:, :self.last].copy()
        else:
            return self.buff[:, self.last - count:self.last].copy()

    def get_buff_from(self, start_index=0, end_index=0):
        if start_index < 0: start_index = 0

        return self.buff[:, start_index:self.last if end_index ==
                         0 else end_index].copy()

    def get_last_num(self):
        return self.last


class Session():
    def __init__(self,
                 save_filtered=True,
                 buffer_size=10000,
                 first_name='',
                 last_name='',
                 eeg_channel_names=EEG_CHANNEL_NAMES,
                 sample_rate=SAMPLE_RATE):

        self.connected = False
        self.save_filtered = save_filtered
        self.status = False
        self.time_init = QDateTime.currentDateTime()
        self.patient = Patient(first_name, last_name)
        self.buffer_main = Buffer(buffer_size=buffer_size,
                                  channels_num=len(SAVE_CHANNEL))
        self.buffer_filtered = Buffer(buffer_size=buffer_size,
                                      channels_num=len(SAVE_CHANNEL))
        self.eeg_channel_names = eeg_channel_names
        self.sample_rate = sample_rate
        self.battery_value = 0

    def session_start(self, board):
        if self.status:
            print('The thread is already running.')
        else:
            self.time_start = QDateTime.currentDateTime()
            self.board = board
            self.worker_buff_main = Worker(self.update_buff)
            self.worker_buff_main.start()
            self.status = True

    def session_stop(self):
        self.time_stop = QDateTime.currentDateTime()
        self.status = False

    def get_save_filtered_status(self):
        return self.save_filtered

    def get_status(self):
        return self.status

    def add(self, data):
        self.buffer_main.add(data)

        add_sample = data.shape[1]
        if add_sample != 0:
            self.filtered_buffer_update(add_sample)

    def filtered_buffer_update(self, add_sample):
        data = self.buffer_main.get_buff_last(SIGNAL_CLIPPING_SEC *
                                              self.sample_rate + add_sample)
        for channel in range(NUM_CHANNELS):
            signal_filtering(data[channel], self.sample_rate)
        self.buffer_filtered.add(data[:, -add_sample:])

    def update_buff(self):
        while self.get_status():
            data = self.board.get_board_data()
            if np.any(data):
                self.add(data[SAVE_CHANNEL, :])
                self.battery_value = data[BATTERY_CHANNEL, -1]

            QThread.msleep(UPDATE_BUFFER_SPEED_MS)

    def get_battery_value(self):
        return self.battery_value

    def get_eeg_ch_names(self):
        return self.eeg_channel_names

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def get_connect_status(self):
        return self.connected

    def get_sample_rate(self):
        return self.sample_rate
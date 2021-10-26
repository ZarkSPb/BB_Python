import numpy as np
from PySide6.QtCore import QDateTime, QThread

from buff import Buffer
from settings import (BATTERY_CHANNEL, NUM_CHANNELS, SAMPLE_RATE, SAVE_CHANNEL,
                      SIGNAL_CLIPPING_SEC, UPDATE_BUFFER_SPEED_MS)
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


class Session():
    def __init__(self,
                 save_filtered=True,
                 buffer_size=10000,
                 first_name='',
                 last_name=''):

        self.save_filtered = save_filtered
        self.status = False
        self.time_init = QDateTime.currentDateTime()
        self.patient = Patient(first_name, last_name)
        self.buffer_main = Buffer(buffer_size=buffer_size,
                                  channels_num=len(SAVE_CHANNEL))
        self.buffer_filtered = Buffer(buffer_size=buffer_size,
                                      channels_num=len(SAVE_CHANNEL))

    def session_start(self, board):
        if self.status:
            print('The thread is already running.')
        else:
            self.time_start = QDateTime.currentDateTime()
            self.board = board
            self.worker_buff_main = Worker(self.update_buff)
            self.worker_buff_main.start(priority=QThread.HighPriority)
            self.status = True

    def session_stop(self):
        self.time_stop = QDateTime.currentDateTime()
        self.status = False

    def get_filtered_status(self):
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
                                              SAMPLE_RATE + add_sample)
        for channel in range(NUM_CHANNELS):
            signal_filtering(data[channel])
        self.buffer_filtered.add(data[:, -add_sample:])

    def update_buff(self):
        while self.get_status():
            data = self.board.get_board_data()
            if np.any(data):
                self.add(data[SAVE_CHANNEL, :])
                self.battery_value = data[BATTERY_CHANNEL, -1]

            QThread.msleep(UPDATE_BUFFER_SPEED_MS)

    def get_battery_value(self):
        return self.battery_value if self.status else 0

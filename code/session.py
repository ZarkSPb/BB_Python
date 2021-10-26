from PySide6.QtCore import QDateTime

from buff import Buffer
from patient import Patient
from settings import (NUM_CHANNELS, SAMPLE_RATE, SAVE_CHANNEL,
                      SIGNAL_CLIPPING_SEC)
from utils import signal_filtering


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

    def session_start(self):
        self.time_start = QDateTime.currentDateTime()
        self.status = True

    def stop_session(self):
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

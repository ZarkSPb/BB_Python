from PySide6.QtCore import QDateTime

from buff import Buffer
from patient import Patient


class Session():
    def __init__(self,
                 save_filtered=True,
                 channels_num=4,
                 buffer_size=1000,
                 first_name='',
                 last_name=''):

        self.save_filtered = save_filtered
        self.status = False
        self.time_init = QDateTime.currentDateTime()
        self.patient = Patient(first_name, last_name)
        self.buffer_main = Buffer(buffer_size=buffer_size, channels_num=channels_num)
        self.buffer_filtered = Buffer(buffer_size=buffer_size, channels_num=channels_num)

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

from patient import Patient
from PySide6.QtCore import QDateTime

class Session():
    def __init__(self, save_filtered=True, first_name='', last_name=''):
        self.save_filtered = save_filtered
        self.status = False
        self.time_init = QDateTime.currentDateTime()
        self.patient = Patient(first_name, last_name)

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
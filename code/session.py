from PySide6.QtCore import QDateTime

class Session:
    def __init__(self, save_filtered=True):
        self.save_filtered = save_filtered
        self.status = False
        self.time_init = QDateTime.currentDateTime()

    def session_start(self):
        self.time_start = QDateTime.currentDateTime()
        self.status = True

    def stop_session(self):
        self.time_stop = QDateTime.currentDateTime()
    
    def get_flt_status(self):
        return self.save_filtered
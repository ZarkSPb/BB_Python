from datetime import datetime


class Session:
    def __init__(self, save_filtered=True):
        self.save_filtered = save_filtered
        self.status = False
        self.time_init = datetime.now()

    def session_start(self):
        self.time_start = datetime.now()
        self.status = True

    def stop_session(self):
        self.time_stop = datetime.now()
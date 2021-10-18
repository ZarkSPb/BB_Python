from datetime import datetime


class Session:
    def __init__(self, save_filtered=True):
        self.start_time = datetime.now()
        self.save_filtered = save_filtered

    def stop_session(self):
        self.stop_time = datetime.now()
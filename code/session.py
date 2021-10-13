from datetime import datetime


class Session:
    def __init__(self):
        self.start_time = datetime.now()

    def stop_session(self):
        self.stop_time = datetime.now()
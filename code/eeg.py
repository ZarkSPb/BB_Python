import numpy as np
from brainflow import BoardShim, BrainFlowInputParams


class Eeg:
    def __init__(self, board_id):
        self.work = False
        self.num_channel = BoardShim.get_package_num_channel(board_id)
        self.exg_channels = BoardShim.get_exg_channels(board_id)
        self.sample_rate = BoardShim.get_sampling_rate(board_id)

        BoardShim.enable_dev_board_logger()
        params = BrainFlowInputParams()
        # try:
        self.board = BoardShim(board_id, params)
        self.board.prepare_session()
        # finally:

    def prepare(self):
        self.board.start_stream(450000)

    def buffer_fill(self, progress_callback):
        # create buffer
        self.BUFFER_SIZE = self.sample_rate
        self.buff = np.zeros((self.BUFFER_SIZE, len(self.exg_channels)))
        i = 0
        while i < self.BUFFER_SIZE:
            data = self.board.get_board_data(1)
            if np.any(data):
                # current_num = data[self.num_channel]
                self.current_exg = data[self.exg_channels]
                # self.buff[i, :] = self.current_exg[:, 0]
                self.buff = np.roll(self.buff, -1, axis=0)
                self.buff[-1] = self.current_exg[:, 0]
                i += 1
                progress_callback.emit(self.buff)

    def capture(self, progress_callback):
        while self.work:
            data = self.board.get_board_data(1)
            if np.any(data):
                self.current_exg = data[self.exg_channels]
                self.buff = np.roll(self.buff, -1, axis=0)
                self.buff[-1] = self.current_exg[:, 0]

                # Callback return
                progress_callback.emit(self.buff)
                
        if self.board.is_prepared():
                self.board.release_session()
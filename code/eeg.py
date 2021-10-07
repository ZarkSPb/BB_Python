import numpy as np
from brainflow import BoardShim

class Eeg:
    def __init__(self, board_shim):
        self.board_id = board_shim.get_board_id()
        self.board_shim = board_shim
        self.num_channel = BoardShim.get_package_num_channel(self.board_id)
        self.exg_channels = BoardShim.get_exg_channels(self.board_id)
        self.sample_rate = BoardShim.get_sampling_rate(self.board_id)

        # create buffer
        self.BUFFER_SIZE = self.sample_rate
        self.buff = np.zeros((self.BUFFER_SIZE, len(self.exg_channels)))

        # print(f'{BoardShim.get_board_descr(self.board_id)}\n')
        # print(f'num channel = {self.num_channel}')
        # print(self.exg_channels, end='\n\n')

        # Filling the buffer
        self.buffer_fill()

    def buffer_fill(self):
        i = 0
        while i < self.BUFFER_SIZE:
            data = self.board_shim.get_board_data(1)
            if np.any(data):
                # current_num = data[self.num_channel]
                self.current_exg = data[self.exg_channels]
                self.buff[i, :] = self.current_exg[:, 0]
                i += 1

    def capture(self, progress_callback):
        i = 0
        while i < 500:
            data = self.board_shim.get_board_data(1)
            if np.any(data):
                self.current_exg = data[self.exg_channels]
                self.buff = np.roll(self.buff, -1, axis=0)
                self.buff[-1] = self.current_exg[:, 0]
                i += 1
                progress_callback.emit(self.buff)
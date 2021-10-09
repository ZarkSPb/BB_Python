import numpy as np
from brainflow import BoardShim, BrainFlowInputParams
from time import sleep


class Eeg:
    def __init__(self, board_id, num_channels):
        self.num_channels = num_channels
        self.work = False
        self.exg_channels = BoardShim.get_exg_channels(board_id)

        BoardShim.enable_dev_board_logger()
        params = BrainFlowInputParams()
        # try:
        self.board = BoardShim(board_id, params)
        self.board.prepare_session()
        # finally:

    def start_stream(self, progress_callback):
        self.board.start_stream(50)
        # while self.work:
        #     data = self.board.get_board_data()
        #     if data.shape[1] > 0:
        #         progress_callback.emit(
        #             data[self.exg_channels[:self.num_channels], :])
        #     sleep(0.02)

    def stop_stream(self):
        self.board.stop_stream()

    def release_session(self):
        if self.board.is_prepared():
            self.board.release_session()

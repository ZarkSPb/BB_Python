import numpy as np
from brainflow import BoardShim, BrainFlowInputParams


class Eeg:
    def __init__(self, board_id):
        self.work = False
        self.num_channel = BoardShim.get_package_num_channel(board_id)
        self.exg_channels = BoardShim.get_exg_channels(board_id)
        self.sample_rate = BoardShim.get_sampling_rate(board_id)
        # self.board_descr = BoardShim.get_board_descr(board_id)

        BoardShim.enable_dev_board_logger()
        params = BrainFlowInputParams()
        # try:
        self.board = BoardShim(board_id, params)
        self.board.prepare_session()
        # finally:

    def start_stream(self):
        self.board.start_stream(450000)

    def capture(self, progress_callback):
        while self.work:
            data = self.board.get_board_data(1)
            if np.any(data):
                current_exg = data[self.exg_channels]
                # Callback return
                progress_callback.emit(current_exg)

    def stop_stream(self):
        self.board.stop_stream()

    def release_session(self):
        if self.board.is_prepared():
            self.board.release_session()

from brainflow.board_shim import BoardShim, BrainFlowInputParams
from settings import BOARD_TIMEOUT, BOARD_ID


class Board(BoardShim):
    def __init__(self):
        params = BrainFlowInputParams()
        params.timeout = BOARD_TIMEOUT
        super().__init__(BOARD_ID, params)
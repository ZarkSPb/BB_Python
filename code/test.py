from brainflow.board_shim import BoardIds, BoardShim, BrainFlowInputParams
import numpy as np
from time import sleep

# BOARD_ID = BoardIds.SYNTHETIC_BOARD.value
BOARD_ID = BoardIds.BRAINBIT_BOARD.value

BoardShim.enable_dev_board_logger()
params = BrainFlowInputParams()
# try:
board = BoardShim(BOARD_ID, params)
board.prepare_session()

board.start_stream(100)

i = 0
j = 0
# while i < 10:
#     data = board.get_current_board_data(2)
#     if np.any(data):
#         i += 1
#         # print(i, j, data, "\n\n")
#         # data = np.array([[]])
#         print(i, data)
#         print('---------', j)
#         j = 0
#     j += 1

while i < 50:
    data = board.get_board_data()
    if data.shape[1] > 0:
        i += 1
        print(i, data.shape)
    sleep(0.02)

if board.is_prepared():
    board.release_session()
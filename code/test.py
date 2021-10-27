from brainflow.board_shim import BoardIds, BoardShim, BrainFlowInputParams
from time import sleep
import time

BOARD_ID = BoardIds.SYNTHETIC_BOARD.value
# BOARD_ID = BoardIds.BRAINBIT_BOARD.value

TIMESTAMP_CHANNEL = BoardShim.get_timestamp_channel(BOARD_ID)

BoardShim.enable_dev_board_logger()
params = BrainFlowInputParams()
board = BoardShim(BOARD_ID, params)
board.prepare_session()

board.start_stream(450000)
start_time = time.time_ns()

sleep(100)
num_samples = board.get_board_data_count()
end_time = time.time_ns()

data = board.get_current_board_data(450000)
board.stop_stream()

if board.is_prepared():
    board.release_session()

num = data.shape[1]

print(f'\nnum: {num}')
print(f'system time: {(end_time - start_time) / 10**9}')
print(f'board time: {(data[TIMESTAMP_CHANNEL, -1] - data[TIMESTAMP_CHANNEL, 0])}')
print(f'frequency by system time: {num / ((end_time - start_time) / 10**9)}')
print(f'frequency by board time: {num / (data[TIMESTAMP_CHANNEL, -1] - data[TIMESTAMP_CHANNEL, 0])}\n')
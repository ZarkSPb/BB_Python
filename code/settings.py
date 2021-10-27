from brainflow.board_shim import BoardIds, BoardShim

# Configuring BB
BOARD_ID = BoardIds.SYNTHETIC_BOARD.value
# BOARD_ID = BoardIds.BRAINBIT_BOARD.value

# Getting BB settings
SAMPLE_RATE = BoardShim.get_sampling_rate(BOARD_ID)  # 250
EXG_CHANNELS = BoardShim.get_exg_channels(BOARD_ID)
NUM_CHANNELS = len(EXG_CHANNELS)
EEG_CHANNEL_NAMES = BoardShim.get_eeg_names(BOARD_ID)
RESISTANCE_CHANNELS = BoardShim.get_resistance_channels(BOARD_ID)
TIMESTAMP_CHANNEL = BoardShim.get_timestamp_channel(BOARD_ID)
PACKAGE_NUM_CHANNEL = BoardShim.get_package_num_channel(BOARD_ID)
BATTERY_CHANNEL = BoardShim.get_battery_channel(BOARD_ID)
BOARD_TIMEOUT = 5

# Chart setting
MAX_CHART_SIGNAL_DURATION = 20  # seconds
UPDATE_CHART_SPEED_MS = 40
SIGNAL_CLIPPING_SEC = 2

UPDATE_IMPEDANCE_SPEED_MS = 500
UPDATE_BUFFER_SPEED_MS = 10
LONG_TIMER_INTERVAL_MS = 5000

REG_KERNEL = '[0-9а-яёa-z()-]+'

if BOARD_ID == BoardIds.SYNTHETIC_BOARD.value:
    NUM_CHANNELS = 4
    EXG_CHANNELS = EXG_CHANNELS[:NUM_CHANNELS]
    EEG_CHANNEL_NAMES = EEG_CHANNEL_NAMES[:4]

SAVE_CHANNEL = EXG_CHANNELS.copy()
SAVE_CHANNEL.append(TIMESTAMP_CHANNEL)
SAVE_CHANNEL.append(PACKAGE_NUM_CHANNEL)
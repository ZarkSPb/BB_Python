from brainflow.board_shim import BoardIds, BoardShim

# Configuring BB
# BOARD_ID = BoardIds.SYNTHETIC_BOARD.value
BOARD_ID = BoardIds.BRAINBIT_BOARD.value

# Getting BB settings
SAMPLE_RATE = BoardShim.get_sampling_rate(BOARD_ID)  # 250
EXG_CHANNELS = BoardShim.get_exg_channels(BOARD_ID)
NUM_CHANNELS = len(EXG_CHANNELS)
EEG_CHANNEL_NAMES = BoardShim.get_eeg_names(BOARD_ID)
RESISTANCE_CHANNELS = BoardShim.get_resistance_channels(BOARD_ID)

# Chart setting
MAX_CHART_SIGNAL_DURATION = 20  # seconds
UPDATE_CHART_SPEED_MS = 40
SIGNAL_CLIPPING_SEC = 2

UPDATE_IMPEDANCE_SPEED_MS = 500
UPDATE_BUFFER_SPEED_MS = 20
SAVE_INTERVAL_MS = 5000

if BOARD_ID == BoardIds.SYNTHETIC_BOARD.value:
    NUM_CHANNELS = 4
    EXG_CHANNELS = EXG_CHANNELS[:NUM_CHANNELS]
    EEG_CHANNEL_NAMES = EEG_CHANNEL_NAMES[:4]
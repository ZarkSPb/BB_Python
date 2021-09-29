import brainflow
import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
import matplotlib.pyplot as plt

SAMPLERATE = 250
AVERAGE_LENGTH = 7 * SAMPLERATE

def get_fft(signal):
    amps = np.absolute(np.fft.rfft(signal))
    return amps / signal.shape[0]

class Eeg:
    def __init__(self, board_shim):
        self.board_id = board_shim.get_board_id()
        self.board_shim = board_shim
        self.num_channel = BoardShim.get_package_num_channel(self.board_id)
        self.exg_channels = BoardShim.get_exg_channels(self.board_id)

        # print(f'{BoardShim.get_board_descr(self.board_id)}\n')
        # print(f'num channel = {self.num_channel}')
        # print(self.exg_channels, end='\n\n')

        self.capture()

    def capture(self):

        BUFFER_SIZE = SAMPLERATE
        buff = np.zeros((BUFFER_SIZE, len(self.exg_channels)))

        # fill the buffer
        i = 0
        while i < SAMPLERATE:
            data = self.board_shim.get_board_data(1)
            if np.any(data):
                # current_num = data[self.num_channel]
                current_exg = data[self.exg_channels]
                buff[i, :] = current_exg[:,0]
                # print(current_exg[:,0])
                # print(buff[i])
                i += 1

        # !!! Включить интерактивный режим для анимации
        plt.ion()
        # Создание окна и осей для графика
        fig, ax = plt.subplots()
        # Отобразить график фукнции в начальный момент времени
        buff_spectrum = get_fft(buff[:, 9])
        line, = ax.plot(buff_spectrum[:41])

        # renew the buffer like queue
        j = 0
        i = 0
        while i < 1000:
            data = self.board_shim.get_board_data(1)
            if np.any(data):
                # current_num = data[self.num_channel]
                current_exg = data[self.exg_channels]
                buff = np.roll(buff, -1, axis=0)
                buff[-1] = current_exg[:,0]                
                i += 1
                # print(f'\r{i} : 1000', end='')

                if j == 10:
                    j = 0
                    buff_spectrum = get_fft(buff[:, 9])
                    line.set_ydata(buff_spectrum[:41])
                    # !!! Следующие два вызова требуются для обновления графика
                    plt.draw()
                    plt.gcf().canvas.flush_events()
                else:
                    j += 1


                
        # Отключить интерактивный режим по завершению анимации
        plt.ioff()
        # Нужно, чтобы график не закрывался после завершения анимации
        plt.show()

def main():

    board_id = BoardIds.SYNTHETIC_BOARD.value
    # board_id = BoardIds.BRAINBIT_BOARD.value

    BoardShim.enable_dev_board_logger()

    params = BrainFlowInputParams()

    try:
        board_shim = BoardShim(board_id, params)
        board_shim.prepare_session()
        board_shim.start_stream(45000)
        eeg = Eeg(board_shim)
    finally:
        if board_shim.is_prepared():
            board_shim.release_session()        


if __name__ == "__main__":
    main()
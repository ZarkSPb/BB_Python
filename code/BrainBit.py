import numpy as np
import threading
from time import sleep
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
        self.buff = np.zeros((BUFFER_SIZE, len(self.exg_channels)))

        # Filling the buffer
        t_thread = threading.Thread(target=self._buffer_fill)
        t_thread.daemon = True
        t_thread.start()

        # Waiting for filling SAMPLERATE count
        while t_thread.is_alive():
            sleep(0.001)

        # make and start main thread
        t_thread = threading.Thread(target=self._capture)
        t_thread.daemon = True
        t_thread.start()

        # plotting data
        self.plotting(t_thread)

    def plotting(self, t_thread):
        # !!! Включить интерактивный режим для анимации
        plt.ion()
        # Создание окна и осей для графика
        fig, ax = plt.subplots()
        # Отобразить график фукнции в начальный момент времени
        buff_spectrum = get_fft(self.buff[:, 9])
        line, = ax.plot(buff_spectrum[:41])

        while t_thread.is_alive():
            buff_spectrum = get_fft(self.buff[:, 9])
            line.set_ydata(buff_spectrum[:41])
            # !!! Следующие два вызова требуются для обновления графика
            plt.draw()
            plt.gcf().canvas.flush_events()
            sleep(0.04)

        # Отключить интерактивный режим по завершению анимации
        plt.ioff()
        # Нужно, чтобы график не закрывался после завершения анимации
        plt.show()

    def _buffer_fill(self):
        i = 0
        while i < SAMPLERATE:
            data = self.board_shim.get_board_data(1)
            if np.any(data):
                # current_num = data[self.num_channel]
                self.current_exg = data[self.exg_channels]
                self.buff[i, :] = self.current_exg[:, 0]
                i += 1
                # print(i)

    def _capture(self):
        i = 0
        while i < 500:
            data = self.board_shim.get_board_data(1)
            if np.any(data):
                self.current_exg = data[self.exg_channels]
                self.buff = np.roll(self.buff, -1, axis=0)
                self.buff[-1] = self.current_exg[:, 0]
                i += 1
                # print(i)


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
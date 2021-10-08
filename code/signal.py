import numpy as np


class Buffer:
    def __init__(self, sample_rate=250, signal_length=10, channels_num=4):
        self.buffer_size = sample_rate * signal_length
        self.buff = np.zeros((self.buffer_size, channels_num))

        print(self.buff.shape)

    def add(self, new_sample):
        self.buff = np.roll(self.buff, -1, axis=0)
        self.buff[-1] = new_sample

    def get_buff(self):
        return self.buff

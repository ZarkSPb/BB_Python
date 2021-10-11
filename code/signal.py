import numpy as np


class Buffer:
    def __init__(self, buffer_size=450000, channels_num=4):
        self.buffer_size = buffer_size
        self.buff = np.zeros((self.buffer_size, channels_num))
        self.last = 0

    def add(self, new_sample):
        new_size = new_sample.shape[0]
        # self.buff = np.roll(self.buff, -roll_count, axis=0)
        self.buff[self.last:self.last + new_size] = new_sample
        self.last = self.last + new_size

    def get_buff(self, count=0):
        if (count == 0) or (count > self.last):
            return self.buff[:self.last]
        else:
            return self.buff[self.last - count:self.last]


# b = Buffer(buffer_size=10, channels_num=2)

# a = np.array([[1, 2]])

# b.add(a)
# print("\n")
# print(b.get_buff())

# b.add(a)
# print("\n")
# print(b.get_buff())

# a = np.array([[3, 4], [5, 6]])

# b.add(a)
# print("\n")
# print(b.get_buff(2))
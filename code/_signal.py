import numpy as np

class Buffer:
    def __init__(self, buffer_size=450000, channels_num=4):
        self.buffer_size = buffer_size
        self.channels_num = channels_num
        self.buff = np.zeros((self.buffer_size, self.channels_num))
        self.last = 0

    def add(self, add_sample):
        add_size = add_sample.shape[0]

        if add_size + self.last < int(self.buffer_size * 3 / 4):
            self.buff[self.last:self.last + add_size] = add_sample
            self.last = self.last + add_size
        else:
            # increase buffer size
            self.buff = np.vstack((self.buff, np.zeros(self.buff.shape)))
            self.buff[self.last:self.last + add_size] = add_sample
            self.last = self.last + add_size

    def get_buff(self, count=0):
        if (count == 0) or (count > self.last):
            return self.buff[:self.last]
        else:
            return self.buff[self.last - count:self.last]


b = Buffer(buffer_size=10, channels_num=2)

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
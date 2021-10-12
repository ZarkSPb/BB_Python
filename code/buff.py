import numpy as np


class Buffer:
    def __init__(self, buffer_size=450000, channels_num=4):
        self.buffer_size = buffer_size
        self.channels_num = channels_num
        self.buff = np.zeros((self.channels_num, self.buffer_size))
        self.last = 0

    def add(self, add_sample):
        add_size = add_sample.shape[1]

        if add_size + self.last < int(self.buff.shape[1] * 3 / 4):
            self.buff[:, self.last:self.last + add_size] = add_sample
            self.last = self.last + add_size
        else:
            # increase buffer size
            self.buff = np.hstack((self.buff, np.zeros(self.buff.shape)))
            self.buff[:, self.last:self.last + add_size] = add_sample
            self.last = self.last + add_size
            print(self.buff.shape)

    def get_buff(self, count=0):
        if (count == 0) or (count > self.last):
            return self.buff[:, :self.last]
        else:
            return self.buff[:, self.last - count:self.last]


# b = Buffer(buffer_size=5, channels_num=2)
# print(b.buff)
# a = np.array([[1], [2]])
# b.add(a)
# print(b.get_buff())

# b.add(a)
# # print("\n")
# print(b.get_buff())

# a = np.array([[3, 4, 5], [6, 7, 8]])
# print(a.shape)

# b.add(a)
# print("\n")
# print(b.get_buff())

# print(b.buff)

# b.add(a)
# print("\n")
# print(b.get_buff(15))

# b.buff = 1
# print(b.buff)
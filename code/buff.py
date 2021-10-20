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

    def get_buff_last(self, count=0):
        if (count == 0) or (count > self.last):
            return self.buff[:, :self.last].copy()
        else:
            return self.buff[:, self.last - count:self.last].copy()

    def get_buff_from(self, start_index=0, end_index=0):
        if end_index == 0:
            return self.buff[:, start_index:self.last].copy()
        else:
            return self.buff[:, start_index:end_index].copy()
    
    def get_last_num(self):
        return self.last



# b = Buffer(buffer_size=5, channels_num=2)
# print(b.buff)
# a = np.array([[1], [2]])
# b.add(a)
# print(b.get_buff_last())

# b.add(a)
# # print("\n")
# print(b.get_buff_last())

# a = np.array([[3, 4, 5], [6, 7, 8]])
# print(a.shape)

# b.add(a)
# print("\n")
# print(b.get_buff_last())

# print(b.buff)

# b.add(a)
# print("\n")

# r = b.get_buff_last()
# print(r)

# r[1] = [0,0,0,0,0,0,0,0]
# print(r)

# # b.buff = 1
# print(b.get_buff_last())

# print(b.get_buf_from(5))
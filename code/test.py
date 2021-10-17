import numpy as np

kerneldt = np.dtype([
    ('Ch1', np.float16),
    ('Ch2', np.float16),
    ('Ch3', np.float16),
    ('Ch4', np.float16),
    ('time', np.float16),
    ('index', np.int8)
])

x = np.zeros((10,), dtype=kerneldt)

x[['Ch1', 'index']] = (5.0, 59)

np.savetxt('1.csv', x, delimiter=';')
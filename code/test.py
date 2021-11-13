import pyedflib
from datetime import datetime, date
import numpy as np

file_name = 'EDF/210128_000014_EEG_edf+.edf'

f = pyedflib.EdfReader(file_name)

# # n = f.signals_in_file
# # signal_labels = f.getSignalLabels()

header = f.getHeader()

print()
for i in header.items():
    print(i)

print()
print()

sh = f.getSignalHeaders()[0]
print()
for i in sh.items():
    print(i)

print()



# n = f.signals_in_file
# signal_labels = f.getSignalLabels()
# sigbufs = np.zeros((n, f.getNSamples()[0]))
# for i in np.arange(n):
#         sigbufs[i, :] = f.readSignal(i)

# print()
# print(np.min(sigbufs))
# print(sigbufs[:, 10])

# # print(f.getPatientName())
# # print(f.getPatientCode())
# # print(f.getBirthdate())
# # print(f.getStartdatetime())

# # sample_freqs = f.getSampleFrequencies()

# # for s in signal_labels:
# #     print(s)

# # for sample_freq in sample_freqs:
# #     print(sample_freq)

# f.close()

# # f = pyedflib.EdfWriter('test.edf', 1, file_type=pyedflib.FILETYPE_EDF)
# # f.setBirthdate(date(1951, 8, 2))
# # f.close()

# # f = pyedflib.EdfReader('test.edf')

# # f.close()

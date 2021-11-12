import pyedflib
from datetime import datetime, date

file_name = 'OUT_FILES/testeeg1.edf'

f = pyedflib.EdfReader(file_name)

n = f.signals_in_file
signal_labels = f.getSignalLabels()



# print(f.getSignalHeaders()[0])
print(f.getHeader())

# print(f.getPatientName())
# print(f.getPatientCode())
# print(f.getBirthdate())
# print(f.getStartdatetime())

# sample_freqs = f.getSampleFrequencies()

# for s in signal_labels:
#     print(s)

# for sample_freq in sample_freqs:
#     print(sample_freq)

f.close()

# f = pyedflib.EdfWriter('test.edf', 1, file_type=pyedflib.FILETYPE_EDF)
# f.setBirthdate(date(1951, 8, 2))
# f.close()
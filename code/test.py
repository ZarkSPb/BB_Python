import pyedflib

file_name = 'EDF/testeeg.edf'

f = pyedflib.EdfReader(file_name)

n = f.signals_in_file
signal_labels = f.getSignalLabels()

print(f.getHeader())

# print(f.getPatientName())
# print(f.getPatientCode())
# print(f.getBirthdate())
# print(f.getStartdatetime())

sample_freqs = f.getSampleFrequencies()

for s in signal_labels:
    print(s)

for sample_freq in sample_freqs:
    print(sample_freq)

f.close()
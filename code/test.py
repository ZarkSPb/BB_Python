import pyedflib

file_name = 'EDF/testeeg.edf'

f = pyedflib.EdfReader(file_name)

n = f.signals_in_file
signal_labels = f.getSignalLabels()

print(f.getPatientName())
print(f.getPatientCode())
print(f.getBirthdate())
print(f.getStartdatetime())


for s in signal_labels:
    print(s)

f.close()
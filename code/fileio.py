import pyedflib
from numpy import loadtxt, zeros, arange


def read_CSV(file_name):
    delim = ';'
    file_structure = {}
    with open(file_name) as f:
        file_structure['first_name'] = f.readline().rstrip().lstrip('#')
        file_structure['last_name'] = f.readline().rstrip().lstrip('#')
        file_structure['data'] = f.readline().rstrip().lstrip('#')
        file_structure['time'] = f.readline().rstrip().lstrip('#')
        f_flag = f.readline().rstrip().lstrip('#')
        header = f.readline().rstrip().lstrip('#').split(delim)

    file_structure['filtered_flag'] = True if f_flag == 'filtered' else False
    file_structure['ch_names'] = [i.split(',')[0] for i in header[:-2]]
    file_structure['table'] = loadtxt(file_name, delimiter=delim).T

    return file_structure


def read_EDF(file_name):
    f = pyedflib.EdfReader(file_name)
    header = f.getHeader()

    d_t = f.getStartdatetime()
    file_structure = {
        'first_name': header['patientname'],
        'last_name': header['patient_additional'],
        'data': d_t.date(),
        'time': d_t.time(),
        'filtered_flag': False if f.getPrefilter(0) == '' else True,
        'ch_names': f.getSignalLabels()
    }

    print(file_structure)

    n = len(file_structure['ch_names'])
    sigbufs = zeros((n, f.getNSamples()[0]))
    for i in arange(n):
        sigbufs[i, :] = f.readSignal(i)
    file_structure['table'] = sigbufs

    return file_structure
from numpy import loadtxt

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
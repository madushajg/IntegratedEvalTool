import pandas as pd
import os

# root_path = os.path.normpath(os.getcwd() + os.sep + os.pardir) + '/Resources'
# os.chdir(root_path)


def get_columns(fname):
    df = pd.read_csv(fname, nrows=0, sep='\t', delimiter=None, header='infer', names=None,
                     index_col=None, encoding="ISO-8859-1")

    attributes_real = df.columns.str.split(',')

    attr_list = []
    count = 1

    for col in attributes_real[0]:
        col_mod = str(col).strip().lower().replace(' ', '_').replace('(', '').replace(')', '')
        pair = [col, col_mod, 'column'+str(count)]
        attr_list.append(pair)
        count += 1

    return attr_list


def get_file_name(fn):
    fn_mod = fn.strip().lower().replace(' ', '_').replace('(', '').replace(')', '')
    file_name = [[fn_mod, fn, 'dataset']]

    return file_name


def get_only_columns(fname):
    df = pd.read_csv(fname, nrows=0, sep='\t', delimiter=None, header='infer', names=None,
                     index_col=None, encoding="ISO-8859-1")

    attributes_real = df.columns.str.split(',')

    return attributes_real[0]

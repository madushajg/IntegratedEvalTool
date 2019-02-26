from pprint import pprint
import read_attributes
from collections import defaultdict


data_dict = defaultdict(list)
# file_path = '/media/madusha/DA0838CA0838A781/PC_Interface/Resources/'
file_path = '/media/arshad/Data/FYP/FYP/UserSpecs2PseudoCode/PC_Interface/Resources/'
file_name = ''


def find_filename(fn):
    global file_name
    file_name = fn


def create_dict():
    att = read_attributes.get_only_columns(file_path+file_name)

    att_dict = {}

    for a in range(len(att)):
        att_dict['column' + str(a + 1)] = att[a]
        att_dict['attribute' + str(a + 1)] = att[a]
        att_dict['feature' + str(a + 1)] = att[a]
        att_dict[str(a + 1)] = att[a]
        att_dict[att[a]] = att[a]
        att_dict[att[a].lower()] = att[a]
        att_dict[att[a].replace('_', ' ')] = att[a]
        att_dict[att[a].replace(' ', '_')] = att[a]

    return att_dict


def create_indexed_dict():
    att = read_attributes.get_only_columns(file_path+file_name)

    att_dict = {}

    for a in range(len(att)):
        att_dict['column' + str(a + 1)] = a+1
        att_dict['attribute' + str(a + 1)] = a+1
        att_dict['feature' + str(a + 1)] = a+1
        att_dict[str(a + 1)] = a+1
        att_dict[att[a]] = a+1
        att_dict[att[a].lower()] = a+1
        att_dict[att[a].replace('_', ' ')] = a+1
        att_dict[att[a].replace(' ', '_')] = a+1
    return att_dict



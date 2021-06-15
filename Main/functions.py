import os
from pathlib import Path
import pandas as pd
from functools import reduce


def find_folders(xpath):

    result = []
    listdir = os.listdir(xpath)
    print('ListDIR', listdir)

    '''
    for filename in listdir:  # loop through all the files and folders
        if os.path.isdir(
                os.path.join(os.path.abspath("."), filename)):  # check whether the current object is a folder or not
            result.append(filename)
    '''

    for filename in listdir:  # loop through all the files and folders
        if os.path.isdir(xpath / filename):  # check whether the current object is a folder or not
            result.append(filename)
    result.sort()

    return result


def find_files(xpath):

    result = []
    listdir = os.listdir(xpath)
    for filename in listdir:  # loop through all the files and folders
        if os.path.isfile(xpath / filename):  # check whether the current object is a file
            result.append(filename)
    result.sort()

    return result


def df_concat_reducer(df_list):
    return reduce(lambda left, right: pd.concat([left, right], axis=0, sort=False), df_list)


# print(find_folders('.'))
# print('done')
#print(find_files(Path('.')))


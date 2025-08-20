
import math
import os
import pandas as pd
import numpy as np


def check_measurement_cat(size_b):
    """
    convert and round the data object size (given in byte) into exponential number
    e.g. input 800 (800 byte data object size) -> output is 1 (1 kilobyte)
    e.g. input 1800 (1800 byte data object size) -> output is 10 (10 kilobyte)
    e.g. input 99999 (99999 byte data object size) -> output is 100 (100 kilobyte)
    :param size_b:
    :return:
    """
    try:
        if size_b == 0:
            return 0 #or 0, depending on desired behavior.
        exponent = math.ceil(math.log10(size_b))
        rounded_data= 10 ** exponent
        data_k=math.ceil(rounded_data/1000)
        return data_k
    except ValueError:
        return 0

def get_measurement(test_path,test_file,timestamp=False) -> pd.DataFrame:
    """
    :param test_path:
    :param test_file:
    :param timestamp: the time of the recorded reaction at the flow cell
    :return: dataframe of potential (I), voltage (V), and timestamp (T) if it is explicitly selected.
    """
    file_name = test_file.strip('.txt')
    file_path = os.path.join(test_path, test_file)
    IV_df = pd.read_csv(file_path, sep='\t')
    columns=IV_df.columns.tolist()
    final_df = IV_df[['I', 'Ewe']]
    if timestamp:
        if 't' in columns:
            final_df['t']= IV_df['t']
        else:
            print('Error: timestamp column not found in IV_df')
    return final_df

def get_measurement_size(df):
    return int(df.memory_usage(index=False).sum())


def duplicate_IV_measurement(IV_df,repeats):
    df = pd.DataFrame(IV_df.values.repeat(repeats, axis=0), columns=IV_df.columns)
    return df

def extract_measurement_parameters(df,columns):
    #TODO read IV dataframe features from columns

    if len(columns) == 2:
        final_df=df[['I', 'Ewe']]
    elif len(columns)==3: # in case timestamp is requested
        final_df=df[['t','I', 'Ewe']]
    return final_df
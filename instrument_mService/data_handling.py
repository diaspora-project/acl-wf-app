
import math
import os
import pandas as pd
import numpy as np


def check_measurement_cat(size_b):
    try:
        if size_b == 0:
            return 0 #or 0, depending on desired behavior.
        exponent = math.ceil(math.log10(size_b))
        rounded_data= 10 ** exponent
        data_k=math.ceil(rounded_data/1000)
        return data_k
    except ValueError:
        return 0

def get_measurement(test_path,test_file):
    file_name = test_file.strip('.txt')
    file_path = os.path.join(test_path, test_file)
    IV_df = pd.read_csv(file_path, sep='\t')
    return IV_df

def get_measurement_size(df):
    return int(df.memory_usage(index=False).sum())

def extract_measurement_parameters(df):
    Ewe = np.array(df.Ewe).reshape(-1, 1)
    I = np.array(df.I).reshape(-1, 1)
    return I,Ewe
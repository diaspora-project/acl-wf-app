import Pyro4
import os
import sys
import time
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.SERIALIZER = "pickle"

ipAddressServer='192.168.1.242'
connectionPort='5001'

def get_IV_dataset():
    """
    three types of returned I-V datasets:
    1- lst_IV_datasets(): return just dataset file names (default)
    2- lst_IV_datasets(pathInclude=True): return datasets with relative paths
    3- lst_IV_datasets(pathInclude=True,type='absolute'): return datasets with absolute paths
    """
    try:
        modules_call = Pyro4.core.Proxy('PYRO:Pyro_Server@' + ipAddressServer + ':' + connectionPort)
        IV_datasets= modules_call.lst_IV_datasets(pathInclude=True)
        print("\n".join(IV_datasets))
    except Exception as e:
        print(e.args)


def call_Shutdown():
    try:
        modules_call = Pyro4.core.Proxy('PYRO:Pyro_Server@' + ipAddressServer + ':' + connectionPort)
        modules_call.shutdown()
        modules_call._pyroRelease()
    except Exception as e:
        print(e.args)


#call_Pyro_test_call()

get_IV_dataset()

call_Shutdown()
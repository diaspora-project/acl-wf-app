import Pyro4
import os
import sys
import time
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from workflow_services import allocate_inference_service,prepare_endpoints_for_inference

Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.SERIALIZER = "pickle"

ipAddressServer='127.0.0.1'
connectionPort='443'

g_endpoint={
    'device':'wombat','gid':'f9f73d0b-72f1-435c-8a07-319b85452ed8','hostname':'pivot03cp.ccs.ornl.gov',
    'classifier_path':'/ccsopen/home/4ua/.globus_compute/acl_ace_ep_wombat_slurm/acl_dependencies/ml_models_dir',
    'sys_path':'/ccsopen/home/4ua/.globus_compute/acl_ace_ep_wombat_slurm/acl_dependencies',
    'training_path':'/ccsopen/home/4ua/.globus_compute/acl_ace_ep_wombat_slurm/acl_dependencies/training_profiles','mode':'gce','timeout':0}


def get_IV_dataset():
    """
    three types of returned I-V datasets:
    1- lst_IV_datasets(): return just dataset file names (default)
    2- lst_IV_datasets(pathInclude=True): return datasets with relative paths
    3- lst_IV_datasets(pathInclude=True,type='absolute'): return datasets with absolute paths
    """
    try:
        modules_call = Pyro4.core.Proxy('PYRO:Pyro_Server@' + ipAddressServer + ':' + connectionPort)
        IV_datasets= modules_call.lst_IV_dataset(pathInclude=True)
        print("\n".join(IV_datasets))
    except Exception as e:
        print(e.args)

def get_IV_data(fileName) ->pd.DataFrame:
    try:
        modules_call = Pyro4.core.Proxy('PYRO:Pyro_Server@' + ipAddressServer + ':' + connectionPort)
        IV_df= modules_call.get_IV_measurement(fileName)
        print(IV_df)
        print(len(IV_df['I']))

    except Exception as e:
        print(e.args)
    return IV_df


def call_Shutdown():
    try:
        modules_call = Pyro4.core.Proxy('PYRO:Pyro_Server@' + ipAddressServer + ':' + connectionPort)
        modules_call.shutdown()
        modules_call._pyroRelease()
    except Exception as e:
        print(e.args)



get_IV_dataset()

fileName_w_path= 'instrument_mService\I-V_data\Test_Ferrocene_normal_s01.txt'
IV_df=get_IV_data(fileName_w_path)
fileName_w_path=os.path.basename(fileName_w_path)[:-4]
I=np.array(IV_df.I).reshape(-1,1)
Ewe=np.array(IV_df.Ewe).reshape(-1,1)
prepare_endpoints_for_inference(g_endpoint)

allocate_inference_service(fileName_w_path,I, Ewe, g_endpoint)
# print("\n##################    Inference Allocation for Testing I-V profile      #################################")
# rc, statuses, i_probe_t,y_pred,profile_class,elapsed_time = allocate_inference_service(ep_gce, I, Ewe, g_endpoint)
#
#
# call_Shutdown()
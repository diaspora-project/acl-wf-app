import Pyro4
import os
import sys
import pandas as pd
import numpy as np
import yaml

from workflow_services import allocate_inference_service,prepare_endpoints_for_inference

Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.SERIALIZER = "pickle"

# to run workflow_orchestration.py via cmd
## python workflow_orchestration.py ipServerAddress=127.0.0.1 connectionPort=443 gendpoint=./workflow_orchestrator_mService/endpoint01.yaml



def get_VI_measurement_parameters():
    try:
        input_parameters = input("Enter IV measurement file, projected size and timestamp(default: blank) ").split(' ')
        # example
        # instrument_mService\I-V_data\Test_Ferrocene_disconnect_working_s01.txt 8000 True
        # or
        # instrument_mService\I-V_data\Test_Ferrocene_disconnect_working_s01.txt
        if len(input_parameters) == 1:
            fileName_w_path = input_parameters[0]
            size = None
            timestamp = False
        elif len(input_parameters) == 2:
            fileName_w_path = input_parameters[0]
            size = int(input_parameters[1])
            timestamp = False
        elif len(input_parameters) == 3:
            fileName_w_path = input_parameters[0]
            size = int(input_parameters[1])
            timestamp = {"true": True, "false": False}.get(input_parameters[2].strip().lower())
        else:
            raise ValueError("Invalid number of parameters and/or type")
    except ValueError as e:
        # Handle the raised ValueError
        print(f"Caught an error: {e}")

    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"An unexpected error occurred: {e}")
    return fileName_w_path, size, timestamp


def get_IV_dataset():
    """
    three types of returned I-V datasets:
    1- lst_IV_datasets(): return just dataset file names (default)
    2- lst_IV_datasets(pathInclude=True): return datasets with relative paths
    3- lst_IV_datasets(pathInclude=True,type='absolute'): return datasets with absolute paths
    """
    try:
        modules_call = Pyro4.core.Proxy('PYRO:Pyro_Server@' + ipAddressServer + ':' + connectionPort)
        IV_dataset, dataset_size= modules_call.lst_IV_dataset(pathInclude=True)
        for i in range(len(IV_dataset)):
            print(f'{IV_dataset[i]}: size: {dataset_size[i]} bytes')
    except Exception as e:
        print(e.args)

def get_IV_data(fileName,size=None,timestamp=False) ->pd.DataFrame:
    try:
        modules_call = Pyro4.core.Proxy('PYRO:Pyro_Server@' + ipAddressServer + ':' + connectionPort)
        IV_df= modules_call.get_IV_measurement(fileName,size,timestamp)
        print(IV_df)
        #print(len(IV_df['I']))

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


if __name__ == '__main__':
    #ARGS
    # ipAddressServer='127.0.0.1'
    # connectionPort='443'
    # with open('./workflow_orchestrator_mService/endpoint01.yaml', 'r') as file:
    #     g_endpoint = yaml.safe_load(file)
    ipAddressServer=(sys.argv[1]).split('=')[1]
    connectionPort=(sys.argv[2]).split('=')[1]
    g_endpoint_file=(sys.argv[3]).split('=')[1]
    with open(g_endpoint_file, 'r') as file:
         g_endpoint = yaml.safe_load(file)


    get_IV_dataset()
    fileName_w_path, size, timestamp = get_VI_measurement_parameters()
    IV_df = get_IV_data(fileName_w_path, size, timestamp)
    fileName_w_path = os.path.basename(fileName_w_path)[:-4]
    I = np.array(IV_df.I).reshape(-1, 1)
    Ewe = np.array(IV_df.Ewe).reshape(-1, 1)
    prepare_endpoints_for_inference(g_endpoint)

    print("\n##################    Inference Allocation for Testing I-V profile      #################################")
    i_probe_t, y_pred, profile_class, elapsed_time = allocate_inference_service(fileName_w_path, I, Ewe, g_endpoint)
    print(f" IV Profile {fileName_w_path} is \
             {('Normal') if profile_class else ('Invalid')}")
    call_Shutdown()
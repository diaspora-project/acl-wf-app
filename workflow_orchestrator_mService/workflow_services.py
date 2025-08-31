from datetime import time
import os
import time

import numpy as np
import concurrent.futures
import warnings

from globus_compute_sdk import Executor
from globus_compute_sdk import Client

warnings.filterwarnings("ignore", category=UserWarning, module="globus_compute_sdk.sdk.client")
from globus_compute_sdk.serialize import CombinedCode
gcc = Client(code_serialization_strategy=CombinedCode())



v_probe=np.linspace(0.2,0.8,10).reshape(-1, 1) # 1-1 should be aligned with scan rate range



def prepare_endpoints_for_inference(g_e_p):
    #TODO helloword checking
    def helloworld_gep(sys_path):
        import sys
        sys.path.append(sys_path)
        from ml_models_for_normality_check import helloworld
        rcv = helloworld('Hello')
        return rcv

    with Executor(endpoint_id=g_e_p['gid'], amqp_port=443,client=gcc) as gce:
        # ... then submit for execution, ...
        future = gce.submit(helloworld_gep,g_e_p['sys_path'])
        rcv = future.result()
        print(future.result())
        print(f"Received {rcv} from {g_e_p['gid']} worker at {g_e_p['device']}")



def Classify_IV_profile(Ewe,I,v_probe,sys_path,EoT_Classifier_Path):
    import os, sys
    sys.path.append(sys_path)
    EoT_Classifier = "clf.pckl"
    from ml_models_for_normality_check import call_normalize_and_analyze_CV_profile
    try:
        i_probe, y_pred, ml_status, elapsed_time = call_normalize_and_analyze_CV_profile(Ewe, I, v_probe,
                                                                                         EoT_Classifier_Path,                                                                                 EoT_Classifier)
    except Exception as e:
        raise
    return i_probe, y_pred, ml_status, elapsed_time


def allocate_inference_service(fileName_w_path,I, Ewe, g_e_p, statuses=None, verbose=False):

    endpoint_id=g_e_p['gid']
    sys_path    = g_e_p['sys_path']
    cl_path     = g_e_p['classifier_path']
    device      = g_e_p['device']   # Used as key to track status
    mode        = g_e_p['mode']
    my_timeout  = g_e_p['timeout']    # Bound remote function
    max_bound   = my_timeout          # Bound local commands

    # ... then create the executor, ...
    with Executor(endpoint_id=endpoint_id, amqp_port=443,client=gcc) as gce:
        # ... then submit for execution, ...
        future = gce.submit(Classify_IV_profile, Ewe, I, v_probe, sys_path, cl_path)
        #print(future.result())
        i_probe, y_pred, profile_class,elapsed_exe_time = future.result()
        print(f" IV Profile {fileName_w_path} is \
         {('Normal') if profile_class else ('Invalid')}")




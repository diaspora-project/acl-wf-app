import numpy as np
import random
import os
from biologic_sp200_config import SP200_Technique_params

########################################################
########################################################
# server connection ip and port
#ipAddressServer = '10.2.11.161'
ipAddressServer = '10.2.11.20'
connectionPort='9090'

########################################################
########################################################
# Data trasnfer methods and related paths
profiles_via_data_channel=False # Default is false

# Note: Paths, may be different based on the channel sent through.
# For example, the testing data paths on the client and server are different if the data_channel is used.
# The measurements collected on the server/instrument cotroller should point to its local directory. 
# The client runs on a remote system accesses the measurements across a mounted directory which its path is different. 

####################
# Paths at the cleint side if measurements are sent via the control Channel (using Pyro)

EoT_Classifier_Path = "./Workflow_dependencies/ml_models_dir"
training_data_path = "./Workflow_dependencies/training_profiles"
testing_data_path="./Workflow_dependencies/testing_profiles"

# Create the directories if they are not exist. 
# Make sure you place the traing samples in the training_profiles for the first time.
os.makedirs(EoT_Classifier_Path, exist_ok=True) # create EoT_Classifier_Path if it is not exist
os.makedirs(training_data_path, exist_ok=True) # create training_data_path if it is not exist
os.makedirs(testing_data_path, exist_ok=True) # create testing_data_path if it is not exist



# ML Configuration
v_probe=np.linspace(SP200_Technique_params['technique']['Voltage_step_E']['E2'],\
                    SP200_Technique_params['technique']['Voltage_step_E']['E1'],\
                    10).reshape(-1, 1) # 1-1 )sholud be aligned with scan rate range

# Classifier file name
EoT_Classifier = "clf.pckl"

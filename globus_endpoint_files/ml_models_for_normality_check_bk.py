# ML Analytical Functions

import os
import pickle
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from workflow_config import *


from sklearn.model_selection import cross_val_score, KFold,cross_val_predict,cross_validate
from sklearn.metrics import precision_score, recall_score, f1_score,accuracy_score,\
classification_report,confusion_matrix,mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier

 
    
###################################################################
###################################################################
def call_GPR_for_probing(_X,_y_target,x_probe):
    
    # GPR
    #1) _X  samples matrix. It represents the voltage potential (Ewe).
    #2) _y target values thqat represents the current (I).
    #3) x_probe: a vector of random potential samples in the range of CV Scan_Rate.
    #4) _X and _y are usually expected to be numpy arrays or equivalent array-like data types,
    # though some estimators work with other formats such as sparse matrices.
    cross_val=cross_val_score
    GPR=GaussianProcessRegressor()

    GPR.fit(_X,_y_target)
    scores = cross_val(GPR, _X,_y_target,cv=5)
    _y_pred = GPR.predict(_X)
    GPR_mse = mean_squared_error(_y_target,_y_pred,squared=True)  

    i_probe=GPR.predict(x_probe)
    
    # print( "V_range: min:  {:.4f} , max: {:.4f}".format(_X.min(0)[0],_X.max(0)[0]))
    # print("Mean cross-validataion score: %.2f" % scores.mean())
    # print("MSE: %f" % GPR_mse)
    # print("RMSE: %f" % np.sqrt(GPR_mse))
    
    return i_probe,_y_pred


###########################################################
###########################################################
def GPR_for_CV_feature_extraction(training_data_path,v_probe):    
    i_probe_lst=[]
    for root, dirs, files in os.walk(training_data_path):
        file_cnt=0;
        for file in files:
            if file.endswith('.txt'):
                print(file)
                i_probe_rcrd={}
                df = pd.read_csv(os.path.join(root,file),sep='\t')
                a=np.array(df.Ewe).reshape(-1,1)
                b=np.array(df.I).reshape(-1,1)
                i_probe_buff,_=call_GPR_for_probing(a,b,v_probe)
                file_cnt=file_cnt+1;
                i_probe_rcrd['indx']=file
                i_probe_rcrd['data']=i_probe_buff.flatten()
                i_probe_lst.append(i_probe_rcrd)
    return i_probe_lst
        
    
#############################################################
#############################################################
def call_assign_classes(i_probe_lst):
    # Assign Classes to the training data set
    # Classes represent "Valid" and "invalid" tests. 
    # These are based on a signituare included in the file name of how they are collected.
               
            
    for i in range(len(i_probe_lst)):
        #if 'GOOD' in i_probe_lst[i]['indx']:
        if ('good' or 'normal' or 'valid') in i_probe_lst[i]['indx'].lower():
            i_probe_lst[i]['class']=1
        else:
            i_probe_lst[i]['class']=0

    return i_probe_lst

###########################################################
###########################################################
def call_RF(_X,_y_target):    
   
    clf = RandomForestClassifier()
    clf.fit(_X,_y_target)

    #scores = cross_val(clf, _X,_y_target)
    y_pred=clf.predict(_X)
    #print("Mean cross-validataion score: %.2f" % scores.mean())
    cm=confusion_matrix(_y_target,y_pred)
    return clf,cm


    

###########################################################
###########################################################
def call_Train_n_Serialize_RF_Classifier(i_probe_lst,EoT_Classifier_Path, EoT_Classifier):

    # Train a classifer with the probing/extrapolated measurement
    X=np.array([list(i_probe_lst[i]['data']) for i in range(len(i_probe_lst))])
    #y=np.reshape(pd.DataFrame(i_probe_lst)['class'].to_numpy(), (-1, 1))
    
    y=pd.DataFrame(i_probe_lst)['class'].to_numpy()
    clf_trained,conf_mat=call_RF(X,y)
    #print('confusion_matrix\n',conf_mat) 

    # Serialize and store the classifier
    ofile=open(os.path.join(EoT_Classifier_Path, EoT_Classifier),'wb')
    pickle.dump(clf_trained,ofile)
    ofile.close()
    #return str(os.path.join(EoT_Classifier_Path, EoT_Classifier))
    return 0
    
    
    
   
def call_analyze_CV_profile(i_probe,EoT_Classifier_Path, EoT_Classifier):
    # De-serialize and load the classifier
    clf_retrieved=pickle.load(open(os.path.join(EoT_Classifier_Path, EoT_Classifier),'rb'))
    ml_status=clf_retrieved.predict(i_probe.reshape(1, -1))
    return ml_status[0]

def call_normalize_and_analyze_CV_profile(i_probe,Ewe,I,v_probe,EoT_Classifier_Path, EoT_Classifier):
    # Extract i_probe of testing profile
    i_probe,y_pred=call_GPR_for_probing(Ewe,I,v_probe)
    i_probe=i_probe.reshape(-1,1)
    y_pred=y_pred.reshape(-1,1)	

    # De-serialize and load the classifier
    clf_retrieved=pickle.load(open(os.path.join(EoT_Classifier_Path, EoT_Classifier),'rb'))
    ml_status=clf_retrieved.predict(i_probe.reshape(1, -1))
    return i_probe,y_pred,ml_status[0]



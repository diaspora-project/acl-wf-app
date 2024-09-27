
# Bio-logic SP200 firmware configuration
SP200_config_params={}
SP200_config_params['address']= "USB0"
SP200_config_params['channel'] = 1
SP200_config_params['timeout'] = 10
SP200_config_params['verbosity'] = 3
SP200_config_params['load_firmware'] = True
SP200_config_params['fpga_path']= "vmp_iv_0395_aa.xlx"
SP200_config_params['firmware_path'] = "kernel4.bin"
SP200_config_params['binary_path'] = "C:/EC-Lab Development Package/EC-Lab Development Package/"

#Bio-logic SP200_Cyclic Voltammetry(CV) technique setting
SP200_Technique_params={} # General params shared with all techniques
SP200_Technique_params['E_range'] = 'E_RANGE_2_5V'
SP200_Technique_params['I_range'] = 'I_RANGE_AUTO'
SP200_Technique_params['Bandwidth'] = 'BW_8'
SP200_Technique_params['tb'] = 0.000045   # in second(S)
SP200_Technique_params['technique']={} # Specific params to CV technique
SP200_Technique_params['technique']['type']='cv'
SP200_Technique_params['technique']['bin_tech_file']= "cv4.ecc" # cv4 because SP200 is in SP300 family
SP200_Technique_params['technique']['Voltage_step_E'] = {'Ei':0.0,'E1':0.8,'E2':0.2,'Ef':0.0}    # in volt(V)
SP200_Technique_params['technique']['vs_initial']=[True,False,False,True,True]
SP200_Technique_params['technique']['Scan_Rate']=[0.02]*5
SP200_Technique_params['technique']['cv_Scan_number'] = 2
SP200_Technique_params['technique']['cv_Record_every_dE'] = 0.002    # in volt(V) # dEN
SP200_Technique_params['technique']['cv_Average_over_dE'] = True
SP200_Technique_params['technique']['cv_N_Cycles'] = 0
SP200_Technique_params['technique']['cv_Begin_measuring_I'] = 0.5     # in percent(%)
SP200_Technique_params['technique']['cv_End_measuring_I'] = 1.0       # in percent(%)



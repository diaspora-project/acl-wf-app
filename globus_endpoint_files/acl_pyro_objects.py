# Cleint-Server Pyro objects
import Pyro4
import os
import sys
import pickle


# for metrics:
# https://scikit-learn.org/stable/modules/model_evaluation.html


Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.SERIALIZER = "pickle"


class ACL_Pyro_Client:
    def __init__(self,ipAddressServer,connectionPort):
        self._connection = Pyro4.core.Proxy('PYRO:ACL_Workstation@' + ipAddressServer + ':' + connectionPort)

    ###################################################
    #########     J-Kem Setup Pyro Objects   ########## 
    ###################################################
    def call_Initialize_JKem_API(self,Serial_Port_MetaData):
        self._connection.Initialize_JKem_API(Serial_Port_MetaData)
        print('J-Kem Initialization is done')
    def call_Activate_JKem_API(self):
        stats=self._connection.Activate_JKem_API()
        print('J-Kem Activation is done')
        #print(stats)
    def call_Exit_JKem_API(self):
        stats=self._connection.Exit_JKem_API()
        print(f'{self.call_Exit_JKem_API.__name__}: {stats}')
        
        
    def Set_Rate_FlowController(self,address,rate):
        stats=self._connection.Set_Rate_Flow_Control(address,rate)
        print(f'{self.Set_Rate_FlowController.__name__}: {stats}')

    
    def Set_Home_FractionCollector(self):
        stats=self._connection.Set_Home_Fraction_Collector()
        print(f'{self.Set_Home_FractionCollector.__name__}: {stats}')
    def Set_Waste_FractionCollector(self):
        stats=self._connection.Set_Waste_Fraction_Collector()
        print(f'{self.Set_Waste_FractionCollector.__name__}: {stats}')
    def Set_Position_FractionCollector(self,position):
        stats=self._connection.Position_Fraction_Collector(position)
        print(f'{self.Set_Position_FractionCollector.__name__}: {stats}')
    def Set_Vial_FractionCollector(self,vial,position):
        stats=self._connection.Set_Vial_Fraction_Collector(vial,position)
        print(f'{self.Set_Vial_FractionCollector.__name__}: {stats}')
    
    def FractionCollector_Rack(self,rack_name):
        stats=self._connection.Set_Fraction_Collector_Rack(rack_name)
        print(f'{self.FractionCollector_Rack.__name__}: {stats}')
    
    
    def Set_Rate_SyringePump(self,address,rate):
         stats=self._connection.Set_Rate_Syringe_Pump(address,rate) 
         time.sleep(3)
         print(f'{self.Set_Rate_SyringePump.__name__}: {stats}')
    def Set_Port_SyringePump(self,address,port):
            stats=self._connection.Set_Port_Syringe_Pump(address,port)
            if 'Error' in stats:
                stats=self._connection.Set_Port_Syringe_Pump(address,port)
            print(f'{self.Set_Port_SyringePump.__name__}: {stats}')
    def Dispense_SyringePump(self,address,volume,rate):
         stats=self._connection.Dispense_Syringe_Pump(address,volume)
         time.sleep((volume/rate)*60)
         print(f'{self.Dispense_SyringePump.__name__}: {stats}')
    def Withdraw_SyringePump(self,address,volume,rate):
        stats=self._connection.Withdraw_Syringe_Pump(address,volume)
        time.sleep((volume/rate)*60)
        print(f'{self.Withdraw_SyringePump.__name__}: {stats}')
    def Fill_SyringePump(self,address):
        stats=self._connection.Fill_Syringe_Pump(address)
        print(f'{self.Fill_SyringePump.__name__}: {stats}')
    def Set_Home_SyringePump(self,address):
         stats=self._connection.Set_Home_Syringe_Pump(address)
         print(f'{self.Set_Home_SyringePump.__name__}: {stats}')
    def IsReady_SyringePump(self,address):
        stats=self._connection.IsReady_Syringe_Pump(address)
        print(f'{self.IsReady_SyringePump.__name__}: {stats}')
        
        
    def Set_Rate_PeristalticPump(self,address,speed):
         stats=self._connection.Set_Rate_Peristaltic_Pump(address,speed)
         print(f'{self.Set_Rate_PeristalticPump.__name__}: {stats}')
    def Set_Direction_PeristalticPump(self,address,direction):
        stats=self._connection.Set_Direction_Peristaltic_Pump(address,direction)
        print(f'{self.Set_Direction_PeristalticPump.__name__}: {stats}')
    def Dispense_PeristalticPump(self,address,volume):
        stats=self._connection.Dispense_Peristaltic_Pump(address,volume)
        print(f'{self.Dispense_PeristalticPump.__name__}: {stats}')
    def Stop_PeristalticPump(self,address):
         stats=self._connection.Stop_Peristaltic_Pump(address)  
         print(f'{self.Stop_PeristalticPump.__name__}: {stats}')
    
    
    def Probe_solution_pH(self,temperature):
        
        stats=self._connection.Get_pH(temperature)
        print(f'{self.Probe_solution_pH.__name__}: {stats}')
        
    
    def Chiller_SetPoint(self,temperature):
        stats=self._connection.Chiller_SetPoint(temperature)
        print(f'{self.Chiller_SetPoint.__name__}: {stats}')
    def Start_Chiller(self):
        stats=self._connection.Start_Chiller()
        print(f'{self.Start_Chiller.__name__}: {stats}')
    def Stop_Chiller(self):
        stats=self._connection.Stop_Chiller()
        print(f'{self.Stop_Chiller.__name__}: {stats}')
    def Probe_Internal_Stats_Chiller(self):
        stats=self._connection.Get_Internal_Stats_Chiller()
        print(f'{self.Probe_Internal_Stats_Chiller.__name__}: {stats}')
    def Probe_External_Stats_Chiller(self):
        stats=self._connection.Get_External_Stats_Chiller()
        print(f'{self.Probe_External_Stats_Chiller.__name__}: {stats}')
        
        
    def Temperature_SetPoint(self,address,temperature):
        stats=self._connection.Temperature_SetPoint(address,temperature)
        print(f'{self.Temperature_SetPoint.__name__}: {stats}')
    def Probe_Temperature(self,address):
        stats=self._connection.Get_Temprature_Stats(address)
        print(f'{self.Probe_Temperature.__name__}: {stats}')
    def Probe_Temperature_Power(self,address,percentage):
        stats=self._connection.Get_Temprature_Power(address,percentage)
        print(f'{self.Probe_Temperature_Power.__name__}: {stats}')

            
    def Set_Electrode_Out(self):
        stats=self._connection.Set_Electrode_Out()
        print(f'{self.Set_Electrode_Out.__name__}: {stats}')
    def Set_Electrode_Home(self):
        stats=self._connection.Set_Electrode_Home()
        print(f'{self.Set_Electrode_Home.__name__}: {stats}')
        
    ###################################################
    #########       SP200 Pyro Objects      ########### 
    ###################################################
    def call_Initialize_SP200_API(self,SP200_config_params):
            self._connection.Initialize_SP200_API(SP200_config_params)
            print('Initialization is done')
    
    def call_Connect_SP200(self):
                self._connection.Connect_SP200()
                print('Channel connection is done')
    
    def call_Load_Firmware_SP200(self):
            self._connection.Load_Firmware_SP200()
            print()

    def call_Start_Channel_SP200(self):
            self._connection.Start_Channel_SP200()
            print('Channel is started for probing measurement')
    
    def call_Stop_Channel_SP200(self):
            self._connection.Stop_Channel_SP200()
            print('Channel is stopped')
    
    def call_Disconnect_SP200(self):
            self._connection.Disconnect_SP200()
            print('Channel is disconnected')

    def call_Shutdown_SP200(self):
            self._connection.shutdown()
            self._connection._pyroRelease()
            
   
    def call_Get_Measurement_SP200(self,Workflow_Path_Rslt,profiles_via_data_channel):
        iv_file_name,iv_profile=self._connection.Get_Measurement_SP200(Workflow_Path_Rslt,profiles_via_data_channel)
        print('Measurements are collected')
        
        if not profiles_via_data_channel: # it means the profiles are transferred as opject via Pyro and gonna be saved on the client side.
            CV_data=pickle.loads(iv_profile)
            CV_data.to_csv(f'{Workflow_Path_Rslt}\{iv_file_name}', sep='\t')
        return iv_file_name
        
    
    ## Potentiostat Technique configuration
    def call_Initialize_CV_Tech_SP200(self,SP200_Technique_params):
        self._connection.Initialize_CV_Tech_SP200(SP200_Technique_params)
        print('Technique is initialized')
        
    def call_Load_Technique_SP200(self):
        self._connection.Load_Technique_SP200(first=True, last=True, display=False)
        print('Loading technique is done')
        
    ## Auxiliary functions
    def call_Print_Params_SP200(self):
            self._connection.Print_SP200_Params()

    def call_Is_Connect_SP200(self):
            return self._connection.Is_Connected_SP200()

    def call_Print_Messages_SP200(self):
            return self._connection.Print_Messages_SP200()

    def call_Get_Channel_Info_SP200(self):
            return self._connection.Get_Channel_Info_SP200()
        
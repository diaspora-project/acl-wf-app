import Pyro4
import sys
import pickle
import time

Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.SERIALIZER = "pickle"

from helpers import Helpers
from sp200 import SP200_API
from jkem_api import JKem_API

mypath = "C:\EC-Lab Development Package\Examples\Python"
sys.path.insert(0, mypath)

from kbio.c_utils import c_is_64b
from kbio.tech_types import TECH_ID

ipAddressServer = '10.2.11.161'
connectionPort = '9090'


@Pyro4.expose
class ACL_Pyro_Server(object):  #Embedded_SP200 --> ACL_Pyro
    def __init__(self, daemon):
        self.daemon = daemon

    #############################################################################################
    ###                         Pyro objects for J-Kem setup
    #############################################################################################

    def Initialize_JKem_API(self,SerailPort_MetaData):
        JKem_API._Initialize_Serial_port(SerailPort_MetaData)
        print(f' J-Kem Initialization done!!')

    def Activate_JKem_API(self):
        stats = JKem_API.Activate_JKem_setup()
        print(f'{self.Activate_JKem_API.__name__}: {stats}')
        return stats
    def Exit_JKem_API(self):
        stats= JKem_API.Exit_JKem_setup()
        print(f'{self.Exit_JKem_API.__name__}: {stats}')
        return stats


    def Set_Rate_Flow_Control(self,addr,rate):
        stats= JKem_API.Flow_Controller_Rate(addr,rate)
        print(f'{self.Set_Rate_Flow_Control.__name__}: {stats}')
        return stats


    def Set_Home_Fraction_Collector(self):
        stats= JKem_API.Fraction_Collector_Home()
        print(f'{self.Set_Home_Fraction_Collector.__name__}: {stats}')
        return stats
    def Set_Waste_Fraction_Collector(self):
        stats= JKem_API.Fraction_Collector_Waste()
        print(f'{self.Set_Waste_Fraction_Collector.__name__}: {stats}')
        return stats
    def Position_Fraction_Collector(self,pos):
        stats= JKem_API.Fraction_Collector_Advance(pos)
        print(f'{self.Position_Fraction_Collector.__name__}: {stats}')
        return stats
    def Set_Vial_Fraction_Collector(self,vial,pos):
        stats= JKem_API.Fraction_Collector_Vial(vial,pos)
        print(f'{self.Set_Vial_Fraction_Collector.__name__}: {stats}')
        return stats
    def Set_Fraction_Collector_Rack(self,rack_name):
        stats= JKem_API.Fraction_Collector_Rack(rack_name)
        print(f'{self.Set_Fraction_Collector_Rack.__name__}: {stats}')
        return stats


    def Set_Rate_Syringe_Pump(self,addr,rate):
        stats= JKem_API.Syringe_Pump_Rate(addr,rate)
        print(f'{self.Set_Rate_Syringe_Pump.__name__}: {stats}')
        return stats
    def Set_Port_Syringe_Pump(self,addr,port):
        stats= JKem_API.Syringe_Pump_Port(addr,port)
        print(f'{self.Set_Port_Syringe_Pump.__name__}: {stats}')
        return stats
    def Dispense_Syringe_Pump(self,addr,vol):
        stats= JKem_API.Syringe_Pump_Dispense(addr,vol)
        print(f'{self.Dispense_Syringe_Pump.__name__}: {stats}')
        return stats
    def Withdraw_Syringe_Pump(self,addr,vol):
        stats= JKem_API.Syringe_Pump_Withdraw(addr,vol)
        print(f'{self.Withdraw_Syringe_Pump.__name__}: {stats}')
        return stats
    def Fill_Syringe_Pump(self,addr):
        stats= JKem_API.Syringe_Pump_Fill(addr)
        print(f'{self.Fill_Syringe_Pump.__name__}: {stats}')
    def Set_Home_Syringe_Pump(self,addr):
        stats= JKem_API.Syringe_Pump_Home(addr)
        print(f'{self.Set_Home_Syringe_Pump.__name__}: {stats}')
        return stats
    def IsReady_Syringe_Pump(self,addr):
        stats= JKem_API.Syringe_Pump_IsReady(addr)
        print(f'{self.IsReady_Syringe_Pump.__name__}: {stats}')
        return stats


    def Set_Rate_Peristaltic_Pump(self,addr,speed):
        stats= JKem_API.Peristaltic_Pump_Rate(addr,speed)
        print(f'{self.Set_Rate_Peristaltic_Pump.__name__}: {stats}')
        return stats
    def Set_Direction_Peristaltic_Pump(self,addr,direction):
        stats= JKem_API.Peristaltic_Pump_Direction(addr,direction)
        print(f'{self.Set_Direction_Peristaltic_Pump.__name__}: {stats}')
        return stats
    def Dispense_Peristaltic_Pump(self,addr,vol):
        stats= JKem_API.Peristaltic_Pump_Dispense(addr,vol)
        print(f'{self.Dispense_Peristaltic_Pump.__name__}: {stats}')
        return stats
    def Stop_Peristaltic_Pump(self,addr):
        stats= JKem_API.Peristaltic_Pump_Stop(addr)
        print(f'{self.Stop_Peristaltic_Pump.__name__}: {stats}')
        return stats


    def Get_pH(self,temp):
        stats= JKem_API.pH_Probe(temp)
        print(f'{self.Get_pH.__name__}: {stats}')
        return stats
    ###################################################################
    ##################################################################
    def Chiller_SetPoint(self,temp):
        stats=JKem_API.PolyScience_Chiller_SetPoint(temp)
        print(f'{self.Chiller_SetPoint.__name__}: {stats}')
        return stats

    def Start_Chiller(self):
        stats=JKem_API.PolyScience_Chiller_Start()
        print(f'{self.Start_Chiller.__name__}: {stats}')
        return stats

    def Stop_Chiller(self):
        stats=JKem_API.PolyScience_Chiller_Stop()
        print(f'{self.Stop_Chiller.__name__}: {stats}')
        return stats

    def Get_Internal_Stats_Chiller(self):
        stats=JKem_API.PolyScience_Chiller_Get_Internal()
        print(f'{self.Get_Internal_Stats_Chiller.__name__}: {stats}')
        return stats

    def Get_External_Stats_Chiller(self):
        stats=JKem_API.PolyScience_Chiller_Get_External()
        print(f'{self.Get_External_Stats_Chiller.__name__}: {stats}')
        return stats

    def Temperature_SetPoint(self,addr,temp):
        stats=JKem_API.Temperature_SetPoint(addr,temp)
        print(f'{self.Temperature_SetPoint.__name__}: {stats}')
        return stats

    def Get_Temprature_Stats(self,addr):
        stats = JKem_API.Get_Temperature(addr)
        print(f'{self.Get_Temprature_Stats.__name__}: {stats}')
        return stats


    def Get_Temprature_Power(self,addr,percentage):
        stats=JKem_API.Temperature_Power(addr,percentage)
        print(f'{self.Get_Temprature_Power.__name__}: {stats}')
        return stats

    def Set_Electrode_Out(self):
        stats = JKem_API.Electrode_Out()
        print(f'{self.Set_Electrode_Out.__name__}: {stats}')
        return stats

    def Set_Electrode_Home(self):
        stats = JKem_API.Electrode_Home()
        print(f'{self.Set_Electrode_Home.__name__}: {stats}')
        return stats
    #############################################################################################
    ###                         Pyro objects for SP200
    #############################################################################################
    def Initialize_SP200_API(self, SP200_config_params):
        SP200_API._initialize_API(c_is_64b,SP200_config_params)
        print(f'Initialization done!!')

    # BL_Connect
    def Connect_SP200(self):
        SP200_API.BL_Connect_dev ()
        print(f'Connection to the Potentiostat is Done')

    # Connection Status
    def Is_Connected_SP200(self):
        #print(f'{self.Is_Connected_SP200.__name__} is called')
        return SP200_API.BL_Test_Connection()

    # Load_Firmware
    def Load_Firmware_SP200(self):
        SP200_API.load_Firmware()
        print("Loading frimware is done !!")

    # BL_GetMessage
    def Print_Messages_SP200(self):
        #print(f'{self.Print_Messages_SP200.__name__} is called')
        sp200_msg = SP200_API.BL_print_messages()
        print(sp200_msg)
        return str(sp200_msg)

    def Get_Channel_Info_SP200(self):
        #print(f'{self.Get_Channel_Info_SP200.__name__} is called')
        #print(f"> Channel {self.SP200_config_params['channel']} info :")
        channel_info = SP200_API.BL_Get_channel_info()
        print(channel_info)
        return str(channel_info)




    def Initialize_CV_Tech_SP200(self, SP200_Technique_params):
        # Initializing CV_parameters
        ecc_parms = SP200_API.BL_Initialize_CV_parameters(SP200_Technique_params)
        print(f'Technique initialization is done !!')





    def Load_Technique_SP200(self, first, last, display):
        SP200_API.BL_LoadTechnique(first, last, display)
        print(f'Loading technique is done !!')

    # Start Channel
    def Start_Channel_SP200(self):
        SP200_API.BL_Start_Channel()
        print(f'Channel connection is initiated')

    def Stop_Channel_SP200(self):
        SP200_API.BL_Stop_Channel()
        print(f'Channel connection is stopped')

    # BL_Disconnect
    def Disconnect_SP200(self):
        SP200_API.BL_Disconnect()
        print(f'Potentiostat is disconnected')

    # Get Measurements
    def Get_Measurement_SP200(self, Path_Rslt, data_channel=False):
        """
        Return
        (default) send IV measurements over the control channel over Pyro
        if data_channel is False. Otherwise, store the measurements and share the file id.
        data is gonna be transferred over the data channel through file mounting or One Drive.
        """
        CV_data = SP200_API.BL_Data_Acquisition()
        print(f'Measurement is collected')
        file_name = f'cv_data_cvs_{time.strftime("%Y%m%d_%H_%M_%S")}.txt'
        if not data_channel:  # it means the measurements gonna be transferred via the control channel (via Pyro)
            return file_name, pickle.dumps(CV_data)
        else:
            # save the data based on the Path_Rslt
            CV_data.to_csv(f'{Path_Rslt}\{file_name}', sep='\t')
            return file_name, ''

    # Get API version
    def Get_Lib_Version(self):
        version=SP200_API.Get_LibVersion()
        print(version)
        return version

    # Get USB Info
    def Get_USB_Dev_Info(self,id):
        info=SP200_API.BL_Get_USB_device_infos(id)
        print (info)
        return info


    # @Pyro4.oneway
    def shutdown(self):
        print(f'Ecosystem communication session is terminated ')
        self.daemon.shutdown()


daemon = Pyro4.Daemon(host=ipAddressServer, port=int(connectionPort))
call_pyro_ps200_class = ACL_Pyro_Server(daemon)
uri = daemon.register(call_pyro_ps200_class, objectId='ACL_Workstation')
print(ACL_Pyro_Server)
print(f'\turi = {uri}')
print('Pyro daemon running.')
time.sleep(5)
daemon.requestLoop()
daemon.close()
print('daemon closed')

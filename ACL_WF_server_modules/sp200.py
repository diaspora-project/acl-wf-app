


import pandas as pd
import time
import sys

from helpers import Helpers

mypath = "C:\EC-Lab Development Package\Examples\Python"
sys.path.insert(0, mypath)

import kbio.kbio_types as KBIO
from kbio.kbio_api import KBIO_api
from kbio.c_utils import c_is_64b
from kbio.utils import exception_brief
from dataclasses import dataclass
from kbio.tech_types import TECH_ID
from kbio.kbio_tech import ECC_parm, make_ecc_parm, make_ecc_parms



#==============================================================================#
# Bio-Logic(BL) SP200 Instrument Steering functions
#==============================================================================#


class SP200_API:
    # TODO: move the self attributes related to ACL_Pyro_Server class to this class, including:
    #  1- self.SP200_config_params
    #  2- self.API
    #  3- self.id_
    #  4- self.device_info
    #  5- self.SP200_Technique_params
    #  6- self.ecc_parms

    SP200_config_params=dict()
    SP200_Technique_params=dict()
    SP200_API=None
    SP200_id=None
    SP200_device_info=None
    ecc_parms=None

    def __init__(self):
        pass
    @staticmethod
    def _firmware_config(c_is_64b,path):
        """
        determine library file according to Python version (32b/64b)
        """
        if c_is_64b:  # firmware application type
            print("> 64b application")
            DLL_file = "EClib64.dll"
        else:
            print("> 32b application")
            DLL_file = "EClib.dll"
        return path + DLL_file

    @staticmethod
    def _initialize_API(c_is_64b,SP200_config_params):
        SP200_API.SP200_config_params=SP200_config_params
        BL_package_path=SP200_API.SP200_config_params['binary_path']
        api_dll_path = SP200_API._firmware_config(c_is_64b, BL_package_path)
        SP200_API.SP200_API=KBIO_api(api_dll_path)

    @staticmethod
    def BL_Connect_dev():
        SP200_API.SP200_id, SP200_API.device_info =SP200_API.SP200_API.Connect\
           (
           SP200_API.SP200_config_params['address'],
           SP200_API.SP200_config_params['timeout']
           )

    @staticmethod
    def BL_Test_Connection():
        return True if SP200_API.SP200_API.TestConnection(SP200_API.SP200_id) else False

    @staticmethod
    def load_Firmware():
        """
        Connect to SP200 device which its address is already defined.
        """
        SP_200_firmware_path=SP200_API.SP200_config_params['firmware_path']
        SP_200_fpga_path=SP200_API.SP200_config_params['fpga_path']
        load_firmware=SP200_API.SP200_config_params['load_firmware']
        # create a map from channel set
        channel_map = SP200_API.SP200_API.channel_map({SP200_API.SP200_config_params['channel']})
        print(f"> Loading {SP_200_firmware_path} ...")
        # BL_LoadFirmware
        SP200_API.SP200_API.LoadFirmware(SP200_API.SP200_id, channel_map, firmware=SP_200_firmware_path, fpga=SP_200_fpga_path,
                            force=load_firmware)
        print("> ... firmware loaded")


    @staticmethod
    def BL_print_messages():
        while True:
            msg = SP200_API.SP200_API.GetMessage(SP200_API.SP200_id, SP200_API.SP200_config_params['channel'])
            if not msg: break
            return msg

    @staticmethod
    def BL_Get_channel_info(BL_ch_lst=None):
        print(f"> Channel {SP200_API.SP200_config_params['channel']} info :")
        if BL_ch_lst:
            # test whether the configured channel exists
            if SP200_API.SP200_config_params['channel'] not in BL_ch_lst:
                print(f"Configured channel {SP200_API.SP200_config_params['channel']} does not belong to device channels {BL_ch_lst}")
                sys.exit(-1)
        return SP200_API.SP200_API.GetChannelInfo(SP200_API.SP200_id, SP200_API.SP200_config_params['channel'])


    @staticmethod
    def BL_Initialize_CV_parameters(SP200_Technique_params):
        SP200_API.SP200_Technique_params=SP200_Technique_params


        @dataclass
        # Construct parameter list as a Data Structure
        class Voltage_step:
            Voltage: float
            ScanRate: float
            vsinitial: bool = True

        CV_parms = {
            'vs_initial': ECC_parm("vs_initial", bool),
            'Voltage_step': ECC_parm("Voltage_step", float),
            'Scan_Rate': ECC_parm("Scan_Rate", float),
            'Scan_number': ECC_parm("Scan_number", int),
            'Record_every_dE': ECC_parm("Record_every_dE", float),
            'Average_over_dE': ECC_parm("Average_over_dE", bool),
            'N_Cycles': ECC_parm("N_Cycles", int),
            'Begin_measuring_I': ECC_parm("Begin_measuring_I", float),
            'End_measuring_I': ECC_parm("End_measuring_I", float),
            'E_Range': ECC_parm("E_Range", int),
            'I_Range': ECC_parm("I_Range", int),
            'Bandwidth': ECC_parm("Bandwidth", int),
            'tb': ECC_parm('tb', float)
        }


        # defines DS parameters
        steps = [
            Voltage_step(SP200_API.SP200_Technique_params['technique']['Voltage_step_E']['Ei'], SP200_API.SP200_Technique_params['technique']['Scan_Rate'][0], SP200_API.SP200_Technique_params['technique']['vs_initial'][0]),
            Voltage_step(SP200_API.SP200_Technique_params['technique']['Voltage_step_E']['E1'], SP200_API.SP200_Technique_params['technique']['Scan_Rate'][1], SP200_API.SP200_Technique_params['technique']['vs_initial'][1]),
            Voltage_step(SP200_API.SP200_Technique_params['technique']['Voltage_step_E']['E2'], SP200_API.SP200_Technique_params['technique']['Scan_Rate'][2], SP200_API.SP200_Technique_params['technique']['vs_initial'][2]),
            Voltage_step(SP200_API.SP200_Technique_params['technique']['Voltage_step_E']['Ei'], SP200_API.SP200_Technique_params['technique']['Scan_Rate'][3], SP200_API.SP200_Technique_params['technique']['vs_initial'][3]),
            Voltage_step(SP200_API.SP200_Technique_params['technique']['Voltage_step_E']['Ef'], SP200_API.SP200_Technique_params['technique']['Scan_Rate'][4], SP200_API.SP200_Technique_params['technique']['vs_initial'][4])
        ]

        # BL_Define CV Parameters
        ecc_parm_Scan_number = make_ecc_parm(SP200_API.SP200_API, CV_parms['Scan_number'],
                                             SP200_API.SP200_Technique_params['technique']['cv_Scan_number'])
        ecc_parm_Record_every_dE = make_ecc_parm(SP200_API.SP200_API, CV_parms['Record_every_dE'],
                                                 SP200_API.SP200_Technique_params['technique']['cv_Record_every_dE'])
        ecc_parm_Average_over_dE = make_ecc_parm(SP200_API.SP200_API, CV_parms['Average_over_dE'],
                                                 SP200_API.SP200_Technique_params['technique']['cv_Average_over_dE'])
        ecc_parm_N_Cycles = make_ecc_parm(SP200_API.SP200_API, CV_parms['N_Cycles'],
                                          SP200_API.SP200_Technique_params['technique']['cv_N_Cycles'])
        ecc_parm_Begin_measuring = make_ecc_parm(SP200_API.SP200_API, CV_parms['Begin_measuring_I'],
                                                 SP200_API.SP200_Technique_params['technique']['cv_Begin_measuring_I'])
        ecc_parm_End_measuring_I = make_ecc_parm(SP200_API.SP200_API, CV_parms['End_measuring_I'],
                                                 SP200_API.SP200_Technique_params['technique']['cv_End_measuring_I'])
        ecc_parm_E_range = make_ecc_parm(SP200_API.SP200_API, CV_parms['E_Range'],
                                         KBIO.E_RANGE[SP200_API.SP200_Technique_params['E_range']].value)
        ecc_parm_I_range = make_ecc_parm(SP200_API.SP200_API, CV_parms['I_Range'],
                                         KBIO.I_RANGE[SP200_API.SP200_Technique_params['I_range']].value)
        ecc_parm_Bandwidth = make_ecc_parm(SP200_API.SP200_API, CV_parms['Bandwidth'],
                                           KBIO.BANDWIDTH[SP200_API.SP200_Technique_params['Bandwidth']].value)
        ecc_parm_timebase = make_ecc_parm(SP200_API.SP200_API, CV_parms['tb'], SP200_API.SP200_Technique_params['tb'])

        ecc_parm_steps = list()

        for indx, step in enumerate(steps):
            parm = make_ecc_parm(SP200_API.SP200_API, CV_parms['Voltage_step'], step.Voltage, indx)
            ecc_parm_steps.append(parm)
            parm = make_ecc_parm(SP200_API.SP200_API,  CV_parms['Scan_Rate'], step.ScanRate, indx)
            ecc_parm_steps.append(parm)
            parm = make_ecc_parm(SP200_API.SP200_API, CV_parms['vs_initial'], step.vsinitial, indx)
            ecc_parm_steps.append(parm)

        ecc_parms = make_ecc_parms(SP200_API.SP200_API, *ecc_parm_steps, ecc_parm_Scan_number, ecc_parm_Record_every_dE, \
                                   ecc_parm_Average_over_dE, ecc_parm_N_Cycles, ecc_parm_Begin_measuring, \
                                   ecc_parm_End_measuring_I, ecc_parm_E_range, ecc_parm_I_range, \
                                   ecc_parm_Bandwidth, ecc_parm_timebase
                                   )

        SP200_API.ecc_parms=ecc_parms

    @staticmethod
    def BL_LoadTechnique(first_bool, last_bool, display_param):
        SP200_API.SP200_API.LoadTechnique \
            (SP200_API.SP200_id, SP200_API.SP200_config_params['channel'],SP200_API.SP200_Technique_params['technique']['bin_tech_file'], SP200_API.ecc_parms,
             first=first_bool, last=last_bool, display=display_param)

    @staticmethod
    def BL_Start_Channel():
        SP200_API.SP200_API.StartChannel(SP200_API.SP200_id, SP200_API.SP200_config_params['channel'])

    @staticmethod
    def BL_Stop_Channel():
        SP200_API.SP200_API.StopChannel(SP200_API.SP200_id, SP200_API.SP200_config_params['channel'])


    @staticmethod
    def BL_Disconnect():
        SP200_API.SP200_API.Disconnect(SP200_API.SP200_id)
        print(f"> disconnected from device[{SP200_API.SP200_config_params['channel']}]")

    @staticmethod
    def Extract_Data(data_df):
        raw_cv_data = SP200_API.SP200_API.GetData(SP200_API.SP200_id, SP200_API.SP200_config_params['channel'])
        current_values, data_info, data_record = raw_cv_data
        status_code = current_values.State
        status_id = KBIO.PROG_STATE(status_code).name
        tech_name = TECH_ID(data_info.TechniqueID).name

        print("> data record :")
        print(data_record)

        ix = 0
        for _ in range(data_info.NbRows):

            if tech_name == 'CV':

                inx = ix + data_info.NbCols
                t_high, t_low, *row = data_record[ix:inx]

                nb_words = len(row)
                if nb_words != 3:
                    raise RuntimeError(f"{tech_name} : unexpected record length ({nb_words})")

                # Current is a float
                I = SP200_API.SP200_API.ConvertNumericIntoSingle(row[0])

                # Ewe is a float
                Ewe = SP200_API.SP200_API.ConvertNumericIntoSingle(row[1])

                # technique cycle is an integer
                Cycle = row[2]

                # compute timestamp in seconds
                t_rel = (t_high << 32) + t_low
                t = data_info.StartTime + current_values.TimeBase * t_rel

                parsed_row = {'t': t, 'Ewe': Ewe, 'I': I, 'Cycle': Cycle}
                parsed_row_pd = pd.DataFrame([parsed_row])
                data_df = pd.concat([data_df, parsed_row_pd], ignore_index=True)

            ix = inx

        return status_id, data_df

    @staticmethod
    def BL_Data_Acquisition():

        cv_data_df = pd.DataFrame(columns=['t', 'I', 'Ewe', 'Cycle'])
        while True:
            status, cv_data_df = SP200_API.Extract_Data(cv_data_df)
            print(cv_data_df)

            if status == 'STOP':
                break
            time.sleep(1)

        print("> experiment done")
        # print(cv_data_df)

        Helpers._newline()
        return cv_data_df

    @staticmethod
    def Get_LibVersion():
        return SP200_API.SP200_API.GetLibVersion()

    @staticmethod
    def BL_Get_USB_device_infos(index):
        """Print device information at USB index, if any."""
        try:
            info = SP200_API.SP200_API.USB_DeviceInfo(index)
            print(f"> USB{index} info : {info}")
            return info
        except Exception as e:
            print(f"> USB{index} info : {e}")


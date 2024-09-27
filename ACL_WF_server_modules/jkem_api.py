
import sys
import serial
import time





#==============================================================================#
# J-Kem Instruments' Steering functions
#==============================================================================#
class JKem_API:
    Serial_Port_MetaData=dict
    Serial_Port=None
    def __init__(self):
        pass

    @staticmethod
    def _Initialize_Serial_port(SP_Meta:dict):
        print(SP_Meta)
        JKem_API.Serial_Port_MetaData=SP_Meta
        JKem_API.Serial_Port=serial.Serial()
        JKem_API.Serial_Port.port = JKem_API.Serial_Port_MetaData['port']
        JKem_API.Serial_Port.baudrate =JKem_API.Serial_Port_MetaData['baudrate']
        JKem_API.Serial_Port.timeout  =JKem_API.Serial_Port_MetaData['timeout']
        JKem_API.Serial_Port.parity   =eval(JKem_API.Serial_Port_MetaData['parity'])
        JKem_API.Serial_Port.stopbits =JKem_API.Serial_Port_MetaData['stopbits']
        JKem_API.Serial_Port.bytesize =JKem_API.Serial_Port_MetaData['bytesize']
        JKem_API.Serial_Port.rtscts   =JKem_API.Serial_Port_MetaData['rtscts']
        JKem_API.Serial_Port.xonxoff  =JKem_API.Serial_Port_MetaData['xonxoff']
        JKem_API.Serial_Port.dsrdtr = JKem_API.Serial_Port_MetaData['dsrdtr']
        #JKem_API.Serial_Port.write_timeout =JKem_API.Serial_Port_MetaData['write_timeout']
        #JKem_API.Serial_Port.inter_byte_timeout=JKem_API.Serial_Port_MetaData['inter_byte_timeout']

    @staticmethod
    def Activate_JKem_setup():
        JKem_API.Serial_Port.open()
        #JKem_API.Serial_Port.write(b'READY\r\n')
        JKem_API.Serial_Port.write(b'READY\r')
        #time.sleep(1)
        stat = JKem_API.Serial_Port.readline().decode('ascii').strip('\r')
        print('Activation:',stat)
        return stat

    @staticmethod
    def Exit_JKem_setup():
        JKem_API.Serial_Port.write(b'Master.Exit()\r')
        #time.sleep(1)
        stat = JKem_API.Serial_Port.readline().decode('ascii').strip('\r')
        JKem_API.Serial_Port.close()
        return stat

    @staticmethod
    def Flow_Controller_Rate(address: int,rate: float):
        """
        address: address of the flow controller instrument being commanded
        rate: flow rate in ml/min
        """
        command=('FlowController.Rate(%d,%f)' %(address,rate)).encode()
        JKem_API.Serial_Port.write(command+b'\r')
        #time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Fraction_Collector_Home():
        JKem_API.Serial_Port.write(b'FractionCollector.Home()\r')
        #time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Fraction_Collector_Waste():
        JKem_API.Serial_Port.write(b'FractionCollector.Waste()\r')
        #time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Fraction_Collector_Advance(position:str):
        """
        Position - Indicates the position in the vial where the needle should be positioned.
           The two options are “TOP” and “BOTTOM”. Generally, if fluid is being dispensed to
            the vial, the position should be set to TOP, and if it is being withdrawn
             from the vial the position should be set to BOTTOM.
        """
        command = ('FractionCollector.Advance(%s)' %position ).encode()
        JKem_API.Serial_Port.write(command+b'\r')
        #time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Fraction_Collector_Rack(rack_name: str):
        """
        Specifies the rack id at the fraction collector to be in use
        """
        command = ('FractionCollector.Rack(%s)' % (rack_name)).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        # time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Fraction_Collector_Vial(vial_number: int, position: str):
        """
        Vial – The vial number to move to in the specified rack.
        Position -  Indicates the position in the vial where the needle should be positioned.
           The two options are “TOP” and “BOTTOM”.   Generally, if fluid is being dispensed
            to the vial, the position should be set to TOP, and if it is being withdrawn
             from the vial the position should be set to BOTTOM.
        """
        command = ('FractionCollector.Vial(%d,%s)' % (vial_number, position)).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        # time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Syringe_Pump_Rate(address:int,rate:float):
        """
        Address – The address of the desired pump.  Range: 1 or 2.
        Rate -  The flow rate of the pump.
        """
        command = ('Syringepump.rate(%d,%f)' % (address,rate)).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        #time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Syringe_Pump_Port(address:int,port:int):
        """
        Address – The address of the desired pump.  Range: 1 or 2.
        Port – The position on the pumps distribution valve to move to. Range: 1 to 8.
        """
        command = ('Syringepump.port(%d,%d)' % (address,port)).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        #time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Syringe_Pump_Dispense(address:int,volume:float):
        """
        Address – The address of the desired pump.  Range: 1 or 2.
        Volume – The volume to dispense. The volume cannot exceed the current volume
         in the syringe, if it .does, the pump simply delivers it current volume and
          then stops. Volume is in units of ml.
        """
        command = ('Syringepump.dispense(%d,%f)' % (address,volume)).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        #time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Syringe_Pump_Withdraw(address: int, volume: float):
        """
        Address – The address of the desired pump.  Range: 1 or 2.
        Volume – The volume to withdraw. The volume cannot exceed the size of the syringe.
        Volume is in units of ml.
        """
        command = ('Syringepump.withdraw(%d,%f)' % (address, volume)).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        #time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Syringe_Pump_Fill(address: int):
        """
        Address – The address of the desired pump.  Range: 1 or 2.
        Volume – The volume to withdraw. The volume cannot exceed the size of the syringe.
        Volume is in units of ml.
        """
        command = ('SyringePump.Fill(%d)' %address).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        #time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Syringe_Pump_Home(address: int):
        """
        Address – The address of the desired pump.  Range: 1 or 2.
        Causes the pump to dispense the current content of the syringe.
           When you want to dispense all of the solvent in the syringe,
            HOME is a better option than using DISPENSE
        """
        command = ('Syringepump.home(%d)' %address).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        #time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Syringe_Pump_IsReady(address: int):
        """
        Address – The address of the desired pump.  Range: 1 or 2.
        Queries whether the pump is currently in a state to receive a new motion command.
        """
        command = ('SyringePump.IsReady(%d)' % address).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        #time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Peristaltic_Pump_Rate(address:int,speed:float):
        """
        Address – The address of the pump being commanded.
        Speed – A floating point value between the minimum and the maximum flow rate range.
        Rate is sent in units of ml/min.
        """
        command = ('PeristalticPump.Rate(%d,%f)' % (address, speed)).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        #time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Peristaltic_Pump_Direction(address:int,direction:str):
        """
        Address – The address of the pump being commanded.
        Direction – CLOCKWISE or COUNTERCLOCKWISE
        Determines whether the pump head rotates in a clockwise or counter clockwise direction
        """
        command = ('PeristalticPump.Direction(%d,%s)' % (address, direction)).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        #time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Peristaltic_Pump_Dispense(address:int,volume:float):
        """
        Address – The address of the desired pump.  Range: 1 or 2.
        Volume is the volume of solvent to dispense at the pumps currently set rate.
          then stops. Volume is in units of ml.
        """
        command = ('PeristalticPump.Dispense(%d,%f)' % (address,volume)).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        #time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Peristaltic_Pump_Stop(address: int):
        """
        Address – The address of the desired pump.  Range: 1 or 2.
        Immediately causes a running pump to stop.
        """
        command = ('PeristalticPump.Stop(%d)' %address).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        #time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def pH_Probe(temp:float):
        """
        Temperature is the temperature of the solution being monitored.  Units are in degrees centigrade.
        The solution pH is returned followed by OK.
        The GetpH command takes about 800 ms to reply.
        """
        command = ('pHProbe.getph(%f)' %temp).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        time.sleep(1.5)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    ##########################################################################################
    #########################################################################################
    @staticmethod
    def PolyScience_Chiller_SetPoint(temp:float):
        """
        Temperature is in degrees centigrade.
        The setpoint temperature is for the chiller.
        The successful return is OK.
        """
        command = ('Chiller.setpoint(%f)' % temp).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        # time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def PolyScience_Chiller_Start():
        """
        Starts the chiller.
        The chiller must have power applied to the unit when this command is sent.
        The successful return is OK.
        """
        JKem_API.Serial_Port.write(b'Chiller.start()\r')
        # time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def PolyScience_Chiller_Stop():
        """
        The chiller immediately stops circulating chiller fluid.
        The successful return is OK.
        """
        JKem_API.Serial_Port.write(b'Chiller.stop()\r')
        # time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def PolyScience_Chiller_Get_Internal():
        """
        This queries the current temperature of the chillers internal bath temperature sensor.
        The reply consists of the internal temperature followed by OK, if successful.
        """
        JKem_API.Serial_Port.write(b'Chiller.Getinternal()\r')
        # time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def PolyScience_Chiller_Get_External():
        """
        If the chiller is equipped with an external temperature sensor,
         this queries the current temperature of the external sensor.
        The reply consists of the external temperature followed by OK, if successful.
        """
        JKem_API.Serial_Port.write(b'Chiller.Getexternal()\r')
        # time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')


    @staticmethod
    def Temperature_SetPoint(address:int,temp: float):
        """
        Temperature is in degrees centigrade.
        Address – The address of the desired digital meter.
            The meter with an address of 1 is a temperature controller
            and the meter with an address of 2 is a temperature monitor.
        Temperature -  The desired temperature to heat to.
        Note:This command is only in effect for the temperature controller on channel 1.
        The successful return is OK.
        """

        command = ('Temperature.Setpoint(%d,%f)' %(address,temp)).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        # time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Get_Temperature(address: int):
        """
        Address – The address of the desired digital meter.
          The meter with an address of 1 is a temperature controller and
          the meter with an address of 2 is a temperature monitor.

        The reply consists of the currently sensed temperature of the addressed meter followed by OK, if successful.
        """

        command = ('Temperature.Gettemperature(%d)' %(address)).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        time.sleep(1.5)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Temperature_Power(address: int,percent:int):
        """

        Address – The address of the desired digital meter.
          The meter with an address of 1 is a temperature controller and
          the meter with an address of 2 is a temperature monitor.
        Percent – The maximum allowable power the temperature controller is allowed to apply to the heater.
          It has a range of 0 to 100.
        This command is only in effect for the temperature controller on channel 1.
        """

        command = ('Temperature.Power(%d,%d)' %(address,percent)).encode()
        JKem_API.Serial_Port.write(command + b'\r')
        #time.sleep(1.5)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Electrode_Out():
        """
        Moves the electrode connection rod to an X-, Z-coordinate pre-programmed to form
         an electrical connection on the electrochemical cell.
        Note: The pre-programmed X- and Z-coordinate that the electrode goes
         to is set in the program running on the tablet.
        The successful return is OK.
        """
        JKem_API.Serial_Port.write(b'Electrode.Out()\r')
        # time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

    @staticmethod
    def Electrode_Home():
        """
        Returns the electrode connector to its home position allowing a robotic arm
         to access the electrode itself
        The successful return is OK.
        """
        JKem_API.Serial_Port.write(b'Electrode.Home()\r')
        # time.sleep(1)
        return JKem_API.Serial_Port.readline().decode('ascii').strip('\r')

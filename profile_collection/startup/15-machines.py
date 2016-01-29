from ophyd import PVPositionerPC, EpicsSignal, EpicsSignalRO
from ophyd import Component as Cpt

# Undulator

class Undulator(PVPositionerPC):
    setpoint = Cpt(EpicsSignal, '-Mtr:2}Inp:Pos')
    readback = Cpt(EpicsSignalRO, '-LEnc}Gap')
    actuate = Cpt(EpicsSignal, '-Mtr:2}Sw:Go')
    actuate_value = 1
    stop_signal = Cpt(EpicsSignal, '-Mtr:2}Pos.STOP')
    stop_value = 1

ivu_gap = Undulator('SR:C11-ID:G1{IVU20:1')

# This class is defined in 10-optics.py
fe = VirtualMotorCenterAndGap('FE:C11A-OP{Slt:12') # Front End Slits (Primary Slits)
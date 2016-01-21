from ophyd import PVPositionerPC

# Undulator

class Undulator(PVPositionerPC):
    setpoint = '-Mtr:2}Inp:Pos',
    readback = '-LEnc}Gap',
    actuate = '-Mtr:2}Sw:Go',
    actuate_value = 1,
    stop='-Mtr:2}Pos.STOP',
    stop_value=1,

ivu_gap = Undulator('SR:C11-ID:G1{IVU20:1')

fe = VirtualMotorCenterAndGap('FE:C11A-OP{Slt:12') # Front End Slits (Primary Slits)

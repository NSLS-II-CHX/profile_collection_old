from ophyd import EpicsMotor, PVPositioner, Device
from ophyd import Component as Cpt, DynamicDeviceComponent as DDC

#gap
#und_gap = 'SR:C11-ID:G1{IVU20:1-Mtr:2}'  #SR:C11-ID:G1{IVU20:1-Mtr:2}Inp:Pos ??


class MotorCenterAndGap(Device):
    xc = Cpt(EpicsMotor, '-Ax:XCtr}Mtr')
    yc = Cpt(EpicsMotor, '-Ax:YCtr}Mtr')
    xg = Cpt(EpicsMotor, '-Ax:XGap}Mtr')
    yg = Cpt(EpicsMotor, '-Ax:YGap}Mtr')


class SlitXGap(PVPositioner):
    setpoint = Cpt(EpicsSignal, 'XF:11IDA-OP{Slt:MB-Ax:X}size')
    readback = Cpt(EpicsSignal, 'XF:11IDA-OP{Slt:MB-Ax:X}t2.C')
    done = Cpt(EpicsSignal, 'XF:11IDA-OP{Slt:MB-Ax:X}DMOV')
	done_value = 1


class SlitXCenter(PVPositioner):
    setpoint = Cpt(EpicsSignal, 'XF:11IDA-OP{Slt:MB-Ax:X}center')
    readback = Cpt(EpicsSignal, 'XF:11IDA-OP{Slt:MB-Ax:X}t2.D')
    done = Cpt(EpicsSignal, 'XF:11IDA-OP{Slt:MB-Ax:X}DMOV')
	done_value = 1


class SlitYGap(PVPositioner):
    setpoint = Cpt(EpicsSignal, 'XF:11IDA-OP{Slt:MB-Ax:Y}size')
    readback = Cpt(EpicsSignal, 'XF:11IDA-OP{Slt:MB-Ax:Y}t2.C')
    done = Cpt(EpicsSignal, 'XF:11IDA-OP{Slt:MB-Ax:Y}DMOV')
	done_value = 1


class SlitXCenter(PVPositioner):
    setpoint = Cpt(EpicsSignal, 'XF:11IDA-OP{Slt:MB-Ax:Y}center')
    readback= Cpt(EpicsSignal, 'XF:11IDA-OP{Slt:MB-Ax:Y}t2.D')
    done = Cpt(EpicsSignal, 'XF:11IDA-OP{Slt:MB-Ax:Y}DMOV')
	done_value = 1


class VirtualMotorCenterAndGap(Device):
    xc = Cpt(SlitXCenter)
    yc = Cpt(SlitYCenter)
    xg = Cpt(SlitXGap)
    yg = Cpt(SltYGap)


class Blades(Device):
    top = Cpt(EpicsMotor, '-Ax:T}Mtr')
    bottom = Cpt(EpicsMotor, '-Ax:B}Mtr')
    outboard = Cpt(EpicsMotor, '-Ax:O}Mtr')
    inboard = Cpt(EpicsMotor, '-Ax:I}Mtr')


class MotorSlits(Blades, MotorCenterAndGap):
    pass

class VirtualMotorSlits(Blades, VirtualMotorCenterAndGap):
    pass


class XYMotor(Device):
    x = Cpt(EpicsMotor, '-Ax:X}Mtr')
    y = Cpt(EpicsMotor, '-Ax:Y}Mtr')


class XYThetaMotor(XYMotor):
    "used for GI mirror"
    theta = Cpt(EpicsMotor, '-Ax:Th}Mtr')


class HorizontalDiffractionMirror(XYMotor):
    "x and y with pitch, which has different read and write PVs"
    p = Cpt(EpicsMotor, read_pv='-Ax:P}E-I', write_pv='-Ax:P}E-SP')



class DCM(Device):
    en = Cpt(EpicsMotor, '-Ax:Energy}Mtr')
    b = Cpt(EpicsMotor, '-Ax:B}Mtr')
    r = Cpt(EpicsMotor, '-Ax:R}Mtr')
    x = Cpt(EpicsMotor, '-Ax:X}Mtr')
    p = Cpt(EpicsMotor, '-Ax:P}Mtr')
    fp = Cpt(EpicsMotor, '-Ax:FP}Mtr')


class DMM(DCM):
    y = Cpt(EpicsMotor, '-Ax:Y}Mtr')  # DCM does not have one


class Transfocator(Device):
    crl = DDC({'num{i}'.format(i): (EpicsMotor, '%d-Ax:X}Mtr' % i)
               for i in range(1, 9)})
    tran_x = Cpt(EpicsMotor, 'Ves-Ax:X}Mtr')
    tran_y = Cpt(EpicsMotor, 'Ves-Ax:Y}Mtr')
    tran_z = Cpt(EpicsMotor, 'Ves-Ax:Z}Mtr')
    tran_ph = Cpt(EpicsMotor, 'Ves-Ax:Ph}Mtr')
    tran_th = Cpt(EpicsMotor, 'Ves-Ax:Th}Mtr')


class Kinoform(Device):
    z = Cpt(EpicsMotor, '-Ax:ZB}Mtr')
    x = Cpt(EpicsMotor, '-Ax:XB}Mtr')
    y = Cpt(EpicsMotor, '-Ax:YB}Mtr')
    chi = Cpt(EpicsMotor, '-Ax:Ch}Mtr')
    theta = Cpt(EpicsMotor, '-Ax:Th}Mtr')
    phi = Cpt(EpicsMotor, '-Ax:Ph}Mtr')
    lx = Cpt(EpicsMotor, '-Ax:XT}Mtr')
    ly = Cpt(EpicsMotor, '-Ax:YT}Mtr')


class Diffractometer(Device):
    gam = Cpt(EpicsMotor, '-Ax:Gam}Mtr')
    om = Cpt(EpicsMotor, '-Ax:Om}Mtr')
    phi = Cpt(EpicsMotor, '-Ax:Ph}Mtr')
    xb = Cpt(EpicsMotor, '-Ax:XB}Mtr')
    yb = Cpt(EpicsMotor, '-Ax:YB}Mtr')
    chh = Cpt(EpicsMotor, '-Ax:ChH}Mtr')
    thh = Cpt(EpicsMotor, '-Ax:ThH}Mtr')
    phh = Cpt(EpicsMotor, '-Ax:PhH}Mtr')
    xh = Cpt(EpicsMotor, '-Ax:XH}Mtr')
    yh = Cpt(EpicsMotor, '-Ax:YH2}Mtr')
    zh = Cpt(EpicsMotor, '-Ax:ZH}Mtr')
    chv = Cpt(EpicsMotor, '-Ax:ChV}Mtr')
    thv = Cpt(EpicsMotor, '-Ax:ThV}Mtr')
    xv = Cpt(EpicsMotor, '-Ax:XV}Mtr')
    yv = Cpt(EpicsMotor, '-Ax:YV}Mtr')
    zv = Cpt(EpicsMotor, '-Ax:ZV}Mtr')
    xv2 = Cpt(EpicsMotor, '-Ax:XV2}Mtr')


diff = Diffractometer('XF:11IDB-ES{Dif')

# sample beamstop
sambst = EpicsMotor('XF:11IDB-OP{BS:Samp')

s1 = MotorCenterAndGap('XF:11IDB-OP{Slt:1', name='s1')
k1 = Kinoform('XF:11IDB-OP{Lens:1', name='k1')  # upstream
k2 = Kinoform('XF:11IDB-OP{Lens:2', 'k2')  # downstream
gi = XYThetaMotor('XF:11IDB-OP{Mir:GI', name='gi')  # GI-mirror
s2 = MotorCenterAndGap('XF:11IDB-OP{Slt:2', name='s2') #Beam-defining (large JJ) slits
pbs = MotorSlits('XF:11IDA-OP{Slt:PB', name='pbs')  # pink beam slits
flt_y = EpicsMotor('XF:11IDA-OP{Flt:1-Ax:Y}Mtr', name='flt_y')  # filters
dcm = DCM('XF:11IDA-OP{Mono:DCM-'), name='dcm')
dmm = DCM('XF:11IDA-OP{Mono:DMM-', name='dmm')
mbs = VirtualMotorSlits('XF:11IDA-OP{Slt:MB', name='mbs')  # Mono-beam Slits
s4 = MotorCenterAndGap('XF:11IDB-ES{Slt:4-Ax:XGap}Mtr', name='s4')  # temp guard slits

# Diagnostic Manipulators
foil_y = EpicsMotor('XF:11IDA-BI{Foil:Bpm-Ax:Y}Mtr', name='foil_y')
bpm = XYMotor('XF:11IDA-BI{Bpm:1-', name='bpm')

w1 = XYMotor('XF:11IDB-OP{Win:1', name='w1')  # window positioners
hdm = HorizontalDiffractionMirror('XF:11IDA-OP{Mir:HDM', name='hdm')
gsl = VirtualMotorCenterAndGap('XF:11IDB-OP{Slt:Guard', name='gs1')  #Guard rSlits (SmarAct)

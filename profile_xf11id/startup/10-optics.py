from ophyd.controls import EpicsMotor, PVPositioner

# HDM
hdm_x = EpicsMotor('XF:11IDA-OP{Mir:HDM-Ax:X}Mtr', name='hdm_x')
hdm_y = EpicsMotor('XF:11IDA-OP{Mir:HDM-Ax:Y}Mtr', name='hdm_y')
hdm_p = PVPositioner('XF:11IDA-OP{Mir:HDM-Ax:P}E-SP',
		     readback='XF:11IDA-OP{Mir:HDM-Ax:P}E-I', name='hdm_p')

# Pink Beam Slits
pbs_xc = EpicsMotor('XF:11IDA-OP{Slt:PB-Ax:XCtr}Mtr', name='pbs_xc')
pbs_xg = EpicsMotor('XF:11IDA-OP{Slt:PB-Ax:XGap}Mtr', name='pbs_xg')
pbs_yc = EpicsMotor('XF:11IDA-OP{Slt:PB-Ax:YCtr}Mtr', name='pbs_yc')
pbs_yg = EpicsMotor('XF:11IDA-OP{Slt:PB-Ax:YGap}Mtr', name='pbs_yg')

# DCM
dcm_b = EpicsMotor('XF:11IDA-OP{Mono:DCM-Ax:B}Mtr', name='dcm_b')
dcm_x = EpicsMotor('XF:11IDA-OP{Mono:DCM-Ax:X}Mtr', name='dcm_x')
dcm_r = EpicsMotor('XF:11IDA-OP{Mono:DCM-Ax:R}Mtr', name='dcm_r')
dcm_p = EpicsMotor('XF:11IDA-OP{Mono:DCM-Ax:P}Mtr', name='dcm_p')
dcm_fp = EpicsMotor('XF:11IDA-OP{Mono:DCM-Ax:FP}Mtr', name='dcm_fp')

# DMM

# Mono-beam Slits

mbs_xg = EpicsMotor('XF:11IDA-OP{Slt:MB-Ax:X}size', name='mbs_xg')
mbs_xc = EpicsMotor('XF:11IDA-OP{Slt:MB-Ax:X}center', name='mbs_xc')
mbs_yg = EpicsMotor('XF:11IDA-OP{Slt:MB-Ax:Y}size', name='mbs_yg')
mbs_yc = EpicsMotor('XF:11IDA-OP{Slt:MB-Ax:Y}center', name='mbs_yc')

# Diagnostic Manipulators
foil_y = EpicsMotor('XF:11IDA-BI{Foil:Bpm-Ax:Y}Mtr', name='foil_y')
bpm_x = EpicsMotor('XF:11IDA-BI{Bpm:1-Ax:X}Mtr', name='bpm_x')
bpm_y = EpicsMotor('XF:11IDA-BI{Bpm:1-Ax:Y}Mtr', name='bpm_y')

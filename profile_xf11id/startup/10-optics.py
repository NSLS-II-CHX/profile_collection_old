from ophyd.controls import EpicsMotor, PVPositioner

# HDM
hdm_x = EpicsMotor('XF:11IDA-OP{Mir:HDM-Ax:X}Mtr')
hdm_y = EpicsMotor('XF:11IDA-OP{Mir:HDM-Ax:Y}Mtr')
hdm_p = PVPositioner('XF:11IDA-OP{Mir:HDM-Ax:P}E-SP',
		     readback='XF:11IDA-OP{Mir:HDM-Ax:P}E-I')

# Pink Beam Slits
pbs_xc = EpicsMotor('XF:11IDA-OP{Slt:PB-Ax:XCtr}Mtr')
pbs_xg = EpicsMotor('XF:11IDA-OP{Slt:PB-Ax:XGap}Mtr')
pbs_yc = EpicsMotor('XF:11IDA-OP{Slt:PB-Ax:YCtr}Mtr')
pbs_yg = EpicsMotor('XF:11IDA-OP{Slt:PB-Ax:YGap}Mtr')

# DCM
dcm_b = EpicsMotor('XF:11IDA-OP{Mono:DCM-Ax:B}Mtr')
dcm_x = EpicsMotor('XF:11IDA-OP{Mono:DCM-Ax:X}Mtr')
dcm_r = EpicsMotor('XF:11IDA-OP{Mono:DCM-Ax:R}Mtr')
dcm_p = EpicsMotor('XF:11IDA-OP{Mono:DCM-Ax:P}Mtr')
dcm_fp = EpicsMotor('XF:11IDA-OP{Mono:DCM-Ax:FP}Mtr')

# DMM

# Mono-beam Slits

mbs_xg = EpicsMotor('XF:11IDA-OP{Slt:MB-Ax:X}size', name='mbs_xg')
mbs_xc = EpicsMotor('XF:11IDA-OP{Slt:MB-Ax:X}center', name='mbs_xc')
mbs_yg = EpicsMotor('XF:11IDA-OP{Slt:MB-Ax:Y}size', name='mbs_yg')
mbs_yc = EpicsMotor('XF:11IDA-OP{Slt:MB-Ax:Y}center', name='mbs_yc')

# Diagnostic Manipulators
foil_y = EpicsMotor('XF:11IDA-BI{Foil:Bpm-Ax:Y}Mtr')
bpm_x = EpicsMotor('XF:11IDA-BI{Bpm:1-Ax:X}Mtr')
bpm_y = EpicsMotor('XF:11IDA-BI{Bpm:1-Ax:Y}Mtr')

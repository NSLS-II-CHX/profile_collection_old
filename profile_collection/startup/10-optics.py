from ophyd.controls import EpicsMotor, PVPositioner

#gap
#und_gap = 'SR:C11-ID:G1{IVU20:1-Mtr:2}'  #SR:C11-ID:G1{IVU20:1-Mtr:2}Inp:Pos ??
 



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

pbs_t = EpicsMotor('XF:11IDA-OP{Slt:PB-Ax:T}Mtr', name='pbs_t')
pbs_b = EpicsMotor('XF:11IDA-OP{Slt:PB-Ax:B}Mtr', name='pbs_b')
pbs_o = EpicsMotor('XF:11IDA-OP{Slt:PB-Ax:O}Mtr', name='pbs_o')
pbs_i = EpicsMotor('XF:11IDA-OP{Slt:PB-Ax:I}Mtr', name='pbs_i')

# Filters
flt_y = EpicsMotor('XF:11IDA-OP{Flt:1-Ax:Y}Mtr', name='flt_y')

# DCM
dcm_en = EpicsMotor('XF:11IDA-OP{Mono:DCM-Ax:Energy}Mtr', name='dcm_en')
dcm_b = EpicsMotor('XF:11IDA-OP{Mono:DCM-Ax:B}Mtr', name='dcm_b')
dcm_x = EpicsMotor('XF:11IDA-OP{Mono:DCM-Ax:X}Mtr', name='dcm_x')
dcm_r = EpicsMotor('XF:11IDA-OP{Mono:DCM-Ax:R}Mtr', name='dcm_r')
dcm_p = EpicsMotor('XF:11IDA-OP{Mono:DCM-Ax:P}Mtr', name='dcm_p')
dcm_fp = EpicsMotor('XF:11IDA-OP{Mono:DCM-Ax:FP}Mtr', name='dcm_fp')

# DMM
dmm_b = EpicsMotor('XF:11IDA-OP{Mono:DMM-Ax:B}Mtr', name='dmm_b')
dmm_r = EpicsMotor('XF:11IDA-OP{Mono:DMM-Ax:R}Mtr', name='dmm_r')
dmm_x = EpicsMotor('XF:11IDA-OP{Mono:DMM-Ax:X}Mtr', name='dmm_x')
dmm_y = EpicsMotor('XF:11IDA-OP{Mono:DMM-Ax:Y}Mtr', name='dmm_y')
dmm_fp = EpicsMotor('XF:11IDA-OP{Mono:DMM-Ax:FP}Mtr', name='dmm_fp')

# Mono-beam Slits

 

mbs_xg = PVPositioner('XF:11IDA-OP{Slt:MB-Ax:X}size',
		      readback='XF:11IDA-OP{Slt:MB-Ax:X}t2.C',
		      done='XF:11IDA-OP{Slt:MB-Ax:X}DMOV',
	              done_val=1,
		      name='mbs_xg')
mbs_xc = PVPositioner('XF:11IDA-OP{Slt:MB-Ax:X}center',
		      readback='XF:11IDA-OP{Slt:MB-Ax:X}t2.D',
		      done='XF:11IDA-OP{Slt:MB-Ax:X}DMOV',
	              done_val=1,
		      name='mbs_xc')
mbs_yg = PVPositioner('XF:11IDA-OP{Slt:MB-Ax:Y}size',
		      readback='XF:11IDA-OP{Slt:MB-Ax:Y}t2.C',
		      done='XF:11IDA-OP{Slt:MB-Ax:Y}DMOV',
	              done_val=1,
		      name='mbs_yg')
mbs_yc = PVPositioner('XF:11IDA-OP{Slt:MB-Ax:Y}center',
		      readback='XF:11IDA-OP{Slt:MB-Ax:Y}t2.D',
		      done='XF:11IDA-OP{Slt:MB-Ax:Y}DMOV',
	              done_val=1,
		      name='mbs_yc')

mbs_b = EpicsMotor('XF:11IDA-OP{Slt:MB-Ax:B}Mtr', name='mbs_b')
mbs_t = EpicsMotor('XF:11IDA-OP{Slt:MB-Ax:T}Mtr', name='mbs_t')
mbs_i = EpicsMotor('XF:11IDA-OP{Slt:MB-Ax:I}Mtr', name='mbs_i')
mbs_o = EpicsMotor('XF:11IDA-OP{Slt:MB-Ax:O}Mtr', name='mbs_o')

# Diagnostic Manipulators
foil_y = EpicsMotor('XF:11IDA-BI{Foil:Bpm-Ax:Y}Mtr', name='foil_y')
bpm_x = EpicsMotor('XF:11IDA-BI{Bpm:1-Ax:X}Mtr', name='bpm_x')
bpm_y = EpicsMotor('XF:11IDA-BI{Bpm:1-Ax:Y}Mtr', name='bpm_y')

# Transfocator
tran_crl1 = EpicsMotor('XF:11IDA-OP{Lens:1-Ax:X}Mtr', name='tran_crl1')
tran_crl2 = EpicsMotor('XF:11IDA-OP{Lens:2-Ax:X}Mtr', name='tran_crl2')
tran_crl3 = EpicsMotor('XF:11IDA-OP{Lens:3-Ax:X}Mtr', name='tran_crl3')
tran_crl4 = EpicsMotor('XF:11IDA-OP{Lens:4-Ax:X}Mtr', name='tran_crl4')
tran_crl5 = EpicsMotor('XF:11IDA-OP{Lens:5-Ax:X}Mtr', name='tran_crl5')
tran_crl6 = EpicsMotor('XF:11IDA-OP{Lens:6-Ax:X}Mtr', name='tran_crl6')
tran_crl7 = EpicsMotor('XF:11IDA-OP{Lens:7-Ax:X}Mtr', name='tran_crl7')
tran_crl8 = EpicsMotor('XF:11IDA-OP{Lens:8-Ax:X}Mtr', name='tran_crl8')
tran_x = EpicsMotor('XF:11IDA-OP{Lens:Ves-Ax:X}Mtr', name='tran_x')
tran_y = EpicsMotor('XF:11IDA-OP{Lens:Ves-Ax:Y}Mtr', name='tran_y')
tran_z = EpicsMotor('XF:11IDA-OP{Lens:Ves-Ax:Z}Mtr', name='tran_z')
tran_ph = EpicsMotor('XF:11IDA-OP{Lens:Ves-Ax:Ph}Mtr', name='tran_ph')
tran_th = EpicsMotor('XF:11IDA-OP{Lens:Ves-Ax:Th}Mtr', name='tran_th')

# Window Positioners
w1_x = EpicsMotor('XF:11IDB-OP{Win:1-Ax:X}Mtr', name='w1_x')
w1_y = EpicsMotor('XF:11IDB-OP{Win:1-Ax:Y}Mtr', name='w1_y')

# Fast Shutter Positioners

# Optics Table


# Beam-defining "pre-kinoform" slits
#XF:11IDB-OP{Slt:1-Ax:XGap}Mtr.DESC
#Name: XF:11IDB-OP{Slt:1-Ax:XCtr}Mtr.DESC
#caput XF:11IDB-OP{Slt:1-Ax:YGap}Mtr.DESC 'Y Gap (s1_yg)'
#caput XF:11IDB-OP{Slt:1-Ax:YCtr}Mtr.DESC 'Y Center (s1_yc)'
s1_xg = EpicsMotor('XF:11IDB-OP{Slt:1-Ax:XGap}Mtr', name='s1_xg')

s1_xc = EpicsMotor('XF:11IDB-OP{Slt:1-Ax:XCtr}Mtr', name='s1_xc')
s1_yg = EpicsMotor('XF:11IDB-OP{Slt:1-Ax:YGap}Mtr', name='s1_yg')
s1_yc = EpicsMotor('XF:11IDB-OP{Slt:1-Ax:YCtr}Mtr', name='s1_yc')

# Kinoform Unit 1 (upstream)
k1_z = EpicsMotor('XF:11IDB-OP{Lens:1-Ax:ZB}Mtr', name='k1_z')
k1_x = EpicsMotor('XF:11IDB-OP{Lens:1-Ax:XB}Mtr', name='k1_x')
k1_y = EpicsMotor('XF:11IDB-OP{Lens:1-Ax:YB}Mtr', name='k1_y')
k1_Chi = EpicsMotor('XF:11IDB-OP{Lens:1-Ax:Ch}Mtr', name='k1_Chi')
k1_Theta = EpicsMotor('XF:11IDB-OP{Lens:1-Ax:Th}Mtr', name='k1_Theta')
k1_Phi = EpicsMotor('XF:11IDB-OP{Lens:1-Ax:Ph}Mtr', name='k1_Phi')
k1_lx = EpicsMotor('XF:11IDB-OP{Lens:1-Ax:XT}Mtr', name='k1_lx')
k1_ly = EpicsMotor('XF:11IDB-OP{Lens:1-Ax:YT}Mtr', name='k1_ly')

# GI-mirror
gi_x  = EpicsMotor('XF:11IDB-OP{Mir:GI-Ax:X}Mtr', name='gi_x')
gi_y  = EpicsMotor('XF:11IDB-OP{Mir:GI-Ax:Y}Mtr', name='gi_y')
gi_th = EpicsMotor('XF:11IDB-OP{Mir:GI-Ax:Th}Mtr', name='gi_th')

# Kinoform Unit 2 (downstream)
k2_z = EpicsMotor('XF:11IDB-OP{Lens:2-Ax:ZB}Mtr', name='k2_z')
k2_x = EpicsMotor('XF:11IDB-OP{Lens:2-Ax:XB}Mtr', name='k2_x')
k2_y = EpicsMotor('XF:11IDB-OP{Lens:2-Ax:YB}Mtr', name='k2_y')
k2_Chi = EpicsMotor('XF:11IDB-OP{Lens:2-Ax:Ch}Mtr', name='k2_Chi')
k2_Theta = EpicsMotor('XF:11IDB-OP{Lens:2-Ax:Th}Mtr', name='k2_Theta')
k2_Phi = EpicsMotor('XF:11IDB-OP{Lens:2-Ax:Ph}Mtr', name='k2_Phi')
k2_lx = EpicsMotor('XF:11IDB-OP{Lens:2-Ax:XT}Mtr', name='k2_lx')
k2_ly = EpicsMotor('XF:11IDB-OP{Lens:2-Ax:YT}Mtr', name='k2_ly')

#Beam-defining (large JJ) slits
s2_xg = EpicsMotor('XF:11IDB-OP{Slt:2-Ax:XGap}Mtr', name='s2_xg')
s2_xc = EpicsMotor('XF:11IDB-OP{Slt:2-Ax:XCtr}Mtr', name='s2_xc')
s2_yg = EpicsMotor('XF:11IDB-OP{Slt:2-Ax:YGap}Mtr', name='s2_yg')
s2_yc = EpicsMotor('XF:11IDB-OP{Slt:2-Ax:YCtr}Mtr', name='s2_yc')

#Guard Slits (SmarAct)

gs_xg = PVPositioner('XF:11IDB-OP{Slt:Guard-Ax:X}size',
		      readback='XF:11IDB-OP{Slt:Guard-Ax:X}t2.C',
		      done='XF:11IDB-OP{Slt:Guard-Ax:X}DMOV',
	              done_val=1,
		      name='gs_xg')

gs_xc = PVPositioner('XF:11IDB-OP{Slt:Guard-Ax:X}center',
		      readback='XF:11IDB-OP{Slt:Guard-Ax:X}t2.D',
		      done='XF:11IDB-OP{Slt:Guard-Ax:X}DMOV',
	              done_val=1,
		      name='gs_xc')

gs_yg = PVPositioner('XF:11IDB-OP{Slt:Guard-Ax:Y}size',
		      readback='XF:11IDB-OP{Slt:Guard-Ax:Y}t2.C',
		      done='XF:11IDB-OP{Slt:Guard-Ax:Y}DMOV',
	              done_val=1,
		      name='gs_yg')

gs_yc = PVPositioner('XF:11IDB-OP{Slt:Guard-Ax:Y}center',
		      readback='XF:11IDB-OP{Slt:Guard-Ax:Y}t2.D',
		      done='XF:11IDB-OP{Slt:Guard-Ax:Y}DMOV',
	              done_val=1,
		      name='gs_yc')

gs_b = EpicsMotor('XF:11IDB-OP{Slt:Guard-Ax:B}Mtr', name='gs_b')
gs_t = EpicsMotor('XF:11IDB-OP{Slt:Guard-Ax:T}Mtr', name='gs_t')
gs_i = EpicsMotor('XF:11IDB-OP{Slt:Guard-Ax:I}Mtr', name='gs_i')
gs_o = EpicsMotor('XF:11IDB-OP{Slt:Guard-Ax:O}Mtr', name='gs_o')


#Temporary Guard slits
s4_xg = EpicsMotor('XF:11IDB-ES{Slt:4-Ax:XGap}Mtr', name='s4_xg')
s4_xc = EpicsMotor('XF:11IDB-ES{Slt:4-Ax:XCtr}Mtr', name='s4_xc')
s4_yg = EpicsMotor('XF:11IDB-ES{Slt:4-Ax:YGap}Mtr', name='s4_yg')
s4_yc = EpicsMotor('XF:11IDB-ES{Slt:4-Ax:YCtr}Mtr', name='s4_yc')

#Diffractometer
diff_del = EpicsMotor('XF:11IDB-ES{Dif-Ax:Del}Mtr', name='diff_del')
diff_gam = EpicsMotor('XF:11IDB-ES{Dif-Ax:Gam}Mtr', name='diff_gam')
diff_om = EpicsMotor('XF:11IDB-ES{Dif-Ax:Om}Mtr', name='diff_om')
diff_phi = EpicsMotor('XF:11IDB-ES{Dif-Ax:Ph}Mtr', name='diff_phi')
diff_xb = EpicsMotor('XF:11IDB-ES{Dif-Ax:XB}Mtr', name='diff_xb')
diff_yb = EpicsMotor('XF:11IDB-ES{Dif-Ax:YB}Mtr', name='diff_yb')
diff_chh = EpicsMotor('XF:11IDB-ES{Dif-Ax:ChH}Mtr', name='diff_chh')
diff_thh = EpicsMotor('XF:11IDB-ES{Dif-Ax:ThH}Mtr', name='diff_thh')
diff_phh = EpicsMotor('XF:11IDB-ES{Dif-Ax:PhH}Mtr', name='diff_phh')
diff_xh = EpicsMotor('XF:11IDB-ES{Dif-Ax:XH}Mtr', name='diff_xh')
diff_yh = EpicsMotor('XF:11IDB-ES{Dif-Ax:YH2}Mtr', name='diff_yh')
diff_zh = EpicsMotor('XF:11IDB-ES{Dif-Ax:ZH}Mtr', name='diff_zh')
diff_chv = EpicsMotor('XF:11IDB-ES{Dif-Ax:ChV}Mtr', name='diff_chv')
diff_thv = EpicsMotor('XF:11IDB-ES{Dif-Ax:ThV}Mtr', name='diff_thv')
diff_xv = EpicsMotor('XF:11IDB-ES{Dif-Ax:XV}Mtr', name='diff_xv')
diff_yv = EpicsMotor('XF:11IDB-ES{Dif-Ax:YV}Mtr', name='diff_yv')
diff_zv = EpicsMotor('XF:11IDB-ES{Dif-Ax:ZV}Mtr', name='diff_zv')
diff_xv2 = EpicsMotor('XF:11IDB-ES{Dif-Ax:XV2}Mtr', name='diff_xv2')

# sample beamstop
sambst_x = EpicsMotor('XF:11IDB-OP{BS:Samp-Ax:X}Mtr', name='sambst_x')
sambst_y = EpicsMotor('XF:11IDB-OP{BS:Samp-Ax:Y}Mtr', name='sambst_y')

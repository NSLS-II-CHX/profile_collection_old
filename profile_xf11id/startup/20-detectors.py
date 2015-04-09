from ophyd.controls import ProsilicaDetector, EpicsSignal

# AreaDetector Beam Instrumentation
fs1_cam = ProsilicaDetector('XF:11IDA-BI{FS:1-Cam:1}')
wbs_cam = ProsilicaDetector('XF:11IDA-BI{BS:WB-Cam:1}')
fs2_cam = ProsilicaDetector('XF:11IDA-BI{FS:2-Cam:1}')
dcm_cam = ProsilicaDetector('XF:11IDA-BI{Mono:DCM-Cam:1}')
pbs_cam = ProsilicaDetector('XF:11IDA-BI{BS:PB-Cam:1}')
bpm_cam = ProsilicaDetector('XF:11IDA-BI{Bpm:1-Cam:1}')

# BPM camera

bpm_cam_acq = EpicsSignal('XF:11IDA-BI{Bpm:1-Cam:1}cam1:Acquire_RBV',
                        write_pv='XF:11IDA-BI{Bpm:1-Cam:1}cam1:Acquire',
                        rw=True, name='bpm_cam_acq')
bpm_tot1 = EpicsSignal('XF:11IDA-BI{Bpm:1-Cam:1}Stats1:Total_RBV',
                         rw=False, name='bpm_tot1')
bpm_tot2 = EpicsSignal('XF:11IDA-BI{Bpm:1-Cam:1}Stats2:Total_RBV',
                         rw=False, name='bpm_tot2')
bpm_tot3 = EpicsSignal('XF:11IDA-BI{Bpm:1-Cam:1}Stats3:Total_RBV',
                         rw=False, name='bpm_tot3')
bpm_tot4 = EpicsSignal('XF:11IDA-BI{Bpm:1-Cam:1}Stats4:Total_RBV',
                         rw=False, name='bpm_tot4')
bpm_tot5 = EpicsSignal('XF:11IDA-BI{Bpm:1-Cam:1}Stats5:Total_RBV',
                         rw=False, name='bpm_tot5')

# FS1 camera

fs1_cam_acq = EpicsSignal('XF:11IDA-BI{FS:1-Cam:1}cam1:Acquire_RBV',
                        write_pv='XF:11IDA-BI{FS:1-Cam:1}cam1:Acquire',
                        rw=True, name='fs1_cam_acq')
fs1_tot1 = EpicsSignal('XF:11IDA-BI{FS:1-Cam:1}Stats1:Total_RBV',
                         rw=False, name='fs1_tot1')
fs1_tot2 = EpicsSignal('XF:11IDA-BI{FS:1-Cam:1}Stats2:Total_RBV',
                         rw=False, name='fs1_tot2')
fs1_tot3 = EpicsSignal('XF:11IDA-BI{FS:1-Cam:1}Stats3:Total_RBV',
                         rw=False, name='fs1_tot3')
fs1_tot4 = EpicsSignal('XF:11IDA-BI{FS:1-Cam:1}Stats4:Total_RBV',
                         rw=False, name='fs1_tot4')
fs1_tot5 = EpicsSignal('XF:11IDA-BI{FS:1-Cam:1}Stats5:Total_RBV',
                         rw=False, name='fs1_tot5')
# WBS camera

wbs_cam_acq = EpicsSignal('XF:11IDA-BI{BS:WB-Cam:1}cam1:Acquire_RBV',
                        write_pv='XF:11IDA-BI{BS:WB-Cam:1}cam1:Acquire',
                        rw=True, name='wbs_cam_acq')
wbs_tot1 = EpicsSignal('XF:11IDA-BI{BS:WB-Cam:1}Stats1:Total_RBV',
                         rw=False, name='wbs_tot1')
wbs_tot2 = EpicsSignal('XF:11IDA-BI{BS:WB-Cam:1}Stats2:Total_RBV',
                         rw=False, name='wbs_tot2')
wbs_tot3 = EpicsSignal('XF:11IDA-BI{BS:WB-Cam:1}Stats3:Total_RBV',
                         rw=False, name='wbs_tot3')
wbs_tot4 = EpicsSignal('XF:11IDA-BI{BS:WB-Cam:1}Stats4:Total_RBV',
                         rw=False, name='wbs_tot4')
wbs_tot5 = EpicsSignal('XF:11IDA-BI{BS:WB-Cam:1}Stats5:Total_RBV',
                         rw=False, name='wbs_tot5')                        
                     
# FS2 camera

fs2_cam_acq = EpicsSignal('XF:11IDA-BI{FS:2-Cam:1}cam1:Acquire_RBV',
                        write_pv='XF:11IDA-BI{FS:2-Cam:1}cam1:Acquire',
                        rw=True, name='fs2_cam_acq')
fs2_tot1 = EpicsSignal('XF:11IDA-BI{FS:2-Cam:1}Stats1:Total_RBV',
                         rw=False, name='fs2_tot1')
fs2_tot2 = EpicsSignal('XF:11IDA-BI{FS:2-Cam:1}Stats2:Total_RBV',
                         rw=False, name='fs2_tot2')
fs2_tot3 = EpicsSignal('XF:11IDA-BI{FS:2-Cam:1}Stats3:Total_RBV',
                         rw=False, name='fs2_tot3')
fs2_tot4 = EpicsSignal('XF:11IDA-BI{FS:2-Cam:1}Stats4:Total_RBV',
                         rw=False, name='fs2_tot4')
fs2_tot5 = EpicsSignal('XF:11IDA-BI{FS:2-Cam:1}Stats5:Total_RBV',
                         rw=False, name='fs2_tot5')
                         
# try to add Electrometer AH401D

elm_cam_acq = EpicsSignal('XF:11IDA-BI{AH401B}AH401B:Acquire_RBV',
			  write_pv='XF:11IDA-BI{AH401B}AH401B:Acquire',
			  rw=True, name='elm_cam_acq')
elm_d1  =  EpicsSignal('XF:11IDA-BI{AH401B}AH401B:Current1:MeanValue_RBV',
			  rw=False, name='elm_d1')
elm_d2  =  EpicsSignal('XF:11IDA-BI{AH401B}AH401B:Current2:MeanValue_RBV',
			  rw=False, name='elm_d2')
elm_d3  =  EpicsSignal('XF:11IDA-BI{AH401B}AH401B:Current3:MeanValue_RBV',
			  rw=False, name='elm_d3')
elm_d4  =  EpicsSignal('XF:11IDA-BI{AH401B}AH401B:Current4:MeanValue_RBV',
			  rw=False, name='elm_d4')
elm_s12  =  EpicsSignal('XF:11IDA-BI{AH401B}AH401B:Sum12:MeanValue_RBV',
			  rw=False, name='elm_s12')
elm_s34  =  EpicsSignal('XF:11IDA-BI{AH401B}AH401B:Sum34:MeanValue_RBV',
			  rw=False, name='elm_s34')
elm_s1234  =  EpicsSignal('XF:11IDA-BI{AH401B}AH401B:Sum1234:MeanValue_RBV',
			  rw=False, name='elm_s1234') 

# X-ray eye camera

xray_cam_acq = EpicsSignal('XF:11IDB-BI{Cam:08}cam1:Acquire_RBV',
                        write_pv='XF:11IDB-BI{Cam:08}cam1:Acquire',
                        rw=True, name='xray_cam_acq')
xray_tot1 = EpicsSignal('XF:11IDB-BI{Cam:08}Stats1:Total_RBV',
                         rw=False, name='xray_tot1')
xray_tot2 = EpicsSignal('XF:11IDB-BI{Cam:08}Stats2:Total_RBV',
                         rw=False, name='xray_tot2')
xray_tot3 = EpicsSignal('XF:11IDB-BI{Cam:08}Stats3:Total_RBV',
                         rw=False, name='xray_tot3')


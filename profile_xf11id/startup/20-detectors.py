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

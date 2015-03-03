from ophyd.userapi.scan_api import Scan, AScan, DScan, Count

scan = Scan()
ascan = AScan()
ascan.default_triggers = [bpm_cam_acq]
ascan.default_detectors = [bpm_tot5]
dscan = DScan()

# Use ct as a count which is a single scan.

ct = Count()

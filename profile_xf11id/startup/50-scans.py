from ophyd.userapi.scan_api import Scan, AScan, DScan, Count, estimate
scan = Scan()
ascan = AScan()

# Use ct as a count which is a single scan.

ct = Count()

from chxtools import ophyd_tools

ascan  = ophyd_tools.CHXAScan()
ascan.default_detectors = []
ascan.user_detectors = [bpm_cam]

dscan = ophyd_tools.CHXDScan()

# Import everything from these locations (for now!)
# from chxtools.chx_wrapper import *
from chxtools.xfuncs import *
from chxtools.plot import plot1d

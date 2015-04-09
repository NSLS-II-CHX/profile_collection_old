from ophyd.userapi.scan_api import Scan, AScan, DScan, Count, estimate
scan = Scan()
ascan = AScan()
ascan.default_triggers = [bpm_cam_acq]
ascan.default_detectors = [bpm_tot5]
dscan = DScan()

# Use ct as a count which is a single scan.

ct = Count()

class CHXAScan(AScan):
    def __call__(self, *args, **kwargs):
        super(CHXAScan, self).__call__(*args, **kwargs)

    def post_scan(self):
        print('pos[0], det[0]: {}, {}'.format(
            self.positioners[0].name, self.detectors[0].name))
        est = estimate(self.positioners[0].name, self.detectors[0].name)
        print('estimates: {}'.format(est))

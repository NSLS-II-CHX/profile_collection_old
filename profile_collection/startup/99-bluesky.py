
def detselect(detector_object, suffix="_stats_total1"):
    """Switch the active detector and set some internal state"""
    gs.DETS =[detector_object]
    gs.PLOT_Y = detector_object.name + suffix
    gs.TABLE_COLS = [gs.PLOT_Y] 

def chx_plot_motor(scan):
    fig = None
    if gs.PLOTMODE == 1:
        fig = plt.gcf()
    elif gs.PLOTMODE == 2:
        fig = plt.gcf()
        fig.clear()
    elif gs.PLOTMODE == 3:
        fig = plt.figure()
    return LivePlot(gs.PLOT_Y, scan.motor._name, fig=fig)

# this changes the default plotter for *all* classes that 
# inherit from bluesky.simple_scans._StepScan
dscan.default_sub_factories['all'][1] = chx_plot_motor

gs.PLOTMODE = 1

from bluesky.global_state import (resume, abort, stop, panic, 
                                  all_is_well, state)


# hacking on the logbook!

from pprint import pformat, pprint
from bluesky.callbacks import CallbackBase
from bluesky.callbacks.olog import OlogCallback

olog_cb = OlogCallback('Data Acquisition')
gs.RE.subscribe('start', olog_cb)


import os
from datetime import datetime

def write_spec_header(path, doc):
    # write a new spec file header!
    #F /home/xf11id/specfiles/test.spec
    #E 1449179338.3418093
    #D 2015-12-03 16:48:58.341809
    #C xf11id  User = xf11id
    #O [list of all motors, 10 per line]
    session_manager = get_session_manager()
    pos = session_manager.get_positioners()
    spec_header = [
        '#F %s' % path,
        '#E %s' % int(doc['time']),
        # time might need to be formatted specifically
        '#D %s' % datetime.fromtimestamp(doc['time']),
        '#C %s  User = %s' % (doc['owner'], doc['owner']),
        'O0 {}'.format(' '.join(sorted(list(pos.keys()))))
    ]
    with open(path, 'w') as f:
        f.write('\n'.join(spec_header))
    return spec_header
                

class LiveSpecFile(CallbackBase):
    def start(self, doc):
        if not os.path.exists(gs.specpath):
            spec_header = write_spec_header(gs.specpath, doc)
        #else:
        #    spec_header = get_spec_header()
        last_command = list(
            get_ipython().history_manager.get_range())[-1][2]
        last_command = last_command.replace('(', ' ')
        last_command = last_command.replace(')', ' ')
        last_command = last_command.replace(',', ' ')
        dets = eval(doc['detectors'])
        try:
            self.acquisition_time = dets[0].cam.acquire_time
        except AttributeError:
            self.acquisition_time = -1
        # write a blank line between scans
        with open(gs.specpath, 'a') as f:
            f.write('\n\n')
        # write the new scan entry
        with open(gs.specpath, 'a') as f:
            f.write('#S %s %s\n' % (doc['scan_id'], last_command))
            f.write('#D %s\n' % datetime.fromtimestamp(doc['time']))
            f.write('#T %s (Seconds)\n' % self.acquisition_time)
        # write the motor positions
        session_manager = get_session_manager()
        pos = session_manager.get_positioners()
        positions = [str(v.position) for k, v in sorted(pos.items())]
        with open(gs.specpath, 'a') as f:
            f.write('#P0 {0}\n'.format(' '.join(positions)))
        # writing the list of motor names and their current values in
        # a more human readable way. Apparently "#M" is not a used key in
        # spec. Fingers crossed....
        with open(gs.specpath, 'a') as f:
            for idx, (name, positioner) in enumerate(sorted(pos.items())):
                f.write('#M%s %s %s\n' % (idx, name, str(positioner.position)))
        print("RunStart document received in LiveSpecFile")
        #raise
        self.motorname = eval(doc['motor']).name
    
    def descriptor(self, doc):
        keys = sorted(list(doc['data_keys'].keys()))
        keys.remove(self.motorname)
        keys.insert(0, 'Seconds')
        keys.insert(0, 'Epoch')
        keys.insert(0, self.motorname)
        with open(gs.specpath, 'a') as f:
            f.write('#N %s\n' % len(keys))
            f.write('#L {0}    {1}\n'.format(keys[0], 
                                             '  '.join(keys[1:])))
    
    def event(self, doc):
        t = int(doc['time'])
        vals = [v for k, v in sorted(doc['data'].items()) if k != self.motorname]
        vals.insert(0, self.acquisition_time)
        vals.insert(0, t)
        vals.insert(0, doc['data'][self.motorname])
        vals = [str(v) for v in vals]
        with open(gs.specpath, 'a') as f:
            f.write('{0}  {1}\n'.format(vals[0], ' '.join(vals[1:])))

gs.specpath = os.path.expanduser('~/specfiles/test.spec')
live_specfile_callback = LiveSpecFile()
gs.RE.subscribe('all', live_specfile_callback)

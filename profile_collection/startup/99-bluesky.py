
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

from pyOlog import SimpleOlogClient
client = SimpleOlogClient()
from pprint import pformat, pprint
from bluesky.callbacks import CallbackBase
from IPython import get_ipython
class OlogCallback(CallbackBase):
    def start(self, doc):
        commands = list(get_ipython().history_manager.get_range())
        document_content = ('%s: %s\n\n'
                            'RunStart Document\n'
                            '-----------------\n'
                            '%s' % (doc['scan_id'],
                                    commands[-1][2],
                                    pformat(doc)))
        olog_status = client.log(document_content, logbooks='Data Acquisition')
        print('client.log returned %s' % olog_status)
#dscan.default_sub_factories['all'].append(OlogCallback())
gs.RE.subscribe('start', OlogCallback())
gs.RE.logbook = None


import os
from datetime import datetime

specfilepath = os.path.expanduser('~/specfiles/test.spec')
from pprint import pprint

def nest_list(lst, ncols):
    numcols = 0
    maxcols = 10
    motors = [[]]
    for item in lst:
        if numcols == maxcols:
            numcols=0
            motors.append([])
        motors[-1].append(str(item))
        numcols += 1
   
    return motors
    
def write_spec_header(path, doc):
    # write a new spec file header!
    #F /home/xf11id/specfiles/test.spec
    #E 1449179338.3418093
    #D 2015-12-03 16:48:58.341809
    #C xf11id  User = xf11id
    #O [list of all motors, 10 per line]
    spec_header = [
        '#F %s' % path,
        '#E %s' % int(doc['time']),
        # time might need to be formatted specifically
        '#D %s' % datetime.fromtimestamp(doc['time']),
        '#C %s  User = %s' % (doc['owner'], doc['owner']),
    ]
    session_manager = get_session_manager()
    pos = session_manager.get_positioners()
    motors = nest_list(sorted(list(pos.keys())), 10)
    for line_num, line in enumerate(motors):
        spec_header.append(
            '#O{0} {1}'.format(line_num, ' '.join(line)))
    with open(path, 'w') as f:
        for line in spec_header:
            f.write(line + '\n')
    return spec_header
                
def get_spec_header():
    # this needs to be implemented...
    raise NotImplementedError()
    
class LiveSpecFile(CallbackBase):
    def __init__(self, specfilepath):
        self.specfilepath = specfilepath
        
    def start(self, doc):
        if not os.path.exists(self.specfilepath):
            spec_header = write_spec_header(self.specfilepath, doc)
        #else:
        #    spec_header = get_spec_header()
        last_command = list(
            get_ipython().history_manager.get_range())[-1][2]
        last_command = last_command.replace('(', ' ')
        last_command = last_command.replace(')', ' ')
        last_command = last_command.replace(',', ' ')
        self.acqisition_time = 1
        # write a blank line between scans
        with open(self.specfilepath, 'a') as f:
            f.write('\n')
        # write the new scan entry
        with open(self.specfilepath, 'a') as f:
            f.write('#S %s %s\n' % (doc['scan_id'], last_command))
            f.write('#D %s\n' % datetime.fromtimestamp(doc['time']))
            f.write('#T %s (Seconds)\n' % self.acqisition_time)
        # write the motor positions
        session_manager = get_session_manager()
        pos = session_manager.get_positioners()        
        positions = [v.position for k, v in sorted(pos.items())]
        nested = nest_list(positions, 10)
        print('nested')
        pprint(nested)
        with open(self.specfilepath, 'a') as f:
            for line_num, line in enumerate(nested):
                f.write('#P{0} {1}\n'.format(line_num, ' '.join(line)))
        print("RunStart document received in LiveSpecFile!")
        #raise
        self.motorname = eval(db[-1]['start']['motor']).name
    
    def descriptor(self, doc):
        keys = sorted(list(doc['data_keys'].keys()))
        keys.remove(self.motorname)
        keys.insert(0, 'Seconds')
        keys.insert(0, 'Epoch')
        keys.insert(0, self.motorname)
        with open(self.specfilepath, 'a') as f:
            f.write('#N %s\n' % len(keys))
            f.write('#L {0}    {1}\n'.format(keys[0], 
                                             '  '.join(keys[1:])))
    
    def event(self, doc):
        t = int(doc['time'])
        vals = [v for k, v in sorted(doc['data'].items()) if k != self.motorname]
        vals.insert(0, self.acqisition_time)
        vals.insert(0, t)
        vals.insert(0, doc['data'][self.motorname])
        vals = [str(v) for v in vals]
        with open(self.specfilepath, 'a') as f:
            f.write('{0}  {1}\n'.format(vals[0], ' '.join(vals[1:])))
        

gs.RE.subscribe('all', LiveSpecFile(specfilepath=specfilepath))
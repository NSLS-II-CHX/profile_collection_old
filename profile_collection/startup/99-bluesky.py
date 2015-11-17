
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
        commands = list(get_ipython().session.history_manager.get_range())
        document_content = ('%s: %s\n\n'
                            'RunStart Document\n'
                            '-----------------\n'
                            '%s' % (doc['scan_id'],
                                    commands[-1][2],
                                    pformat(doc)))
        client.log(document_content, logbooks='Data Acquisition')

#dscan.default_sub_factories['all'].append(OlogCallback())
gs.RE.subscribe('start', OlogCallback())
gs.RE.logbook = None


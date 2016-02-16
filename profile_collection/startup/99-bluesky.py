
def detselect(detector_object, suffix="_stats1_total"):
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
#dscan.default_sub_factories['all'][1] = chx_plot_motor

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

def get_epics_motors():
    return {name: obj for name, obj in globals().items() if isinstance(obj, (EpicsMotor))}


gs.specpath = os.path.expanduser('~/specfiles/test4.spec')
#live_specfile_callback = LiveSpecFile()
#gs.RE.subscribe('all', live_specfile_callback)




from bluesky.callbacks.core import LiveSpecFile
from bluesky.spec_api import ascan, dscan, ct  # this may already be in your profile
spec_cb = LiveSpecFile('/home/xf11id/specfiles/test4.spec')
for spec_scan in [ascan, dscan, ct]:
    #    Route all documents to the spec callback.
    spec_scan.subs['all'].append(spec_cb)


def relabel_figure(fig, new_title):
    fig.set_label(new_title)
    fig.canvas.manager.window.setWindowTitle(new_title)
    




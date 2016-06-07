
def detselect(detector_object, suffix="_stats1_total"):
    """Switch the active detector and set some internal state"""
    gs.DETS =[detector_object]
    gs.PLOT_Y = detector_object.name + suffix
    gs.TABLE_COLS = [gs.PLOT_Y] 

def E_scan(energy, gap=[], xtal="Si111cryo", gapmode="auto", harm=5, det=elm.sum_all):
	"""
	energy scan: Scanning both Bragg axis and gap of IVU in a linked fashion
	calling sequence: E_scan(energy, gap=[], xtal="Si111cryo", gapmode="auto", harm=5 det=elm.sum_all.value)
	energy: X-ray energy in [keV] & xtal define the Bragg angles used in the scan via xf.get_Bragg()
	gap: manually entered list of gap values with gapmode="manual" OR calculated from xf.get_gap(energy, harm, default id map) with gapmode="auto"
	to-do: allow detector selection from 'detselect()'
	by LW June 2016	
	"""
	from cycler import cycler
	from bluesky import PlanND
	th_B=list(-1*xf.get_Bragg(xtal,energy)[:,0])
	if gapmode == "manual":
		if len(gap) == len(energy):
			gap = gap
			print('using manually entered gap values...')
		else: print('error: length of manually entered list of gap value does not match number of energy points')
	elif gapmode =="auto":
		gap=list(xf.get_gap(energy,harm))
		print('using calculated gap values from xfuncs!')
	inner = cycler(dcm.b,th_B)+cycler(ivu_gap,gap)
	#plan = PlanND([det],inner)
	plan = PlanND([det],inner)
	RE(plan, [LiveTable([dcm.b,ivu_gap,det]),LivePlot(x='dcm_b',y=det.name,fig = plt.figure())])
			

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


# hacking on the logbook!

from pprint import pformat, pprint
from bluesky.callbacks import CallbackBase

import os
from datetime import datetime

def get_epics_motors():
    return {name: obj for name, obj in globals().items() if isinstance(obj, (EpicsMotor))}


gs.specpath = os.path.expanduser('/home/xf11id/specfiles/spec0.spec')
#live_specfile_callback = LiveSpecFile()
#gs.RE.subscribe('all', live_specfile_callback)

#def print_scan_id(name,doc):
#    print(db[-1]['scan_id'])
#RE.subscribe('stop', print_scan_id)


class print_scan_id(CallbackBase):
    def start(self, doc):
        self._scan_id = doc['scan_id']

    def stop(self, doc):
        print("The scan ID is: %s" %self._scan_id)
RE.subscribe('all', print_scan_id())


#RE.subscribe('stop', Whatever())

#RE.subscribe('all', Whatever())

#wh = Whatever()
#RE.subscribe('start', wh)
#RE.subscribe('stop', wh)


#from bluesky.callbacks.core import LiveSpecFile
#

# for spec_scan in [ascan, dscan, ct]:
    #    Route all documents to the spec callback.
#    spec_scan.subs['all'].append(spec_cb)


def relabel_figure(fig, new_title):
    fig.set_label(new_title)
    fig.canvas.manager.window.setWindowTitle(new_title)
    


from suitcase.spec import DocumentToSpec
spec_cb = DocumentToSpec('/home/xf11id/specfiles/testing.spec')

import bluesky.spec_api
from bluesky.plans import planify, subs_context
from functools import wraps

@wraps(bluesky.spec_api.dscan)
@planify
def dscan(*args, **kwargs):
    plans = []
    with subs_context(plans, [spec_cb]):
        plans.append(bluesky.spec_api.dscan(*args, **kwargs))
    return plans


@wraps(bluesky.spec_api.ascan)
@planify
def ascan(*args, **kwargs):
    plans = []
    with subs_context(plans, [spec_cb]):
        plans.append(bluesky.spec_api.ascan(*args, **kwargs))
    return plans


@wraps(bluesky.spec_api.ct)
@planify
def ct(*args, **kwargs):
    plans = []
    with subs_context(plans, [spec_cb]):
        plans.append(bluesky.spec_api.ct(*args, **kwargs))
    return plans
    

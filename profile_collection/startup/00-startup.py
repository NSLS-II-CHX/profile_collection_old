# import ophyd
# ophyd.commands.setup_ophyd()

import logging
from bluesky.standard_config import *  # gs, etc.
import matplotlib.pyplot as plt
plt.ion()
from bluesky import qt_kicker
qt_kicker.install_qt_kicker()
from databroker import DataBroker as db, get_events, get_images, get_table, get_fields, restream, process

from epics import caput, caget

# connect olog
# gs.RE.logbook = olog_wrapper(olog_client, ['Data Acquisition'])

# ophyd expects to find 'logbook' in the IPython namespace
from pyOlog import SimpleOlogClient
logbook = SimpleOlogClient()

RE=gs.RE
from bluesky.scientific_callbacks import plot_peak_stats
# from chxtools.xfuncs import *
# from chxtools.plot import plot1

from bluesky.plans import  *

import ophyd




from chxtools import attfuncs as att
from chxtools import xfuncs as xf
from chxtools.bpm_stability import bpm_read
#from chxtools import bpm_stability as bpmst

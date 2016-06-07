import logging
# Make ophyd listen to pyepics.
from ophyd import setup_ophyd
setup_ophyd()

import matplotlib.pyplot as plt
plt.ion()
# Make plots update live while scans run.
from bluesky.utils import install_qt_kicker
install_qt_kicker()

# convenience imports
from ophyd.commands import *
from bluesky.callbacks import *
# from bluesky.scientific_callbacks import plot_peak_stats
# from bluesky.plans import *
from bluesky.plan_tools import print_summary
from bluesky.spec_api import *
from bluesky.global_state import gs, abort, stop, resume
from databroker import (DataBroker as db, get_events, get_images,
                        get_table, get_fields, restream, process)
from time import sleep
import numpy as np

RE = gs.RE  # convenience alias


# Subscribe metadatastore to documents.
# If this is removed, data is not saved to metadatastore.
import metadatastore.commands
gs.RE.subscribe_lossless('all', metadatastore.commands.insert)

from epics import caput, caget

# c.InteractiveShellApp.extensions = ['pyOlog.cli.ipy']

gs.MD_TIME_KEY = 'count_time'  # this will the default in bluesky v0.5.3+


from chxtools import attfuncs as att
from chxtools import xfuncs as xf
from chxtools.bpm_stability import bpm_read
from chxtools import transfuncs as trans


#from chxtools import bpm_stability as bpmst

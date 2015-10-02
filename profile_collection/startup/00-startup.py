import logging
from bluesky.standard_config import *  # gs, etc.
import matplotlib.pyplot as plt
plt.ion()
from databroker import DataBroker as db, get_events, get_images, get_table

# connect olog
gs.RE.logbook = olog_wrapper(olog_client, ['Data Acquisition'])
RE=gs.RE
from bluesky.scientific_callbacks import plot_peak_stats
# from chxtools.xfuncs import *
# from chxtools.plot import plot1d

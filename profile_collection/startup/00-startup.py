import logging
import time
from contextlib import contextmanager

@contextmanager
def progress(text):
    start = time.time()
    print(text)
    yield
    print('Done in %f.1 seconds' % (time.time() - start))

with progress('setting up ophyd'):
    # Make ophyd listen to pyepics.
    from ophyd import setup_ophyd
    setup_ophyd()

with progress('importing matplotlib'):
    import matplotlib.pyplot as plt
    plt.ion()

with progress('qt kicking'):
    # Make plots update live while scans run.
    from bluesky.utils import install_qt_kicker
    install_qt_kicker()

with progress('ophyd, bluesky imports'):
    # convenience imports
    from ophyd.commands import *
    from bluesky.callbacks import *
    # from bluesky.scientific_callbacks import plot_peak_stats
    # from bluesky.plans import *
    from bluesky.plan_tools import print_summary
    from bluesky.spec_api import *
    from bluesky.global_state import gs, abort, stop, resume

with progress('databroker import'):
    from databroker import (DataBroker as db, get_events, get_images,
                            get_table, get_fields, restream, process)
from time import sleep
import numpy as np

RE = gs.RE  # convenience alias


from metadatastore.mds import MDS
# from metadataclient.mds import MDS
from databroker import Broker
from databroker.core import register_builtin_handlers
from filestore.fs import FileStore

mds = MDS({'host': 'xf11id-srv1',
           'database': 'datastore',
           'port': 27017,
           'timezone': 'US/Eastern'}, auth=False)
# mds = MDS({'host': CA, 'port': 7770})

db = Broker(mds, FileStore({'host': 'xf11id-srv1',
           'database': 'filestore',
           'port': 27017}))
register_builtin_handlers(db.fs)

gs.RE.subscribe('all', db.mds.insert)

from epics import caput, caget

# c.InteractiveShellApp.extensions = ['pyOlog.cli.ipy']

gs.MD_TIME_KEY = 'count_time'  # this will the default in bluesky v0.5.3+


from chxtools import attfuncs as att
from chxtools import xfuncs as xf
from chxtools.bpm_stability import bpm_read
from chxtools import transfuncs as trans  


from chxtools import bpm_stability as bpmst

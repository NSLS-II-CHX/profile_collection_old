from chxtools.chx_wrapper import *
from ophyd.userapi.scan_api import estimate
import xfuncs as xf
from prettytable import PrettyTable
from chxtools.ophyd_tools import print_estimate_table_det_rows
from dataportal import DataBroker, DataMuxer, Images
import numpy as np

def est(x_axis, scan_id):
    """

    Parameters
    ----------
    x_axis : str
        The name of the x axis to use for stats computation
    scan_id : int
        Some argument that gets passed to db[]. Any valid argument for
        db[] is a valid argument for scan_id
    """

    hdr = DataBroker[scan_id]
    ev = list(DataBroker.fetch_events(hdr, fill=False))
    dm = DataMuxer.from_events(ev)
    df = dm.to_sparse_dataframe()
    keys = list(df)
    if not hasattr(x_axis, 'append'):
        x_axis = [x_axis]
    # check that all x values are in the dataframe
    for x in x_axis:
        if x not in keys:
            raise ValueError("%s is not an available key. Available"
                             " keys are %s" % (x, keys))
    estimates = {}
    for x_name in x_axis:
        x = np.asarray(df[x_name])
        estimates[x_name] = {}
        for k in list(df):
            y = np.asarray(df[k])
            estimates[x_name][k] = estimate(x, y)
    print_estimate_table_det_rows(estimates)
    



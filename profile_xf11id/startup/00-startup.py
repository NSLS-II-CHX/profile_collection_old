import logging
session_mgr._logger.setLevel(logging.INFO)
from ophyd.userapi import *
import matplotlib.pyplot as plt
plt.ion()
from dataportal import (DataBroker as db, 
                        StepScan as ss,
                        StepScan, DataBroker, 
                        DataMuxer)

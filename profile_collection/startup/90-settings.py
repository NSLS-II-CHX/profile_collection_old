gs.DETS = [xray_eye3]


import logging

# metadata set at startup
gs.RE.md['owner'] = 'xf11id'
gs.RE.md['group'] = 'chx'
gs.RE.md['beamline_id'] = 'CHX'
# removing 'custom' as it is raising an exception in 0.3.2
# gs.RE.md['custom'] = {}



def print_scanid(name, doc):
    if name == 'start':
        print('Scan ID:', doc['scan_id'])
        print('Unique ID:', doc['uid'])

def print_md(name, doc):
    if name == 'start':
        print('Metadata:\n', repr(doc))

gs.RE.subscribe('start', print_scanid)

from ophyd.commands import wh_pos, log_pos, mov, movr

from eiger_io.fs_handler import EigerHandler
from filestore.api import register_handler
register_handler("AD_EIGER", EigerHandler)

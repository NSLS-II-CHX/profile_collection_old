gs.DETS = [bpm_cam]


import logging

from ophyd.session import get_session_manager

sessionmgr = get_session_manager()
sessionmgr['olog_client'] = olog_client
print('These positioners are disconnected:')
print([k for k, v in sessionmgr.get_positioners().items() if not v.connected])

# metadata set at startup
gs.RE.md['owner'] = 'xf11id'
gs.RE.md['group'] = 'chx'
gs.RE.md['beamline_id'] = 'CHX'
gs.RE.md['custom'] = {}



def print_scanid(name, doc):
    if name == 'start':
        print('Scan ID:', doc['scan_id'])
        print('Unique ID:', doc['uid'])

def print_md(name, doc):
    if name == 'start':
        print('Metadata:\n', repr(doc))

gs.RE.subscribe('start', print_scanid)

from ophyd.commands import wh_pos,log_pos

from ophyd.commands import mov



from eiger_io.fs_handler import EigerHandler
from filestore.api import register_handler
register_handler("AD_EIGER", EigerHandler)

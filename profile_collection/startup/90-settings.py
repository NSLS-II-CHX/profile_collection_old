import logging

# metadata set at startup
RE.md['owner'] = 'xf11id'
RE.md['beamline_id'] = 'CHX'
# removing 'custom' as it is raising an exception in 0.3.2
# gs.RE.md['custom'] = {}

def print_md(name, doc):
    if name == 'start':
        print('Metadata:\n', repr(doc))

RE.subscribe(print_scanid)

#from eiger_io.fs_handler import LazyEigerHandler
#db.fs.register_handler("AD_EIGER", LazyEigerHandler)

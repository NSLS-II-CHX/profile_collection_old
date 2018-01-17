# Make reference to the db instance defined in 00-startup.py.
from eiger_io.fs_handler import EigerHandler
db.reg.register_handler('AD_EIGER2', EigerHandler, overwrite=True)
db.reg.register_handler('AD_EIGER', EigerHandler, overwrite=True)

# if you want to use dask, uncomment these instead
#from eiger_io.fs_handler_dask import EigerHandlerDask
#db.reg.register_handler('AD_EIGER2', EigerHandlerDask, overwrite=True)
#db.reg.register_handler('AD_EIGER', EigerHandlerDask, overwrite=True)

from __future__ import print_function
import epics
import logging

from ophyd.controls import EpicsSignal
from ophyd.controls.signal import SignalGroup


class Shutter(SignalGroup):
    def __init__(self, open=None, open_status=None,
                 close=None, close_status=None):
       super(Shutter, self).__init__()
       signals = [EpicsSignal(open_status, write_pv=open, alias='_open'),
                  EpicsSignal(close_status, write_pv=close, alias='_close'),
                  ]

       for sig in signals:
           self.add_signal(sig)

    def open(self):
        self._open.value = 1

    def close(self):
        self._close.value = 1



fe_sh = Shutter(open='XF:11ID-PPS{Sh:FE}Cmd:Opn-Cmd',
                 open_status='XF:11ID-PPS{Sh:FE}Cmd:Opn-Sts',
                 close='XF:11ID-PPS{Sh:FE}Cmd:Cls-Cmd',
                 close_status='XF:11ID-PPS{Sh:FE}Cmd:Cls-Sts')

foe_sh = Shutter(open='XF:11IDA-PPS{PSh}Cmd:Opn-Cmd',
                open_status='XF:11IDA-PPS{PSh}Cmd:Opn-Sts',
                close='XF:11IDA-PPS{PSh}Cmd:Cls-Cmd',
                close_status='XF:11IDA-PPS{PSh}Cmd:Cls-Sts')


class FastShutter(EpicsSignal):
    def open(self):
        self.put(1)
    
    def close(self):
        self.put(0)

fast_sh = FastShutter('XF:11IDB-ES{Zebra}:SOFT_IN:B0',
                      rw=True, name='fast_sh')





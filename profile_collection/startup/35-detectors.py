from ophyd import (Device, Component as Cpt, EpicsSignalRO)


class XBpm(Device):
    x = Cpt(EpicsSignalRO, 'Pos:X-I')
    y = Cpt(EpicsSignalRO, 'Pos:Y-I')
    a = Cpt(EpicsSignalRO, 'Ampl:ACurrAvg-I')
    b = Cpt(EpicsSignalRO, 'Ampl:BCurrAvg-I')
    c = Cpt(EpicsSignalRO, 'Ampl:CCurrAvg-I')
    d = Cpt(EpicsSignalRO, 'Ampl:DCurrAvg-I')
    



xbpm = XBpm('XF:11IDB-BI{XBPM:02}', name='xbpm')
xbpm.read_attrs = ['x', 'y', 'ca', 'cb', 'cc', 'cd']

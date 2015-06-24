from ophyd.controls import EpicsMotor
from ophyd.controls import EpicsMotor

fs_x = EpicsMotor('XF:11IDB-OP{FS:1-Ax:X}Mtr', name='fs_x')

fs_y = EpicsMotor('XF:11IDB-OP{FS:1-Ax:Y}Mtr', name='fs_y')

fs_p = EpicsMotor('XF:11IDB-OP{FS:1-Ax:P}Mtr', name='fs_p')

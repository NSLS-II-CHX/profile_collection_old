from ophyd.controls import EpicsMotor

class ReversedEpicsMotor(EpicsMotor):
    
    def move(self, position, wait=True, **kwargs):
        return super().move(-position, wait, **kwargs)

    @property
    def position(self):
        return -super().position

    def read(self):
        vals = super().read()
        print('vals = %s' % vals)
        for k, v in vals.items():
            v['value'] = -v['value']
        return vals

# keep this line as example!!!! bst_x = ReversedEpicsMotor('XF:11IDB-ES{Dif-Ax:XV2}Mtr', name='bst_x')
#bst_x = ReversedEpicsMotor('XF:11IDB-ES{Dif-Ax:XV2}Mtr', name='bst_x')
bst_y = ReversedEpicsMotor('XF:11IDB-ES{Dif-Ax:YV}Mtr', name = 'bst_y')
#bst_rot = diff_om

# Alias motors
bst_x = diff_xv2
sam_x = diff_xh
sam_y = diff_yh
#sam_z = diff_zh
#sam_th = diff_thh
#sam_chi = diff_chh
sam_pitch = diff_phh

def att(num):
	if num == 0:
		mov(bst_x,18.)
		mov(bst_y,.17)
	elif num == 1:
		mov(bst_x,25.)
		mov(bst_y,.17)
	elif num == 2:
		mov(bst_x,31.)
		mov(bst_y,.17)

def W_in():
	mov(bst_x,-12.5)
	mov(bst_y,-.6298)


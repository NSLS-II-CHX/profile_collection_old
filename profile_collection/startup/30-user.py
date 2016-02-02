from ophyd import EpicsMotor
from epics import caput

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
bst_x = diff.xv2
sam_x = diff.xh
sam_y = diff.yh
#sam_z = diff_zh
#sam_th = diff_thh
#sam_chi = diff_chh
sam_pitch = diff.phh

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
	mov(bst_x,-12.19)
	mov(bst_y,-.1298)

def W_saxs():
	mov(bst_x,-12.2005)
	mov(bst_y,-.97985)


def launch_4m():
	det=eiger_4M_cam_img
	caput ('XF:11IDB-BI{Det:Eig4M}cam1:SaveFiles', 'Yes')
	gs.RE(Count([det],1,0))

gs.PLOTMODE = 2


def dlup(m,start,stop,nstep):
	plan = DeltaScanPlan([det],m,start,stop,nstep)
	plan.subs=[ LiveTable( [m, str(det.stats1.name)+'_'+str(det.stats1.read_attrs[0])]), LivePlot(x=str(m.name)+'_'+m.read_attrs[0], y=str(det.stats1.name)+'_'+str(det.stats1.read_attrs[0]), markersize=10,  marker='o',color='r' ) ]
	RE(plan)


def alup(m,start,stop,nstep):
	plan = AbsScanPlan([det],m,start,stop,nstep)
	plan.subs=[ LiveTable( [m, str(det.stats1.name)+'_'+str(det.stats1.read_attrs[0])]), LivePlot(x=str(m.name)+'_'+m.read_attrs[0], y=str(det.stats1.name)+'_'+str(det.stats1.read_attrs[0]), markersize=10,  marker='o',color='r' ) ]
	RE(plan)

import time
from ophyd import EpicsMotor
from epics import caput
from filestore import RawHandler

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


def change_motor_name( device):
    for k in device.signal_names:
        if hasattr( getattr(device, k), 'user_readback'):
            getattr(device, k).user_readback.name = getattr(device, k).name
        elif hasattr( getattr(device, k), 'readback'):
            getattr(device, k).readback.name = getattr(device, k).name



for motors in [ diff, bpm2, mbs, dcm, s1, s2, s4]:
    change_motor_name( motors )
    
# Alias motors
bst_x = diff.xv2
sam_x = diff.xh
sam_y = diff.yh
#sam_z = diff_zh
#sam_th = diff_thh
#sam_chi = diff_chh
sam_pitch = diff.phh

def W_in():
	mov(diff.zv,0.20018)
	mov(diff.xv2,9.85)
	mov(diff.yv,1.32992)

def Pt_in():
   mov(diff.zv,0.2003)
   #mov(diff.xv2,-4.74)
   mov(diff.xv2,-4.8901)
   mov(diff.yv,1.32)

def bst_out():
	mov(diff.xv2,-20.)

def s1_in():
	mov(diff.xh,-9.1)		#not the center, but there are lots of cracks...
	mov(diff.yh,-31.0)

def s2_in():
	mov(diff.xh,-4.9)
	mov(diff.yh,-31.7)

def s3_in():
	mov(diff.xh,-.9)
	mov(diff.yh,-31.3)

def s4_in():
	mov(diff.xh,2.95)
	mov(diff.yh,-31.3)

def s5_in():
	mov(diff.xh,7.2)
	mov(diff.yh,-31.3)

def s6_in():
	mov(diff.xh,11.5)
	mov(diff.yh,-31.3)

def Log_Pos( ):
    for motors in [ diff, mbs, dcm, s1, s2, s4, bpm1,bpm2, xbpm ]:
        log_pos( motors )




def launch_4m():
	det=eiger_4M_cam_img
	caput ('XF:11IDB-BI{Det:Eig4M}cam1:SaveFiles', 'Yes')
	gs.RE(Count([det],1,0))

gs.PLOTMODE = 2


def dlup(m,start,stop,nstep):
	plan = DeltaScanPlan([det],m,start,stop,nstep)
	plan.subs=[ LiveTable( [m, str(det.stats1.name)+'_'+str(det.stats1.read_attrs[0])]), LivePlot(x=str(m.name), y=str(det.stats1.name)+'_'+str(det.stats1.read_attrs[0]), markersize=10,  marker='o',color='r' ),spec_cb]
	RE(plan)


def alup(m,start,stop,nstep):
	plan = AbsScanPlan([det],m,start,stop,nstep)
	plan.subs=[ LiveTable( [m, str(det.stats1.name)+'_'+str(det.stats1.read_attrs[0])]), LivePlot(x=str(m.name), y=str(det.stats1.name)+'_'+str(det.stats1.read_attrs[0]), markersize=10,  marker='o',color='r' ),spec_cb]
	RE(plan)

def dscan_bpm_vlt( start, stop, num,  ):
    pv = 'XF:11IDB-BI{XBPM:02}CtrlDAC:BLevel-SP'
    cur_vlt = caget( pv )
    vlt = np.linspace( start, stop, num ) +  cur_vlt
    inten = []
    #fig, ax = plt.subplots()
    for i in vlt:
        caput(  pv, i )
        sleep( 1 )
        inten.append(  xray_eye1.stats1.total.value  )
        # ax.plot(   vlt, np.array( inten),  '-go')
        #ax.plot( i, xray_eye1.stats1.total.value, '-go')
    caput( pv, cur_vlt )
    fig, ax = plt.subplots()
    ax.plot(   vlt, np.array( inten),  '-go')


#diff.xh.user_readback.name = 'diff_xh'

def get_filenames(header):
    keys = [k for k, v in header.descriptors[0]['data_keys'].items() if 'external' in v]
    events = get_events(db[-1], keys, handler_overrides={key: RawHandler for key in keys})
    key, = keys
    unique_filenames = set([ev['data'][key][0] for ev in events])
    return unique_filenames


def show_filenames(name, doc):
    time.sleep(5)
    print('Files generated:', get_filenames(db[doc['run_start']]))


# RE.subscribe('stop', show_filenames)

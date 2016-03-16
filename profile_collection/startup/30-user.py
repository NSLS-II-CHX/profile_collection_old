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
    mov(diff.xv2, 9.69470)
    mov(diff.yv,1.24146)

def Pt_in():
   mov(diff.zv,0.20014)
   #mov(diff.xv2,-4.74)
   #mov(diff.xv2,-4.93060)
   mov(diff.yv,1.31484)

   mov(diff.xv2,-4.8106)
def bst_out():
    mov(diff.xv2,-20.)

def s10_in():
    mov(diff.xh,-11.695)    
    mov(diff.yh,-13.992)

def s9_in():
    mov(diff.xh,-5.42)
    mov(diff.yh,-13.992)

def s8_in():      
    mov(diff.xh,.89)
    mov(diff.yh,-13.992)

def s7_in():
    mov(diff.xh,7.15)
    mov(diff.yh,-13.992)

def s6_in():
    mov(diff.xh,13.67)
    mov(diff.yh,-13.992)

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

def dscan_hdm_p( start, stop, num,  ):
    pv = 'XF:11IDA-OP{Mir:HDM-Ax:P}PID-SP'
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





# 2016 Mar
# CFN specific code

class Sample(object):

    def __init__(self, name, **md):

        self.md = md
        self.md['name'] = name

        self.sample_tilt = 0

    def xr(self, move_amount):
        diff.xh.move( diff.xh.user_readback.value + move_amount, timeout=180 )

    def yr(self, move_amount):
        diff.yh.move( diff.yh.user_readback.value + move_amount, timeout=180 )


    def get_md(self, **md):

        md_current = {}
        md_current['user'] = 'CFN'
        md_current.update(md)
        md_current['energy_keV'] = caget('XF:11IDA-OP{Mono:DCM-Ax:Energy}Mtr.RBV')/1000.0
        md_current['exposure_time'] = caget('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime')
        md_current['sequence_ID'] = caget('XF:11IDB-ES{Det:Eig4M}cam1:SequenceId') + 1
        md_current['sample'] = self.md
        md_current['sample']['x'] = diff.xh.user_readback.value
        md_current['sample']['y'] = diff.yh.user_readback.value
        md_current['sample']['holder'] = 'air capillary holder'
        #md_current['sample']['holder'] = 'vacuum bar holder'

        md_current.update(self.md)
        md_current['x_position'] = md_current['sample']['x']
        md_current['y_position'] = md_current['sample']['y']
        md_current['holder'] = md_current['sample']['holder']

        return md_current


    def snap(self, exposure_time=1, measure_type='snap', **md):

        if exposure_time is not None:
            caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime', exposure_time)

        md_current = self.get_md(**md)
        md_current['measure_type'] = measure_type


        count(**md_current)



    def measure(self, exposure_time=1, measure_type='measure', **md):

        self.snap(exposure_time=exposure_time, measure_type=measure_type, **md)




    def measureSpots(self, num_spots=4, translation_amount=0.03, axis='y', exposure_time=None, measure_type='measureSpots', **md):
        '''Measure multiple spots on the sample.'''

        if 'spot_number' not in self.md:
            self.md['spot_number'] = 1


        for spot_num in range(num_spots):

            self.measure(exposure_time=exposure_time, measure_type=measure_type, **md)

            if axis=='y':
                self.yr(translation_amount)
            elif axis=='x':
                self.xr(translation_amount)
            else:
                print('Axis not recognized.')

            self.md['spot_number'] += 1


    def measureXPCS(self, exposure_time=0.00134, num_frame=2000, measure_type='XPCS', **md):


        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime', exposure_time)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquirePeriod', exposure_time)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:NumImages', num_frame)

        md_current = self.get_md(**md)
        md_current['measure_type'] = measure_type


        count(**md_current)

        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime', 1)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquirePeriod', 1)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:NumImages', 1)


    def measureTimeSeries(self, exposure_time=0.002, num_frame=5000, measure_type='measureTimeSeries', **md):


        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime', exposure_time)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquirePeriod', exposure_time)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:NumImages', num_frame)

        md_current = self.get_md(**md)
        md_current['measure_type'] = measure_type


        count(**md_current)

        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime', 1)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquirePeriod', 1)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:NumImages', 1)

    def gotoOrigin(self):
        diff.xh.move( 0, timeout=180 )
        diff.yh.move( -2.39178, timeout=180 )


    def spiralSearch(self, step_size=0.05, max_stride=10):

        # 1 * +y
        # 1 * +x
        # 2 * -y
        # 2 * -x
        # 3 * +y
        # 3 * +x
        # 4 * -y
        # 4 * -x
        # etc.

        #self.snap()

        stride_length = 1
        polarity = +1
        while(stride_length<max_stride):

            for istride in range(stride_length):
                print('Move y {:.3f}'.format(polarity*step_size))
                self.yr(polarity*step_size)
                self.snap(exposure_time=None)

            for istride in range(stride_length):
                print('Move x {:.3f}'.format(polarity*step_size))
                self.xr(polarity*step_size)
                self.snap(exposure_time=None)

            stride_length += 1
            polarity *= -1


    def gridMeasure(self, nx=10, ny = 10, step_size=.005,exposure_time=None, skip=0, wait_time=None, **md):
        '''  Measure in an nx * ny grid. Move in a snake manner
            Assumes you start in lower left corner.
            SKip the first skip points (useful when a run prematurely ends)
            Note: This starts from wherever you were last positioned. If a 
            run is cancelled, make sure to reposition accordingly before running to
            resume.
        '''
        scl = -1
        xtmp,ytmp = 0,0
        
        for i in range(nx*ny):
            if i > skip:
                self.measure(exposure_time=exposure_time, **md)
                if wait_time is not None:
                    time.sleep(wait_time)
                
            if i%nx == 0:
                # Move up one and now switch move direction
                scl *= -1
                self.yr(step_size)
                #ytmp += step_size
                #print("Now at {}, {}".format(xtmp,ytmp))
            else:
                # move left or right (depends on scl)
                self.xr(step_size*scl)
                #xtmp += step_size*scl
                #print("Now at {}, {}".format(xtmp, ytmp))

                
    def gridMove(self, amt=[0,0], grid_spacing=0.06):
        '''Move in the sample coordinate grid. The amt is [x,y].'''

        tilt = np.radians(self.sample_tilt)

        rot_matrix = np.array( [ 
            [+np.cos(tilt), +np.sin(tilt)],
            [-np.sin(tilt), +np.cos(tilt)]
            ] )

        dv = np.array(np.asarray(amt)*grid_spacing) # vector in sample coordinate system
        dvp = np.dot(dv, rot_matrix) # dx in instrument coordinate system

        print('Move by ({:.4f}, {:.4f})'.format(dvp[0], -dvp[1]))
        self.xr(dvp[0])
        self.yr(-dvp[1])






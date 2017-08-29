import time
from ophyd import EpicsMotor
from epics import caput
from filestore import RawHandler
from math import radians


def beam_on():
	foil_x.move(-22.0)

def beam_off():
	foil_x.move(-21.0)

def eiger4m_feedback():
	caput('XF:11IDB-ES{Det:Eig4M}cam1:ManualTrigger',1)	#set manual trigger mode
	beam_off()
	eiger4m_single.cam.acquire.put(1) 	# opens fast shutter and arms detector
	sleep(1)
	caput('XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP',1)	# feedback on
	caput('XF:11IDB-BI{XBPM:02}Fdbk:AEn-SP',1)
	sleep(2)
	beam_on()
	caput('XF:11IDB-ES{Det:Eig4M}cam1:Trigger',1)   # this needs to be done from BS, not from cha! Could even revert with previous command -> dark images at the beginning, but no beam damage overhead
	caput('XF:11IDB-ES{Det:Eig4M}cam1:ManualTrigger',0)	#remove manual trigger mode


#def movr_samy(d ):
#    '''A temporary solution for move sample in y direction by a combination of xv and zh 
#    d: the relative move distance
#    Octo 21, 2016
#    '''
#    angle=9
#    movr( [diff.xv,diff.xh],[ d/np.sin(  radians(angle)), -1 * d/ np.tan( radians(angle))] )
#    #movr( diff.xv, d/np.sin(  radians(angle)) )
#    #movr( diff.xh, -1 * d/ np.tan( radians(angle)) )

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



for motors in [ diff, bpm2, mbs, dcm, tran, s1, s2, s4]:
    change_motor_name( motors )
    
# Alias motors
#bst_x = diff.xv2
sam_x = diff.xb   # xh,zh stage was dismounted for Headrick experiment
sam_y = diff.yh
sam_phi = diff.phh
#sam_z = diff_zh
#sam_th = diff_thh
#sam_chi = diff_chh
#sam_pitch = diff.phh

#def W_in():
    #mov(diff.zv,0.20016)     - these were for the liquid GI-SAXS setup, Wiegart 2016-1
    #mov(diff.yv, 6.48889)
    #mov(diff.xv2,-21.8501)

def goto_500k():
	caput('XF:11IDB-ES{Det:SAXS-Ax:X}Mtr.VAL',304.6242)
	caput('XF:11IDB-ES{Det:SAXS-Ax:Y}Mtr.VAL',151.7567)   

def goto_4m():
	caput('XF:11IDB-ES{Det:SAXS-Ax:X}Mtr.VAL',477.9539)
	caput('XF:11IDB-ES{Det:SAXS-Ax:Y}Mtr.VAL',83.7567)

def ct_500k(expt=.0001,frame_rate=9000,imnum=1,comment='eiger500K image'):
	caput('XF:11IDB-ES{Det:Eig500K}cam1:FWClear',1)   #remove files from detector
	caput('XF:11IDB-ES{Det:Eig500K}cam1:ArrayCounter',0)
	eiger500K_single.photon_energy.put(9652.0)
	#add some metadata:
	RE.md['transmission']=att.get_T()
	#RE.md['T_yoke']=str(caget('XF:11IDB-ES{Env:01-Chan:C}T:C-I'))
	eiger500K_single.cam.num_images.put(imnum)
	eiger500K_single.cam.acquire_time.put(expt)
	eiger500K_single.cam.acquire_period.put(max([0.000112,1./frame_rate]))
	RE(count([eiger500K_single]),Measurement=comment)
	#remove meta data keys
	a=RE.md.pop('transmission')
	#a=RE.md.pop('T_yoke')

def feedback_ON():
    '''
    feedback_ON()
    moves the pin diode (monitor chamber) in the beam to protect the sample while the fast shutter is opened
    sets attenuator to 1
    opens the fast shutter
    sets att to 1
    turns feedback ON
    '''
    #mov(foil_x, 8)
    beam_off()  #using monitor holder to protect the sample
    #fast_sh.open()
    #att.set_T(1)
    sleep(4)
    caput('XF:11IDA-OP{Mir:HDM-Ax:P}Sts:FB-Sel',0)  #turn off epics pid feedback on HDM encoder
    caput('XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP',1)
    caput('XF:11IDB-BI{XBPM:02}Fdbk:AEn-SP',1)
    sleep(5)
    if caget('XF:11IDB-BI{XBPM:02}Pos:Y-I')>1 or caget('XF:11IDB-BI{XBPM:02}Pos:Y-I')<-1:
        caput('XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP',0)
        sleep(1)
        caput('XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP',1)
    else: pass
    if caget('XF:11IDB-BI{XBPM:02}Pos:X-I')>1 or caget('XF:11IDB-BI{XBPM:02}Pos:X-I')<-1:
        caput('XF:11IDB-BI{XBPM:02}Fdbk:AEn-SP',0)
        sleep(1)
        caput('XF:11IDB-BI{XBPM:02}Fdbk:AEn-SP',1)
    else: pass

def feedback_OFF_backup(): 
    print('moving diode out of the beam')
    fast_sh.close()
    mov(foil_x,-26.) # Empty
    caput('XF:11IDA-OP{Mir:HDM-Ax:P}Sts:FB-Sel',1)  #feedback on HDM ON

def feedback_OFF(): 
	hdm_setpoint=caget('XF:11IDA-OP{Mir:HDM-Ax:P}Pos-I')
	caput('XF:11IDA-OP{Mir:HDM-Ax:P}PID-SP',hdm_setpoint)    
	caput('XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP',0)
	caput('XF:11IDB-BI{XBPM:02}Fdbk:AEn-SP',0)
	caput('XF:11IDA-OP{Mir:HDM-Ax:P}Sts:FB-Sel',1)  #feedback on HDM ON

# alignment/measurement macros are better defined in user specific locations
#def alignment_mode():
#	"""
#	puts beamline into alignment mode: att.set_T(1E-4)
#	mov(saxs_bst.x,119.4151)
#	mov(foil_x,-26.) - empty slot 
#	"""
#	print('putting beamline into alignment mode: transmission: 1E-4, beamstop: out, diagnostics:out')
#	fast_sh.close()
#	att.set_T(1E-4)
#	mov(saxs_bst.x,119.41)
#	mov(foil_x,-26.)
#	detselect(eiger4m_single)
#	caput('XF:11IDB-ES{Det:Eig4M}cam1:SaveFiles',0)
#	print('Not saving the Eiger files ...')
#	eiger4m_single.cam.acquire_time.value=.1
#	eiger4m_single.cam.acquire_period.value=.1
#	eiger4m_single.cam.num_images.value=1
#	#movr(saxs_bst.y1,5.)
#
#def measurement_mode():
#	"""
#	puts beamline into measurement mode: 
#    att.set_T(1)
#	mov(saxs_bst.x,129.41)   !!! absolute !!!
#	"""
#	print('putting beamline into measurement mode: transmission: 1, beamstop: in')
#	print('removing files from detector')
#	caput('XF:11IDB-ES{Det:Eig4M}cam1:FWClear',1)
#	caput('XF:11IDB-ES{Det:Eig4M}cam1:SaveFiles',1)
#	print('Should be also saving files now ...')
#	mov(saxs_bst.x,129.41)
#	att.set_T(1)
#	caput('XF:11IDB-ES{Dif-Ax:PhH}Cmd:Kill-Cmd',1)

def diode_OUT():
	mov(foil_x,-26.)

def diode_IN():
	mov(foil_x,8.)

def snap(det='eiger4m',expt=0.1,comment='Single image'):
    """
    sets exp time (and period) to expt (default 0.1s)
    sets #images and #triggers both to 1
    takes an Eiger image
    """
    if det == 'eiger4m':
        caput('XF:11IDB-ES{Det:Eig4M}cam1:NumImages',1)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:NumTriggers',1)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime',expt)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquirePeriod',expt)
        RE(count([eiger4m_single]),Measurement=comment)
    elif det == 'eiger1m':
        caput('XF:11IDB-ES{Det:Eig1M}cam1:NumImages',1)
        caput('XF:11IDB-ES{Det:Eig1M}cam1:NumTriggers',1)
        caput('XF:11IDB-ES{Det:Eig1M}cam1:AcquireTime',expt)
        caput('XF:11IDB-ES{Det:Eig1M}cam1:AcquirePeriod',expt)
        RE(count([eiger1m_single]),Measurement=comment)

###### sample-detector distance macros for SAXS ##########

def tube_length(tube_nr):
	'''
	function to get tube length of SAXS instrument, from label on tube
	calling sequence: tube_length(tube_nr) -> returns tube length in mm
	tube_nr: see label on instrument. This is only the length of the tube, NOT the sample-detector distance!
	'''
	tube_l=np.array([1758.24,2764.78,3766.66,4616.18,6789.28,9790.93,12792.57,15742.99])-228.22
	if tube_nr >= 0 and tube_nr <=7:
		return tube_l[tube_nr]
	else: raise param_Exception('error: argument tube_nr must be between 0 and 7')
	

def get_saxs_sd(tube_nr,detector='eiger4m'):
	'''
	function returns sample detector distance for SAXS instrument
	based on tube nr, detector and Z1 position
	calling sequence: get_saxs_sd(tube_nr,detector='eiger4m') -> returns sample-detector distance [mm]
	'''
	tube=tube_length(tube_nr)
	if detector == 'eiger4m':
		det_chamber=247.136
	else: raise param_Exception('error: detector '+detector+'currently not defined...')
	sd=273.62+caget('XF:11IDB-ES{Tbl:SAXS-Ax:Z1}Mtr.RBV')+tube+det_chamber
	print('sample-detector distance using tube_nr: '+str(tube_nr)+' detector: '+detector+' at Z1 position '+str(caget('XF:11IDB-ES{Tbl:SAXS-Ax:Z1}Mtr.RBV'))+': '+str(sd)+'mm')
	return sd

def calc_saxs_sd(tube_nr,z1,detector='eiger4m'):
	'''
	function calculates sample detector distance for SAXS instrument
	based on tube nr, detector and Z1 position
	calling sequence: calc_saxs_sd(tube_nr,z1,detector='eiger4m') -> returns sample detector distance [mm]
	'''
	tube=tube_length(tube_nr)
	if detector == 'eiger4m':
		det_chamber=247.136
	else: raise param_Exception('error: detector '+detector+'currently not defined...')
	sd=273.62+z1+tube+det_chamber
	print('sample-detector distance using tube_nr: '+str(tube_nr)+' detector: '+detector+' at Z1 position '+str(z1)+': '+str(sd)+'mm')
	return sd

def update_saxs_sd(tube_nr,detector='eiger4m'):
	'''
	get sample detector distance for SAXS instrument
	based on tube nr, detector and Z1 position and update metadata
	calling sequence: update_saxs_sd(tube_nr,detector='eiger4m')
	'''
	sd=get_saxs_sd(tube_nr,detector='eiger4m')
	if detector == 'eiger4m':
		print('updating metadata in Eiger4M HDF5 file...')
		caput('XF:11IDB-ES{Det:Eig4M}cam1:DetDist',sd/1000.)
	else: raise param_Exception('error: detector '+detector+'currently not defined...')
	

class param_Exception(Exception):
	pass 

########## END sample-detector distance macros for SAXS ####################

# temporary fix for not having the fast shutter
def eiger4m_series(expt=.1,acqp='auto',imnum=5,comment=''):
	"""
	July 2017: fast shutter broken, use edge of empty slot in monitor chamber
	use 'manual' triggering of eiger4m (implemented by Dan)
	"""
	print('start of series: '+time.ctime())
	if acqp=='auto':
		acqp=expt
		#print('setting acquire period to '+str(acqp)+'s')
	if expt <.00134:
			expt=.00134
	else:
			pass
	seqid=caget('XF:11IDB-ES{Det:Eig4M}cam1:SequenceId')+1
	idpath=caget('XF:11IDB-ES{Det:Eig4M}cam1:FilePath',' {"longString":true}')
	caput('XF:11IDB-ES{Det:Eig4M}cam1:FWClear',1)	#remove files from the detector DISABLE FOR MANUAL DOWNLOAD!!!
	caput('XF:11IDB-ES{Det:Eig4M}cam1:ArrayCounter',0) # set image counter to '0'
	if imnum < 500:															# set chunk size
			caput('XF:11IDB-ES{Det:Eig4M}cam1:FWNImagesPerFile',10)
	else: 
			caput('XF:11IDB-ES{Det:Eig4M}cam1:FWNImagesPerFile',100)		
	detector=eiger4m_single
	detector.cam.acquire_time.value=expt   	# setting up exposure for eiger1m/4m_single
	detector.cam.acquire_period.value=acqp
	detector.cam.num_images.value=imnum
	detector.num_triggers.put(1)
	#print('adding metadata: '+time.ctime())
	sleep(2) # needed to ensure values are updated in EPICS prior to reading them back...
	RE.md['exposure time']=str(expt)		# add metadata information about this run
	#print('adding metadata acquire period: '+str(detector.cam.acquire_period.value))
	RE.md['acquire period']=str(acqp)
	RE.md['shutter mode']='single using edge in monitor chamber'
	RE.md['number of images']=str(imnum)
	RE.md['data path']=idpath
	RE.md['sequence id']=str(seqid)
	RE.md['transmission']=att.get_T()
	RE.md['diff_yh']=str(round(diff.yh.user_readback.value,4))
	## add experiment specific metadata:
	#RE.md['T_yoke']=str(caget('XF:11IDB-ES{Env:01-Chan:C}T:C-I'))
	#RE.md['T_sample']=str(caget('XF:11IDB-ES{Env:01-Chan:D}T:C-I'))
	if caget('XF:11IDB-BI{XBPM:02}Fdbk:AEn-SP') == 1:
		RE.md['feedback_x']='on'
	elif caget('XF:11IDB-BI{XBPM:02}Fdbk:AEn-SP') == 0:
		RE.md['feedback_x']='off'
	if caget('XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP') == 1:
		RE.md['feedback_y']='on'
	elif caget('XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP') == 0:
		RE.md['feedback_y']='off'
	## end experiment specific metadata
	## would be nice to make the olog entry here, but how do we get the uid at this stage?
	print('taking data series: exposure time: '+str(expt)+'s,  period: '+str(acqp)+'s '+str(imnum)+'frames')
	print('Dectris sequence id: '+str(int(seqid)))
	### data acquisition
	RE(manual_count(det=eiger4m_single),Measurement=comment)
	beam_on()
	RE.resume()
	beam_off()
	### end data acquisition
	a=RE.md.pop('exposure time')		# remove eiger series specific meta data (need better way to remove keys 'silently'....)
	a=RE.md.pop('acquire period')
	#a=RE.md.pop('shutter mode')
	a=RE.md.pop('number of images')
	a=RE.md.pop('data path')
	a=RE.md.pop('sequence id')
	a=RE.md.pop('diff_yh')
	## remove experiment specific dictionary key
	#a=RE.md.pop('T_yoke')
	#a=RE.md.pop('T_sample')
	a=RE.md.pop('feedback_x')
	a=RE.md.pop('feedback_y')
	a=RE.md.pop('transmission')
	log_manual_count()

# temporary fix for not having the fast shutter
def eiger1m_series(expt=.1,acqp='auto',imnum=5,comment=''):
	"""
	July 2017: fast shutter broken, use edge of empty slot in monitor chamber
	use 'manual' triggering of eiger1m (implemented by Dan)
	"""
	print('start of series: '+time.ctime())
	if acqp=='auto':
		acqp=expt
		#print('setting acquire period to '+str(acqp)+'s')
	if expt <.00033334:
			expt=.00033334
	else:
			pass
	seqid=caget('XF:11IDB-ES{Det:Eig1M}cam1:SequenceId')+1
	idpath=caget('XF:11IDB-ES{Det:Eig1M}cam1:FilePath',' {"longString":true}')
	caput('XF:11IDB-ES{Det:Eig1M}cam1:FWClear',1)	#remove files from the detector DISABLE FOR MANUAL DOWNLOAD!!!
	caput('XF:11IDB-ES{Det:Eig1M}cam1:ArrayCounter',0) # set image counter to '0'
	if imnum < 500:															# set chunk size
			caput('XF:11IDB-ES{Det:Eig1M}cam1:FWNImagesPerFile',10)
	else: 
			caput('XF:11IDB-ES{Det:Eig1M}cam1:FWNImagesPerFile',100)		
	detector=eiger1m_single
	detector.cam.acquire_time.value=expt   	# setting up exposure for eiger1m/4m_single
	detector.cam.acquire_period.value=acqp
	detector.cam.num_images.value=imnum
	detector.num_triggers.put(1)
	#print('adding metadata: '+time.ctime())
	sleep(2) # needed to ensure values are updated in EPICS prior to reading them back...
	RE.md['exposure time']=str(expt)		# add metadata information about this run
	#print('adding metadata acquire period: '+str(detector.cam.acquire_period.value))
	RE.md['acquire period']=str(acqp)
	RE.md['shutter mode']='single using edge in monitor chamber'
	RE.md['number of images']=str(imnum)
	RE.md['data path']=idpath
	RE.md['sequence id']=str(seqid)
	RE.md['transmission']=att.get_T()
	## add experiment specific metadata:
	RE.md['T_yoke']=str(caget('XF:11IDB-ES{Env:01-Chan:C}T:C-I'))
	#RE.md['T_sample']=str(caget('XF:11IDB-ES{Env:01-Chan:D}T:C-I'))
	if caget('XF:11IDB-BI{XBPM:02}Fdbk:AEn-SP') == 1:
		RE.md['feedback_x']='on'
	elif caget('XF:11IDB-BI{XBPM:02}Fdbk:AEn-SP') == 0:
		RE.md['feedback_x']='off'
	if caget('XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP') == 1:
		RE.md['feedback_y']='on'
	elif caget('XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP') == 0:
		RE.md['feedback_y']='off'
	## end experiment specific metadata
	## would be nice to make the olog entry here, but how do we get the uid at this stage?
	print('taking data series: exposure time: '+str(expt)+'s,  period: '+str(acqp)+'s '+str(imnum)+'frames')
	print('Dectris sequence id: '+str(int(seqid)))
	### data acquisition
	RE(manual_count(det=eiger1m_single),Measurement=comment)
	beam_on()
	RE.resume()
	beam_off()
	### end data acquisition
	a=RE.md.pop('exposure time')		# remove eiger series specific meta data (need better way to remove keys 'silently'....)
	a=RE.md.pop('acquire period')
	#a=RE.md.pop('shutter mode')
	a=RE.md.pop('number of images')
	a=RE.md.pop('data path')
	a=RE.md.pop('sequence id')
	## remove experiment specific dictionary key
	a=RE.md.pop('T_yoke')
	#a=RE.md.pop('T_sample')
	a=RE.md.pop('feedback_x')
	a=RE.md.pop('feedback_y')
	a=RE.md.pop('transmission')
	log_manual_count()

# Lutz's test Nov 08 start
def series(det='eiger4m',shutter_mode='single',expt=.1,acqp=.1,imnum=5,comment=''):
	"""
	det='eiger1m' / 'eiger4m'
	shutter_mode='single' / 'multi'
	expt: exposure time [s]
	acqp: acquire period [s] OR 'auto': acqp=expt
	imnum: number of frames
	comment: free comment (string) shown in Olog and attached as RE.md['Measurement']=comment
	update 01/23/2017:  for imnum <100, set chunk size to 10 images to force download. Might still cause problems under certain conditions!!
	"""
	print('start of series: '+time.ctime())
	if acqp=='auto':
		acqp=expt
	if det == 'eiger1m':    #get Dectris sequence ID
		seqid=caget('XF:11IDB-ES{Det:Eig1M}cam1:SequenceId')+1
		idpath=caget('XF:11IDB-ES{Det:Eig1M}cam1:FilePath',' {"longString":true}')
		caput('XF:11IDB-ES{Det:Eig1M}cam1:FWClear',1)	#remove files from the detector
		caput('XF:11IDB-ES{Det:Eig1M}cam1:ArrayCounter',0) # set image counter to '0'
		if imnum < 500:															# set chunk size
			caput('XF:11IDB-ES{Det:Eig1M}cam1:FWNImagesPerFile',10)
		else: 
			caput('XF:11IDB-ES{Det:Eig1M}cam1:FWNImagesPerFile',100)
	elif det == 'eiger4m':
		if expt <.00134:
			expt=.00134
		else:
			pass
		seqid=caget('XF:11IDB-ES{Det:Eig4M}cam1:SequenceId')+1
		idpath=caget('XF:11IDB-ES{Det:Eig4M}cam1:FilePath',' {"longString":true}')
		#caput('XF:11IDB-ES{Det:Eig4M}cam1:FWClear',1)	#remove files from the detector DISABLED FOR MANUAL DOWNLOAD!!!
		caput('XF:11IDB-ES{Det:Eig4M}cam1:ArrayCounter',0) # set image counter to '0'
		if imnum < 500:															# set chunk size
			caput('XF:11IDB-ES{Det:Eig4M}cam1:FWNImagesPerFile',10)
		else: 
			caput('XF:11IDB-ES{Det:Eig4M}cam1:FWNImagesPerFile',100)
	#print('setting detector paramters: '+time.ctime())
	if shutter_mode=='single':
		if det == 'eiger1m':
			detector=eiger1m_single
		if det == 'eiger4m':
			detector=eiger4m_single
		detector.cam.acquire_time.value=expt   	# setting up exposure for eiger1m/4m_single
		detector.cam.acquire_period.value=acqp
		detector.cam.num_images.value=imnum
		#print('adding metadata: '+time.ctime())
		RE.md['exposure time']=str(expt)		# add metadata information about this run
		RE.md['acquire period']=str(acqp)
		RE.md['shutter mode']=shutter_mode
		RE.md['number of images']=str(imnum)
		RE.md['data path']=idpath
		RE.md['sequence id']=str(seqid)
		RE.md['transmission']=att.get_T()
	if shutter_mode=='multi':
#		if 1./acqp*1E3>51000:           # check for fast shutter / vacuum issues....
#			raise series_Exception('error: due to vacuum issues, 1/acqp*1000 !<51000 ')
#		if caget('XF:11IDB-VA{Att:1-CCG:1}P-I') > 8.E-8:
#			print('vacuum in fast shutter section is bad: '+str(caget('XF:11IDB-VA{Att:1-CCG:1}P-I'))+' Torr (need: 8.E-8 Torr)...'+time.ctime()+': going to wait for 15 min!')
#			sleep(900)
#			if caget('XF:11IDB-VA{Att:1-CCG:1}P-I') > 8.E-8:
#				print('vacuum in fast shutter section is bad: '+str(caget('XF:11IDB-VA{Att:1-CCG:1}P-I'))+' Torr -> still bad, going to abort!')
#				raise series_Exception('error: vacuum issue in the fast shutter section...aborting run.')
#			else: print('vacuum level: '+str(caget('XF:11IDB-VA{Att:1-CCG:1}P-I'))+' Torr -> pass!')
		if acqp <.1 and imnum > 5000:
				print('warning: max number frames with shutter >10Hz is 5000....re-setting "imnum" to 5000.')
				imnum=5000
		if expt*acqp < 5.99E-5:
				raise series_Exception('error: shutter duty cycle is too high...make sure expt x acqp <6E-5.')
		if det == 'eiger1m':
			detector=eiger1m
			if expt+caget('XF:11IDB-ES{Det:Eig1M}ExposureDelay-SP') >= acqp or acqp<.019:   # check whether requested parameters are sensible
				raise series_Exception('error: exposure time +shutter time > acquire period or shutter requested to go >50Hz')
			
			caput('XF:11IDB-ES{Det:Eig1M}Mode-Cmd',1)    #enable auto-shutter-mode
			caput('XF:11IDB-ES{Det:Eig1M}NumImages-SP',imnum)
			caput('XF:11IDB-ES{Det:Eig1M}ExposureTime-SP',expt)
			caput('XF:11IDB-ES{Det:Eig1M}AcquirePeriod-SP',acqp)
			detector.cam.acquire_period.value=acqp   # ignored in data acquisition, but gets correct metadata in HDF5 file
		if det == 'eiger4m':
			detector=eiger4m
			if expt+caget('XF:11IDB-ES{Det:Eig4M}ExposureDelay-SP') >= acqp or acqp<.019:
				raise series_Exception('error: exposure time +shutter time > acquire period or shutter requested to go >50Hz')
			caput('XF:11IDB-ES{Det:Eig4M}Mode-Cmd',1)    #enable auto-shutter-mode
			caput('XF:11IDB-ES{Det:Eig4M}NumImages-SP',imnum)
			caput('XF:11IDB-ES{Det:Eig4M}ExposureTime-SP',expt)
			caput('XF:11IDB-ES{Det:Eig4M}AcquirePeriod-SP',acqp)
			detector.cam.acquire_period.value=acqp   # ignored in data acquisition, but gets correct metadata in HDF5 file
		RE.md['exposure time']=expt		# add metadata information about this run
		RE.md['acquire period']=acqp
		RE.md['shutter mode']=shutter_mode
		RE.md['number of images']=imnum
		RE.md['data path']=idpath
		RE.md['sequence id']=str(seqid)
		RE.md['transmission']=att.get_T()
	#print('adding experiment specific metadata: '+time.ctime())
	## add experiment specific metadata:
	RE.md['T_yoke']=str(caget('XF:11IDB-ES{Env:01-Chan:C}T:C-I'))
	RE.md['T_sample']=str(caget('XF:11IDB-ES{Env:01-Chan:D}T:C-I'))
	if caget('XF:11IDB-BI{XBPM:02}Fdbk:AEn-SP') == 1:
		RE.md['feedback_x']='on'
	elif caget('XF:11IDB-BI{XBPM:02}Fdbk:AEn-SP') == 0:
		RE.md['feedback_x']='off'
	if caget('XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP') == 1:
		RE.md['feedback_y']='on'
	elif caget('XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP') == 0:
		RE.md['feedback_y']='off'
	## end experiment specific metadata
	print('taking data series: exposure time: '+str(expt)+'s,  period: '+str(acqp)+'s '+str(imnum)+'frames  shutter mode: '+shutter_mode)
	print('Dectris sequence id: '+str(int(seqid)))
	#print('executing count: '+time.ctime())
	RE(count([detector]),Measurement=comment)
	#print('remove metadata: '+time.ctime())	
	a=RE.md.pop('exposure time')		# remove eiger series specific meta data (need better way to remove keys 'silently'....)
	a=RE.md.pop('acquire period')
	a=RE.md.pop('shutter mode')
	a=RE.md.pop('number of images')
	a=RE.md.pop('data path')
	a=RE.md.pop('sequence id')
	## remove experiment specific dictionary key
	a=RE.md.pop('T_yoke')
	a=RE.md.pop('T_sample')
	a=RE.md.pop('feedback_x')
	a=RE.md.pop('feedback_y')
	a=RE.md.pop('transmission')

class series_Exception(Exception):
	pass

# heating with sample chamber, using both heaters:
def set_temperature(Tsetpoint,heat_ramp=2,cool_ramp=1,log_entry='on'):       # MADE MAJOR CHANGES: NEEDS TESTING!!! [01/23/2017 LW]
	"""
	heating with sample chamber, using both heaters
	macro maintains 40deg difference between both heaters to have a temperature gradient for stabilization
	Tsetpoint: temperature setpoint in deg Celsius!
	heat_ramp: ramping speed [deg.C/min] on heating. Because of heater issues, currently a ramp with max 2deg.C/min will be enforced!
	cool_ramp: ramping speed [deg.C/min] on cooling. '0' -> ramp off!
	log_entry: 'on' / 'off'  -> make olog entry when changing temperature ('try', ignored, if Olog is down...)
	"""
	if heat_ramp > 2.:
		heat_ramp=2.
	else: pass
	if cool_ramp==0:
		cool_ramp_on=0
	else:  cool_ramp_on=1
	
	start_T=caget('XF:11IDB-ES{Env:01-Chan:C}T:C-I')
	start_T2=caget('XF:11IDB-ES{Env:01-Chan:B}T:C-I')
	if start_T >= Tsetpoint:		# cooling requested 
		caput('XF:11IDB-ES{Env:01-Out:1}Enbl:Ramp-Sel',0)  # ramp off
		caput('XF:11IDB-ES{Env:01-Out:2}Enbl:Ramp-Sel',0)				          
		caput('XF:11IDB-ES{Env:01-Out:1}T-SP',273.15+start_T)	# start from current temperature
		caput('XF:11IDB-ES{Env:01-Out:2}T-SP',273.15+start_T2)
		if cool_ramp==0:																				# print message and make Olog entry, if requested
			print('cooling Channel C to '+str(Tsetpoint)+'deg, no ramp')
			sleep(5)  # need time to update setpoint....
			if log_entry == 'on':
				try:
					olog_client.log( 'Changed temperature to T='+ str(Tsetpoint)[:5]+'C, ramp: off')
				except:
					pass
			else: pass
		elif cool_ramp >0:
			print('cooling Channel C to '+str(Tsetpoint)+'deg @ '+str(cool_ramp)+'deg./min')	
			if log_entry == 'on':
				try:
					olog_client.log( 'Changed temperature to T='+ str(Tsetpoint)[:5]+'C, ramp: '+str(cool_ramp)+'deg./min')
				except:
					pass
			else: pass
		#caput('XF:11IDB-ES{Env:01-Out:1}Enbl:Ramp-Sel',cool_ramp_on)		#switch ramp on/off as requested
		#caput('XF:11IDB-ES{Env:01-Out:2}Enbl:Ramp-Sel',cool_ramp_on)
		caput('XF:11IDB-ES{Env:01-Out:1}Val:Ramp-SP',cool_ramp)   # set ramp to requested value
		caput('XF:11IDB-ES{Env:01-Out:2}Val:Ramp-SP',cool_ramp)
		sleep(5)
		caput('XF:11IDB-ES{Env:01-Out:1}Enbl:Ramp-Sel',cool_ramp_on)		#switch ramp on/off as requested
		caput('XF:11IDB-ES{Env:01-Out:2}Enbl:Ramp-Sel',cool_ramp_on)
		caput('XF:11IDB-ES{Env:01-Out:1}T-SP',273.15+Tsetpoint)	# setting channel C to Tsetpoint
		caput('XF:11IDB-ES{Env:01-Out:2}T-SP',233.15+Tsetpoint) # setting channel B to Tsetpoint-40C
	elif start_T<Tsetpoint:		#heating requested, ramp on
		print('heating Channel C to '+str(Tsetpoint)+'deg @ '+str(heat_ramp)+'deg./min')
		sleep(5)	
		if log_entry == 'on':
			try:
				olog_client.log( 'Changed temperature to T='+ str(Tsetpoint)[:5]+'C, ramp: '+str(heat_ramp)+'deg./min')
			except:
				pass
		else: pass
		caput('XF:11IDB-ES{Env:01-Out:1}Enbl:Ramp-Sel',0)  # ramp off
		caput('XF:11IDB-ES{Env:01-Out:2}Enbl:Ramp-Sel',0)
		caput('XF:11IDB-ES{Env:01-Out:1}T-SP',273.15+start_T)	# start from current temperature
		caput('XF:11IDB-ES{Env:01-Out:2}T-SP',273.15+start_T2)
		caput('XF:11IDB-ES{Env:01-Out:1}Val:Ramp-SP',heat_ramp)   # set ramp to selected value or allowed maximum
		caput('XF:11IDB-ES{Env:01-Out:2}Val:Ramp-SP',heat_ramp)
		caput('XF:11IDB-ES{Env:01-Out:1}Out:MaxI-SP',.5) # force max current to 0.5 Amp
		caput('XF:11IDB-ES{Env:01-Out:2}Out:MaxI-SP',.7)
		caput('XF:11IDB-ES{Env:01-Out:1}Val:Range-Sel',3) # force heater range 3 -> should be able to follow 2deg/min ramp
		caput('XF:11IDB-ES{Env:01-Out:2}Val:Range-Sel',3)
		sleep(5)
		caput('XF:11IDB-ES{Env:01-Out:1}Enbl:Ramp-Sel',1)  # ramp on
		caput('XF:11IDB-ES{Env:01-Out:2}Enbl:Ramp-Sel',1)
		caput('XF:11IDB-ES{Env:01-Out:1}T-SP',273.15+Tsetpoint)	# setting channel C to Tsetpoint
		caput('XF:11IDB-ES{Env:01-Out:2}T-SP',233.15+Tsetpoint) # setting channel B to Tsetpoint-40C


# wait for temperature NOT TESTED YET
def wait_temperature(wait_time=1200,dead_band=1.,channel=1,log_entry='on'):
	"""
	"""
	sleep(5) # make sure previous changes to the Lakehsore settings are updated...
	ch=['none','XF:11IDB-ES{Env:01-Chan:A}T:C-I','XF:11IDB-ES{Env:01-Chan:B}T:C-I','XF:11IDB-ES{Env:01-Chan:C}T:C-I','XF:11IDB-ES{Env:01-Chan:D}T:C-I']
	#check on which temperature the selected channel feedbacks:
	if channel==1:
		ch_num=caget('XF:11IDB-ES{Env:01-Out:1}Out-Sel')
		ramp=caget('XF:11IDB-ES{Env:01-Out:1}Val:Ramp-RB')
		T_set=caget('XF:11IDB-ES{Env:01-Out:1}T-SP') - 273.15
		ramp_on=caget('XF:11IDB-ES{Env:01-Out:1}Enbl:Ramp-Sel')
	elif channel==2:
		ch_num=caget('XF:11IDB-ES{Env:01-Out:2}Out-Sel')
		ramp=caget('XF:11IDB-ES{Env:01-Out:2}Val:Ramp-RB')
		T_set=caget('XF:11IDB-ES{Env:01-Out:2}T-SP') - 273.15
		ramp_on=caget('XF:11IDB-ES{Env:01-Out:2}Enbl:Ramp-Sel')
	else: raise check_Exception('error: control channel has to be either "1" or "2"!')
	curr_T=caget(ch[ch_num])
	# estimate how long it will take to reach the temperature setpoint:
	if ramp_on==1:
		dtime=abs(T_set-curr_T)/ramp
	else:
		print('temperature ramping is off...checking temperature increase vs. time...this will take several minutes....')
		sleep(120) # wait 2 minutes (overcome T-inertia)
		dtime=get_T_gradient(channel)
	print(time.ctime()+ '   initial estimate to reach T='+str(T_set)[:5]+'C on channel '+caget('XF:11IDB-ES{Env:01-Out:1}Out-Sel','char')+': '+str(dtime)[:5]+' minutes')
	# initial wait for reaching setpoint temperature
	dT=T_set-caget(ch[ch_num])
	while abs(dT)>2*dead_band:
		sleep(min([abs(dtime)*60,300]))		# get an update after max 5 minutes...
		dtime=(T_set-caget(ch[ch_num]))/(abs(get_T_gradient(channel))+.1)
		dT=T_set-caget(ch[ch_num])  #why was this commented??
		print(time.ctime()+ '       updated estimate to reach T='+str(T_set)[:5]+'C on channel '+caget('XF:11IDB-ES{Env:01-Out:1}Out-Sel','char')+': '+str(dtime)[:5]+' minutes    current temperature: '+str(caget(ch[ch_num]))[:5]+'C')
	print('hurray! temperature within 2x deadband! Going to check for stability....waiting max 1x wait_time to stabilize + 1x wait_time!')
	check=0
	period=0	
	while check<10 and period<5:
		if get_T_stability(wait_time,channel, dead_band) ==1:
			period=period+1
		elif get_T_stability(wait_time,channel, dead_band) ==0:
			period=0
		check=check+1
	if period == 5:
		message=time.ctime()+'    achieved T='+str(T_set)+' +/- '+str(dead_band)+'C for '+str(wait_time)+'s'
	elif period<5 and check==10:
		message=time.ctime()+'    failed to achieve T='+str(T_set)+' +/- '+str(dead_band)+'C for '+str(wait_time)+'s, required stability achieved for ~'+str(period*wait_time/5)+'s only'
	print(message)
	if log_entry=='on':
		olog_entry(message)
	else: pass
		

def get_T_stability(wait_time,channel,dead_band):
	"""
	checks whether the temperatures is within the deadband for 1/5 of the total waiting time
	-> yes: returns 1 | no: returns 0
	"""
	ch=['none','XF:11IDB-ES{Env:01-Chan:A}T:C-I','XF:11IDB-ES{Env:01-Chan:B}T:C-I','XF:11IDB-ES{Env:01-Chan:C}T:C-I','XF:11IDB-ES{Env:01-Chan:D}T:C-I']
	ch_num=caget('XF:11IDB-ES{Env:01-Out:'+str(channel)+'}Out-Sel')	
	temperatures=np.zeros(int(wait_time/5))
	for i in range(int(wait_time/5)):
		sleep(1)
		temperatures[i]=caget(ch[ch_num])-(caget('XF:11IDB-ES{Env:01-Out:'+str(channel)+'}T-SP') - 273.15)
	if max(abs(temperatures))>dead_band:
		T_stability_pass=0
	elif max(abs(temperatures))<=dead_band:
		T_stability_pass=1
	return T_stability_pass
	
	
def get_T_gradient(channel):
	"""
	returns temperature gradient on control channel in deg.C/min
	"""
	ch=['none','XF:11IDB-ES{Env:01-Chan:A}T:C-I','XF:11IDB-ES{Env:01-Chan:B}T:C-I','XF:11IDB-ES{Env:01-Chan:C}T:C-I','XF:11IDB-ES{Env:01-Chan:D}T:C-I']
	ch_num=caget('XF:11IDB-ES{Env:01-Out:'+str(channel)+'}Out-Sel')	
	T1=caget(ch[ch_num])
	t1=time.time()
	sleep(60)
	T2=caget(ch[ch_num])
	t2=time.time()
	T_gradient=60*abs(T2-T1)/(t2-t1)
	return T_gradient

def olog_entry(string):
	"""
	wrapper for making an olog entry within a 'try / except: pass' sequence, to avoid hanging up, in case olog is not reachable
	calling sequence: olog_entry(string)
	"""
	try:
		olog_client.log(string)
	except:
		pass

# Lutz's test Nov 08 end

# begin test better function to check if beam is available for experiment + better recovery [Jan 2017]
def check_ring():
	if caget('SR-OPS{}Mode-Sts',1) == 'Operations' and caget('SR:C11-EPS{PLC:1}Sts:ID_BE_Enbl-Sts') ==1 and caget('SR:C03-BI{DCCT:1}I:Real-I') >200:
		ring_ok=1
		print('checking for SR ring status...seems ok')
	else:
		ring_ok=0
		print('checking for SR ring status...seems there is a problem')		
	return ring_ok

def wait_for_ring(wait_after=0):
	ring_ok=check_ring()
	if ring_ok==0:
		while ring_ok==0:
			print('no beam in SR ring...checking again in 5 minutes.')
			sleep(300)
			ring_ok=check_ring()
		sleep(wait_after)
	if ring_ok==1: pass

def check_bl():
	"""
	macro to check whether stable beam can be obtained on the DBPM
	opens all shutters, checks whether beam is blocked by diode
	checks for feedback stays on (-> enough intensity on DBPM)
	checks for feedback running (-> deviation of <.5um combined error in X & Y in slow readout)
	"""
	print('checking beamline for beam available...')
	mov(foil_x,8)
	if 	foil_x.user_readback.value<8.5 and foil_x.user_readback.value>7.5:
		fe_sh.open()
		foe_sh.open()
		fast_sh.open()
		att.set_T(1)
		feedback_ON()
		sleep(2)
		if caget('XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP')==1 and caget('XF:11IDB-BI{XBPM:02}Fdbk:AEn-SP')==1 and abs(caget('XF:11IDB-BI{XBPM:02}Pos:X-I'))+abs(caget('XF:11IDB-BI{XBPM:02}Pos:Y-I'))<.5:
			bl_ok=1
			print('################################\n')
			print('checked beamline: beam on DBPM, all ok!')
		else:
			bl_ok=0
			print('################################\n')
			print('checked beamline: NO beam on DBPM, not ready for experiment....')
	else: raise check_Exception('error: cannot block beam in ES with diode, abort beamline check')

def check_recover():
	print('checking SR ring and BL for beam available and try to recover if necessary....')
	ring_ok=check_ring()
	if ring_ok==1:
		pass
	elif ring_ok==0:
		print('looks like a beam loss in the SR ring...')
		try:
			olog_client.log('looks like a beam loss in the SR ring...trying to recover')
		except: pass	
		wait_for_ring()
	bl_ok=check_bl()
	if bl_ok==1:
		pass
	elif bl_ok==0:
		print('beam in SR, but not at DBPM...trying to recover...')
		try:
			olog_client.log('beam in SR, but not at DBPM...trying to recover...')
		except: pass	
		caput('XF:11IDB-BI{XBPM:02}Fdbk:AEn-SP',0)	# DBPM feedback off
		caput('XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP',0)
		caput('XF:11IDA-OP{Mir:HDM-Ax:P}Sts:FB-Sel',1) # Epics feedback on HDM on
		sleep(8)
		if abs(caget('XF:11IDA-OP{Mir:HDM-Ax:P}PID-SP')-caget('XF:11IDA-OP{Mir:HDM-Ax:P}Pos-I'))>.5:
			print('Beam in Storage ring, but cannot recover at BL side...')
			try:
				olog_client.log('Beam in Storage ring, but cannot recover at BL side...possible problem wiht PID loop on SIEPA3P')
			except: pass	
			raise check_Exception('error: looks like the PID loop on SIEPA3P is NOT running, abort recovery attempt')
		else: pass
		caput('XF:11IDB-BI{XBPM:02}CtrlDAC:BLevel-SP',caget('XF:11IDB-BI{XBPM:02}CtrlDAC:BLevel-SP')) # enforce last known (good) DAC outputs
		caput('XF:11IDB-BI{XBPM:02}CtrlDAC:ALevel-SP',caget('XF:11IDB-BI{XBPM:02}CtrlDAC:ALevel-SP'))
		caput('XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP',1)
		sleep(10)
		caput('XF:11IDA-OP{Mir:HDM-Ax:P}Sts:FB-Sel',0)
		caput('XF:11IDB-BI{XBPM:02}Fdbk:AEn-SP',1)			# back to feedback on DBPM
		sleep(10)
		bl_ok=check_bl()
		if bl_ok==0:
			feeback_ON()	# one last chance...
		else: pass
		bl_ok=check_bl()
		if bl_ok==1:
			print('Successfully recovered! Hurray!')
			try:
				olog_client.log('Successfully recoverd beam loss. Check data for impact of possible non-ideal alignment.')
			except: 
				pass	
		elif bl_ok==0:
			try:
				olog_client.log('Beam in Storage ring, but cannot recover at BL side...abort recovery attempt')
			except: pass	
			raise check_Exception('error: could not recover beam on BL side...abort!')
			

	
class check_Exception(Exception):
    pass
    """
    class to raise exceptions during beamline auto-check and recovery
    """

# end test better function to check if beam is available for experiment + better recovery

def check_cryo(level_threshold=55.):
	"""
	checking whether cryo-cooler refill is in progress or initiating refill, if current level is below threshold.
	waits for refill to be completed and reports current filling level
	calling sequence: check_cryo(level_threshold=55.)
	"""
	if caget('XF:11IDA-UT{Cryo:1}L:19-I')<level_threshold or caget('XF:11IDA-UT{Cryo:1-IV:19}Pos-I') >10.:
		if caget('XF:11IDA-UT{Cryo:1-IV:19}Pos-I') >10.:
			print('cryo-cooler refill in progress, wait for completion. Current filling level: '+ str(caget('XF:11IDA-UT{Cryo:1}L:19-I'))[:5]+'%')
		elif caget('XF:11IDA-UT{Cryo:1}L:19-I')<level_threshold and caget('XF:11IDA-UT{Cryo:1-IV:19}Pos-I') <10.:
			print('cryo-cooler level: '+ str(caget('XF:11IDA-UT{Cryo:1}L:19-I'))[:5]+'% -> going to refill cryo_cooler')
		else: pass
		caput('XF:11IDA-UT{Cryo:1-IV:19}Pos-SP',100)
		refill_on=1
		#print('cryo-cooler level: '+ str(caget('XF:11IDA-UT{Cryo:1}L:19-I'))+'-> going to refill cryo_cooler')
		while refill_on==1:
			sleep(60)
			if caget('XF:11IDA-UT{Cryo:1-IV:19}Pos-I') >10.:
				print('cryo-cooler refill in progress, filling level: '+str(caget('XF:11IDA-UT{Cryo:1}L:19-I'))[:5])
			elif caget('XF:11IDA-UT{Cryo:1-IV:19}Pos-I') <10.:
				print('cryo-cooler refill complete!')
				refill_on=0
	else:
		print('cryo-cooler level: '+ str(caget('XF:11IDA-UT{Cryo:1}L:19-I'))[:5]+'-> no refill at this time')

# reference position horz kinoform lens 1 (horz focus for SAXS), 9.65 keV 05/29/2017
def kinoform_focus(foc='horz_SAXS_9650'):
	if foc == 	'horz_SAXS_9650':
		mov([k1.z,k1.x,k1.y,k1.chi,k1.theta,k1.phi,k1.lx,k1.ly],[5.,-.0524,1.8324,2.0,-.25,1.52,.768,7.016])
	if foc == 	'vert_WAXS_9750':
		mov([k1.z,k1.x,k1.y,k1.chi,k1.theta,k1.phi,k1.lx,k1.ly],[-20.,4.95,-3.167,2.0,-.98,-.68,9.244,3.93])
	if foc == 	'vert_WAXS_12800':
		mov([k1.z,k1.x,k1.y,k1.chi,k1.theta,k1.phi,k1.lx,k1.ly],[0.,4.55,-3.167,2.65,.2,-.68,9.098,4.916])
	if foc == 	'horz_WAXS_12800':
		mov([k2.z,k2.x,k2.y,k2.chi,k2.theta,k2.phi,k2.lx,k2.ly],[0.,0.002,4.6,.2,-1.24,-2.,-.868,6.975])
	if foc == 	'horz_WAXS_9750':
		mov([k2.z,k2.x,k2.y,k2.chi,k2.theta,k2.phi,k2.lx,k2.ly],[0.,-.44,4.6,.2,-1.24,-2.,-.868,7.049])




#def movr_samx(value):
#	movr(diff.xh,-value)
#	movr(diff.xv2,-value)


### python based kinematics for rotation of SAXS table's WAXS section #### 03/08/2017
# WAXS section rotation
def WAXS_rot_setup():          
	WAXS_angle=np.arange(0,17.2,.2)
	x1_pos= 1399*2*np.pi/360.*WAXS_angle
	x2_pos=5144.23*np.sin((WAXS_angle-4.008)/180*np.pi)+359.56
	x2_velocity=np.array([3.669,3.669,3.669,3.67,3.671,3.672,3.672,3.673,3.674,3.674,3.675,3.675,3.675,3.676,3.676,3.676,3.677,3.677,3.677,3.677,3.677,3.677,3.677,3.677,3.677,3.677,3.676,3.676,3.676,3.675,3.675,3.675,3.674,3.674,3.673,3.672,3.672,3.671,3.67,3.669,3.669,3.668,3.667,3.666,3.665,3.664,3.663,3.661,3.66,3.659,3.658,3.656,3.655,3.653,3.652,3.651,3.649,3.647,3.646,3.644,3.642,3.64,3.639,3.637,3.635,3.633,3.631,3.629,3.627,3.625,3.622,3.62,3.618,3.616,3.613,3.611,3.608,3.606,3.603,3.601,3.598,3.595,3.593,3.59,3.587,3.584])
	return [WAXS_angle,x1_pos,x2_pos,x2_velocity]

def WAXS_rot_pos():
	'''
	calculates current rotation angle for SAXS table's WAXS section from X1 and X2 positions via a look-up table
	'''
	[WAXS_angle,x1_pos,x2_pos,x2_velocity]=WAXS_rot_setup()
	WAXS_angle=np.array(WAXS_angle)
	x1_pos=np.array(x1_pos)
	x2_pos=np.array(x2_pos)
	x2_velocity=np.array(x2_velocity)
	### WAXS angle according to X1:	
	if SAXS_x1.position >415.09 or SAXS_x1.position <=-.2:
		raise rotation_exception('error: position of X1 is out of range')	
	elif SAXS_x1.position <0:
		WAXS_angle_x1=0
	elif SAXS_x1.position <415.09 and SAXS_x1.position >=0:
		WAXS_angle_x1 = np.interp(SAXS_x1.position,x1_pos,WAXS_angle)
	### WAXS angle according to X2:	
	if SAXS_x2.position >1516.06 or SAXS_x1.position <=-.2:
		raise rotation_exception('error: position of X2 is out of range')	
	elif SAXS_x2.position <0:
		WAXS_angle_x2=0
	elif SAXS_x2.position <1516.06 and SAXS_x2.position >=0:
		WAXS_angle_x2 = np.interp(SAXS_x2.position,x2_pos,WAXS_angle)
	curr_WAXS_angle=0.5*(WAXS_angle_x1+WAXS_angle_x2)
	print('WAXS rotation according to X1: '+str(WAXS_angle_x1)+'  WAXS rotation according to X2: '+str(WAXS_angle_x2)+'  -> WAXS rotation: ~'+str(curr_WAXS_angle))
	return curr_WAXS_angle

def WAXS_rotation(angle):
	'''
	moves SAXS table's WAXS section to desired rotation angle in 2 deg steps, using lookup table for positions and X2 velocity
	WAXS_rotation(angle) -> angle [deg.]
	'''
	max_angle=14.1 #hard coded limit for current setup	
	[WAXS_angle,x1_pos,x2_pos,x2_velocity]=WAXS_rot_setup()
	WAXS_angle=np.array(WAXS_angle)
	x1_pos=np.array(x1_pos)
	x2_pos=np.array(x2_pos)
	x2_velocity=np.array(x2_velocity)
	if angle <0 or angle>max_angle:
		raise rotation_exception('error: requested rotation angle out of range')
	curr_WAXS_angle=WAXS_rot_pos()
	#curr_WAXS_angle=7.9 ### fake for test
	if angle >= curr_WAXS_angle:
		direction=1
	elif angle < curr_WAXS_angle:
		direction=-1
	print('going to move WAXS section from '+str(curr_WAXS_angle)+' to: '+str(angle))
	while abs(angle - curr_WAXS_angle) > 1:		# moving in 1 deg steps
		curr_velocity= np.interp((curr_WAXS_angle+direction*.5),WAXS_angle,x2_velocity)
		curr_X1=np.interp((curr_WAXS_angle+direction*1),WAXS_angle,x1_pos)
		curr_X2=np.interp((curr_WAXS_angle+direction*1),WAXS_angle,x2_pos)
		print('moving to: '+str(curr_WAXS_angle+direction*1)+' setting X2 velocity to '+str(curr_velocity)+'  X1 -> '+str(curr_X1)+'  X2 -> '+str(curr_X2))
		# need to do the actual moves here:
		SAXS_x2.velocity.value=curr_velocity
		mov([SAXS_x1,SAXS_x2],[curr_X1,curr_X2])
		curr_WAXS_angle=WAXS_rot_pos()		# the real thing...
		#curr_WAXS_angle=curr_WAXS_angle+direction*1 #faking move for testing
	# moving the balance:
	if abs(angle - curr_WAXS_angle) <1.2:
		curr_X1=np.interp(angle,WAXS_angle,x1_pos)
		curr_X2=np.interp(angle,WAXS_angle,x2_pos)
		print('moving to: '+str(angle)+'  X1 -> '+str(curr_X1)+'  X2 -> '+str(curr_X2))	
		# need to do the actual move here:
		mov([SAXS_x1,SAXS_x2],[curr_X1,curr_X2])
	else: raise rotation_exception('error: discrepancy from where the rotation is expected to be....')


class rotation_exception(Exception):
	pass

#Amplifier stage - J.Lhermitte et al.
#amp_x = EpicsMotor('XF:11IDB-OP{BS:Samp-Ax:X}Mtr', name='amp_x')
#amp_y = EpicsMotor('XF:11IDB-OP{Stg:Samp-Ax:Phi}Mtr', name='amp_y')
#amp_z = EpicsMotor('XF:11IDB-OP{BS:Samp-Ax:Y}Mtr', name='amp_z')


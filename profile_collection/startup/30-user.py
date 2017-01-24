import time
from ophyd import EpicsMotor
from epics import caput
from filestore import RawHandler
from math import radians

def movr_samy(d ):
    '''A temporary solution for move sample in y direction by a combination of xv and zh 
    d: the relative move distance
    Octo 21, 2016
    '''
    angle=9
    movr( [diff.xv,diff.xh],[ d/np.sin(  radians(angle)), -1 * d/ np.tan( radians(angle))] )
    #movr( diff.xv, d/np.sin(  radians(angle)) )
    #movr( diff.xh, -1 * d/ np.tan( radians(angle)) )

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
#sam_x = diff.xh
#sam_y = diff.yh
#sam_z = diff_zh
#sam_th = diff_thh
#sam_chi = diff_chh
#sam_pitch = diff.phh

#def W_in():
    #mov(diff.zv,0.20016)     - these were for the liquid GI-SAXS setup, Wiegart 2016-1
    #mov(diff.yv, 6.48889)
    #mov(diff.xv2,-21.8501)
    



def feedback_ON():
    mov(foil_x, 8)
    fast_sh.open()
    att.set_T(1)
    sleep(4)
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

def feedback_OFF(): 
    print('moving diode out of the beam')
    fast_sh.close()
    mov(foil_x,-26.) # Empty

def alignment_mode():
	"""
	put beamline into alignment mode: att.set_T(1E-4)
	movr(saxs_bst.y1,-5)
	mov(foil_x,-26.) 
	"""
	print('putting beamline into alignment mode: transmission: 1E-4, beamstop: out, diagnostics:out')
	fast_sh.close()
	att.set_T(1E-4)
	movr(saxs_bst.y1,-5.)
	mov(foil_x,-26.)
	detselect(eiger4m_single)
	eiger4m_single.cam.acquire_time.value=.1
	eiger4m_single.cam.acquire_period.value=.1
	eiger4m_single.cam.num_images.value=1
	

def measurement_mode():
	"""
	put beamline into measurement mode: att.set_T(1)
	mov(saxs_bst.y1,-189.1)   !!! absolute !!!
	"""
	print('putting beamline into measurement mode: transmission: 1, beamstop: in')
	print('removing files from detector')
	caput('XF:11IDB-ES{Det:Eig4M}cam1:FWClear',1)
	mov(saxs_bst.y1,-189.1)
	att.set_T(1)
	caput('XF:11IDB-ES{Dif-Ax:PhH}Cmd:Kill-Cmd',1)

def diode_OUT():
	mov(foil_x,-26.)

def snap(expt=0.1,comment='Single image'):
    """
    sets exp time (and period) to expt (default 0.1s)
    sets #images and #triggers both to 1
    takes an Eiger image
    """
    caput('XF:11IDB-ES{Det:Eig4M}cam1:NumImages',1)
    caput('XF:11IDB-ES{Det:Eig4M}cam1:NumTriggers',1)
    caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime',expt)
    caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquirePeriod',expt)
    RE(count([eiger4m_single]),Measurement=comment)



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
	if acqp=='auto':
		acqp=expt
	if det == 'eiger1m':    #get Dectris sequence ID
		seqid=caget('XF:11IDB-ES{Det:Eig1M}cam1:SequenceId')+1
		idpath=caget('XF:11IDB-ES{Det:Eig1M}cam1:FilePath',' {"longString":true}')
		aput('XF:11IDB-ES{Det:Eig1M}cam1:FWClear',1)	#remove files from the detector
		caput('XF:11IDB-ES{Det:Eig1M}cam1:ArrayCounter',0) # set image counter to '0'
		if imnum < 100:															# set chunk size
			caput('XF:11IDB-ES{Det:Eig1M}cam1:FWNImagesPerFile',10)
		else: 
			caput('XF:11IDB-ES{Det:Eig1M}cam1:FWNImagesPerFile',100)
	elif det == 'eiger4m':
		seqid=caget('XF:11IDB-ES{Det:Eig4M}cam1:SequenceId')+1
		idpath=caget('XF:11IDB-ES{Det:Eig4M}cam1:FilePath',' {"longString":true}')
		caput('XF:11IDB-ES{Det:Eig4M}cam1:FWClear',1)	#remove files from the detector
		caput('XF:11IDB-ES{Det:Eig4M}cam1:ArrayCounter',0) # set image counter to '0'
		if imnum < 100:															# set chunk size
			caput('XF:11IDB-ES{Det:Eig4M}cam1:FWNImagesPerFile',10)
		else: 
			caput('XF:11IDB-ES{Det:Eig4M}cam1:FWNImagesPerFile',100)
	if shutter_mode=='single':
		if det == 'eiger1m':
			detector=eiger1m_single
		if det == 'eiger4m':
			detector=eiger4m_single
		detector.cam.acquire_time.value=expt   	# setting up exposure for eiger1m/4m_single
		detector.cam.acquire_period.value=acqp
		detector.cam.num_images.value=imnum
		RE.md['exposure time']=str(detector.cam.acquire_time.value)		# add metadata information about this run
		RE.md['acquire period']=str(detector.cam.acquire_period.value)
		RE.md['shutter mode']=shutter_mode
		RE.md['number of images']=str(detector.cam.num_images.value)
		RE.md['data path']=idpath
		RE.md['sequence id']=str(seqid)
	if shutter_mode=='multi':
		if det == 'eiger1m':
			detector=eiger1m
			if expt+caget('XF:11IDB-ES{Det:Eig1M}ExposureDelay-SP') >= acqp or acqp<.01:   # check whether requested parameters are sensible
				raise series_Exception('error: exposure time +shutter time > acquire period or shutter requested to go >100Hz')
			caput('XF:11IDB-ES{Det:Eig1M}Mode-Cmd',1)    #enable auto-shutter-mode
			caput('XF:11IDB-ES{Det:Eig1M}NumImages-SP',imnum)
			caput('XF:11IDB-ES{Det:Eig1M}ExposureTime-SP',expt)
			caput('XF:11IDB-ES{Det:Eig1M}AcquirePeriod-SP',acqp)
			detector.cam.acquire_period.value=acqp   # ignored in data acquisition, but gets correct metadata in HDF5 file
		if det == 'eiger4m':
			detector=eiger4m
			if expt+caget('XF:11IDB-ES{Det:Eig4M}ExposureDelay-SP') >= acqp or acqp<.01:
				raise series_Exception('error: exposure time +shutter time > acquire period or shutter requested to go >100Hz')
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
	RE(count([detector]),Measurement=comment)
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
			if log_entry == 'on':
				try:
					olog_client.log( 'Changed temperature to T='+ str(caget('XF:11IDB-ES{Env:01-Out:1}T-SP')-273.15)[:5]+'C, ramp: off')
				except:
					pass
			else: pass
		elif cool_ramp >0:
			print('cooling Channel C to '+str(Tsetpoint)+'deg @ '+str(cool_ramp)+'deg./min')	
			if log_entry == 'on':
				try:
					olog_client.log( 'Changed temperature to T='+ str(caget('XF:11IDB-ES{Env:01-Out:1}T-SP')-273.15)[:5]+'C, ramp: '+str(cool_ramp)+'deg./min')
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
		if log_entry == 'on':
			try:
				olog_client.log( 'Changed temperature to T='+ str(caget('XF:11IDB-ES{Env:01-Out:1}T-SP')-273.15)[:5]+'C, ramp: '+str(heat_ramp)+'deg./min')
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
		T_set=caget('XF:11IDB-ES{Env:1-Out:2}T-SP') - 273.15
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
		sleep(min([dtime*60,300]))		# get an update after max 5 minutes...
		dtime=1./get_T_gradient(channel)
		dT=T_set-caget(ch[ch_num]) 
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

def wait_for_ring():
	ring_ok=check_ring()
	if ring_ok==0:
		while ring_ok==0:
			print('no beam in SR ring...checking again in 5 minutes.')
			sleep(300)
			ring_ok=check_ring()
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


def movr_samx(value):
	movr(diff.xh,-value)
	movr(diff.xv2,-value)

def launch_4m():
    det=eiger_4M_cam_img
    caput ('XF:11IDB-BI{Det:Eig4M}cam1:SaveFiles', 'Yes')
    gs.RE(Count([det],1,0))

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

def yg_snap(**subs ):
    movr(diff.xh,.7)
    caput('XF:11IDB-ES{Det:Eig4M}cam1:NumImages',subs['frames'])
    caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime',subs['acq'])
    caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquirePeriod',subs['acq'])
    count(**RE.md)
    movr(diff.xh,-.7)
    caput('XF:11IDB-ES{Det:Eig4M}cam1:NumImages',1)
    caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime',.1)
    caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquirePeriod',.1)

def get_R(header_si, header_rh):
    datsi=get_table(header_si)
    datrh=get_table(header_rh)
    th_B=-datsi.dcm_b
    En=xf.get_EBragg('Si111cryo',th_B)
    Rsi=datsi.elm_sum_all
    Rrh=datrh.elm_sum_all
    plt.close(99)
    plt.figure(99)
    plt.semilogy(En,Rsi/Rrh,'ro-')
    plt.xlabel('E [keV]');plt.ylabel('R_si / R_rh')
    plt.grid()
    return Rsi/Rrh




# 2016 Mar
# CFN specific code

class Sample(object):

    def __init__(self, name, **md):

        self.md = md
        self.md['name'] = name

        self.sample_tilt = 0 # degrees
        self.references = None # referenc points for gridMoveAbs

        # sample_tilt positive means sample (and scattering) is misrotated counter-clockwise

    def xr(self, move_amount):
        target = diff.xh.user_readback.value + move_amount
        diff.xh.move( target, timeout=180 )
        diff.xh.move( target, timeout=180 )

    def yr(self, move_amount):
        target = diff.yh.user_readback.value + move_amount
        diff.yh.move( target, timeout=180 )
        diff.yh.move( target, timeout=180 )


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
        #md_current['sample']['holder'] = 'air capillary holder'
        #md_current['sample']['holder'] = 'vacuum bar holder (kinematic)'
        md_current['sample']['holder'] = 'air bar holder (kinematic)'

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


        #count(**md_current)
        RE(count([eiger4m_single]),**md_current)



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

                
    def gridMove(self, amt=[0,0], grid_spacing=0.075):
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



    def gridMoveAbs(self, amt=[0,0], grid_spacing=0.075):
        '''Move in the sample coordinate grid. The amt is [x,y].
            Moves with respect to a reference point
        '''
        if self.references is None:
            print("Error, no reference point set, please set\
                by selecting addreferencepoint.")
        
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


def measurecustom1():
    x0 = 0.715003
    y0 = -0.46736
    dx = 0.075
    dy = 0.075
    mov(diff.yh,y0)
    mov(diff.xh,x0)
    # neg move
    # up on sample
    jlst = -(np.arange(8)-3)
    ilst = [0]
    for j in jlst:
        for i in ilst:
            mov(diff.yh,y0-j*dy)
            mov(diff.xh, x0+i*dx)
            mov(diff.yh,y0-j*dy)
            mov(diff.xh, x0+i*dx)
            sam.measure(600,comment="box ({},{})".format(12+j,16+i))

def measurecustom2():
    print("tile structures")
    # ref coordinates:
    #print("WARNING : need optimized box (5,3) poxition")
    #x0 = 0.715003
    #y0 = -0.46736
    #reference coordinates box label:
    #box is y,x pair where y increasing goes down and x increasing right
    box0 = 3,5
    #x0, y0 = -.486268, -1.05503 # from box (4,0) tile 2
    #x0, y0 = -.485841, -.90597 # from box (6,1) tile 4
    x0, y0 = -.106606, -1.13920# box 2,3, (x,y
    dx = 0.075
    dy = 0.075
    mov(diff.yh,y0)
    mov(diff.xh,x0)
    #mov(sam_x, -.33532-0.075*3);mov(sam_y, -1.13244 -0.075*3);

    #tile 1,2,3,4 elements 0 to 3:
    #positive y is down and pos x is right
    jlst = [4]
    ilst = [0, 1, 2, 3,4,5,6]
          
    for i in ilst:
        for j in jlst:
            mov(diff.yh,y0+j*dy)
            mov(diff.xh, x0+i*dx)
            mov(diff.yh,y0+j*dy)
            mov(diff.xh, x0+i*dx)
            sam.measure(600,comment="box ({},{})".format(box0[0]+j,box0[1]+i))

    #tile 1,2,4 elements 4 to 8 (same ref box, (5,3)):
    #positive y is up and pos x is right
    #jlst = [-2,-1,1]
    #ilst = np.arange(8)-3
          
    #for j in jlst:
        #for i in ilst:
            #mov(diff.yh,y0-j*dy)
            #mov(diff.xh, x0+i*dx)
            #mov(diff.yh,y0-j*dy)
            #mov(diff.xh, x0+i*dx)
            #sam.measure(600,comment="box ({},{})".format(box0[0]-j,box0[1]+i))

def measurecustom3():
    print("hex structures vary number, 60 sec exposures")
    #reference coordinates box label:
    #box is y,x pair where y increasing goes down and x increasing right
    #box0 = 0, 15 # (y,x)
    #x0, y0 = .632094, -1.37608# box 0, 15 (y,x)
    #box0 = 4, 15 # (y,x)
    #x0, y0 = 0.6400, -1.07768 # box (4, 15) 
    
    box0 = 9, 15
    x0, y0=.644901, -.68919

    dx = 0.075
    dy = 0.075

    mov(diff.yh,y0)
    mov(diff.xh,x0)

    #positive y is down and pos x is right
    jlst = [0, 1, 2, 3, 4, 5, 6, 7]
    ilst = [-6, -5, -4, -3, -2, -1, 0, 1]
          
    for i in ilst:
        for j in jlst:
            mov(diff.yh,y0+j*dy)
            mov(diff.xh, x0+i*dx)
            mov(diff.yh,y0+j*dy)
            mov(diff.xh, x0+i*dx)
            sam.measure(60,comment="box ({},{}) (5x5 hex arrays vary N)".format(box0[0]+j,box0[1]+i))

    #tile 1,2,4 elements 4 to 8 (same ref box, (5,3)):
    #positive y is up and pos x is right
    #jlst = [-2,-1,1]
    #ilst = np.arange(8)-3
          
    #for j in jlst:
        #for i in ilst:
            #mov(diff.yh,y0-j*dy)
            #mov(diff.xh, x0+i*dx)
            #mov(diff.yh,y0-j*dy)
            #mov(diff.xh, x0+i*dx)
            #sam.measure(600,comment="box ({},{})".format(box0[0]-j,box0[1]+i))


#template
    
def measurecustomscratch():
    x0 = .03765
    y0 = -.99294
    dx = 0.075
    dy = 0.075
    mov(diff.yh,y0)
    mov(diff.xh,x0)

    jlst = [0]
    ilst = [-4, -5, -6, -7]
    for j in jlst:
        for i in ilst:
            mov(diff.yh,y0-j*dy)
            mov(diff.xh, x0+i*dx)
            mov(diff.yh,y0-j*dy)
            mov(diff.xh, x0+i*dx)
            sam.measure(600,comment="box ({},{})".format(5-j,i+7))


    jlst = [2, 1, -1, -2]
    ilst = [-7, -6, -5, -4, -3,-2, -1,0,1]
    for j in jlst:
        for i in ilst:
            mov(diff.yh,y0-j*dy)
            mov(diff.xh, x0+i*dx)
            mov(diff.yh,y0-j*dy)
            mov(diff.xh, x0+i*dx)
            sam.measure(600,comment="box ({},{})".format(6-j,i+7))

    #this ref is box (9,16) upper right box of lower right quad
    x0 = .71645
    y0 = -.68810
    jlst = [0, -1, -2, -3, -4, -5, -6, -7]
    ilst = [0,-1, -2, -3, -4, -5, -6, -7]
    for j in jlst:
        for i in ilst:
            mov(diff.yh,y0-j*dy)
            mov(diff.xh, x0+i*dx)
            mov(diff.yh,y0-j*dy)
            mov(diff.xh, x0+i*dx)
            sam.measure(600,comment="box ({},{})".format(6-j,i+7))
          


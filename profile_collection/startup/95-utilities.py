# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 14:02:59 2015
by LW March 2015
set of utility functions for beamline alingment and commissioning
v 0.0.1 (this version): might have created a typo in E-calibration!!!
                        added dcm_roll for calculating DCM Roll correction
"""

############
##################
####
def E_calibration(file,Edge='Cu',xtal='Si111cryo',B_off=0):
    """
    by LW 3/25/2015
    function to read energy scan file and determine offset correction
    calling sequence: E_calibration(file,Edge='Cu',xtal='Si111cryo',B_off=0)
    file: path/filename of experimental data; 'ia' opens interactive dialog
    Edge: elment used for calibration
    xtal: monochromator crystal under calibration
    B_off (optional): apply offset to Bragg angle data
    currently there is no check on input parameters!
    """
    # read the data file 
    import csv
    import numpy as np
    import matplotlib.pyplot as plt
    #import xfuncs as xf
    #import Tkinter, tkFileDialog
        
    if file=='ia':          # open file dialog
        print('this would open a file input dialog IF Tkinter was available in the $%^& python environment as it used to')
        #root = Tkinter.Tk()
        #root.withdraw()
        #file_path = tkFileDialog.askopenfilename()
        description=file_path
    elif isinstance(file, str) and file!='ia':
        file_path=file
        descritpion=file_path
    elif isinstance(file,dict) and 'start' in file.keys():
       databroker_object=1
       description='scan # ',header.start['scan_id'],' uid: ', header.start['uid'][:10]
    plt.close("all")
    Edge_data={'Cu': 8.979, 'Ti': 4.966}
    if databroker_object !=1:
       Bragg=[]
       Gap=[]
       Intensity=[]
       with open(file_path, 'rb') as csvfile:
           filereader = csv.reader(csvfile, delimiter=' ')
           filereader.next()   # skip header lines
           filereader.next()
           filereader.next()
           for row in filereader:              # read data
               try: Bragg.append(float(row[2]))
               except: print('could not convert: ',row[2])
               try: Gap.append(float(row[5]))
               except: print('could not convert: ',row[5])
               try: Intensity.append(float(row[7]))
               except: print('could not convert: ',row[8])
    elif databroker_object==1:
       data = get_table(file)
       Bragg = data.dcm_b[1:]     #retrive the data (first data point is often "wrong", so don't use
       #Gap = data.SR:C11-ID:G1{IVU20:1_readback[1:] name is messed up in databroker -> currently don't use gap
       Intensity = data.elm_sum_all [1:] 			#need to find signal from electrometer...elm is commented out in detectors at the moment...???														


    B=np.array(Bragg)*-1.0+B_off
    #G=np.array(Gap[0:len(B)])   # not currently used, but converted for future use
    Int=np.array(Intensity[0:len(B)])
        
    # normalize and remove background:
    Int=Int-min(Int)
    Int=Int/max(Int)

    plt.figure(1)
    plt.plot(B,Int,'ko-',label='experimental data')
    plt.plot([xf.get_Bragg(xtal,Edge_data[Edge])[0],xf.get_Bragg(xtal,Edge_data[Edge])[0]],[0,1],'r--',label='Edge for: '+Edge)
    plt.legend(loc='best')
    plt.xlabel(r'$\theta_B$ [deg.]')
    plt.ylabel('intensity')
    plt.title(['Energy Calibration using: ',description])
    plt.grid()
        
    plt.figure(2)
    Eexp=xf.get_EBragg(xtal,B)
    plt.plot(Eexp,Int,'ko-',label='experimental data')
    plt.plot([Edge_data[Edge],Edge_data[Edge]],[0,1],'r--',label='Edge for: '+Edge)
    plt.legend(loc='best')
    plt.xlabel('E [keV.]')
    plt.ylabel('intensity')
    plt.title(['Energy Calibration using: ',description])
    plt.grid()
        
    # calculate derivative and analyze:
    Bragg_Edge=xf.get_Bragg(xtal,Edge_data[Edge])[0]
    plt.figure(3)
    diffdat=np.diff(Int)
    plt.plot(B[0:len(diffdat)],diffdat,'ko-',label='diff experimental data')
    plt.plot([Bragg_Edge,Bragg_Edge],[min(diffdat),max(diffdat)],'r--',label='Edge for: '+Edge)
    plt.legend(loc='best')
    plt.xlabel(r'$\theta_B$ [deg.]')
    plt.ylabel('diff(int)')
    plt.title(['Energy Calibration using: ',description])
    plt.grid()
        
    plt.figure(4)
    plt.plot(xf.get_EBragg(xtal,B[0:len(diffdat)]),diffdat,'ko-',label='diff experimental data')
    plt.plot([Edge_data[Edge],Edge_data[Edge]],[min(diffdat),max(diffdat)],'r--',label='Edge for: '+Edge)
    plt.legend(loc='best')
    plt.xlabel('E [keV.]')
    plt.ylabel('diff(int)')
    plt.title(['Energy Calibration using: ',description])
    plt.grid()
        
    edge_index=np.argmax(diffdat)
    B_edge=xf.get_Bragg(xtal,Edge_data[Edge])[0]
        
    print('') 
    print('Energy calibration for: ',description)
    print('Edge used for calibration: ',Edge)
    print('Crystal used for calibration: ',xtal)
    print('Bragg angle offset: ', B_edge-B[edge_index],'deg. (CHX coordinate system: ',-(B_edge-B[edge_index]),'deg.)')
    print('=> move Bragg to ',-B[edge_index],'deg. and set value to ',-Bragg_Edge,'deg.')
    print( 'Energy offset: ',Eexp[edge_index]-Edge_data[Edge],' keV')

def dcm_roll(Bragg,offset,distance,offmode='mm',pixsize=5.0):
    """
    by LW 03/27/2015
    function to calculate Roll correction on the DCM
    calling sequence: dcm_roll(Bragg,offset,distance,offmode='mm',pixsize=5.0)
    Bragg: set of Bragg angles
    offset: set of corresponding offsets
    offmode: units of offsets = mm or pixel (default:'mm')
    pixsize: pixel size for offset conversion to mm, if offsets are given in pixels
    default is 5um (pixsize is ignored, if offmode is 'mm')
    distance: DCM center of 1st xtal to diagnostic/slit [mm]
    preset distances available: 'dcm_bpm',dcm_mbs', 'dcm_sample'
    """
    import numpy as np
    from scipy import optimize
    from matplotlib import pyplot as plt
    Bragg=np.array(Bragg)
    if offmode=='mm':
        offset=np.array(offset)
    elif offmode=='pixel':
        offset=np.array(offset)*pixsize/1000.0
    else: raise CHX_utilities_Exception('Eror: offmode must be either "mm" or "pixel"')
    if distance=='dcm_bpm':    
        d=3000.0 # distance dcm-bpm in mm
    elif distance=='dcm_mbs':
        d=2697.6 #distance dcm-mbs in mm
    elif distance=='dcm_sample':
        d=16200 #distance dcm-sample in mm
    else:
        try:
            d=float(distance)
        except:
            raise CHX_utilities_Exception('Eror: distance must be a recognized string or numerical value')    
        
    # data fitting    
    fitfunc = lambda p, x: p[0]+2*d*p[1]*np.sin(x/180.*np.pi) # Target function
    errfunc = lambda p, x, y: fitfunc(p, Bragg) - y # Distance to the target function
    p0 = [np.mean(offset), -.5] # Initial guess for the parameters
    p1, success = optimize.leastsq(errfunc, p0[:], args=(Bragg, offset))
    
    # plotting the result:    
    plt.close(1)    
    plt.figure(1)
    B = np.linspace(Bragg.min(), Bragg.max(), 100)
    plt.plot(Bragg,offset,'ro',label='measured offset')
    plt.plot(B,fitfunc(p1,B),'k-',label=r'$x_o$+2*D*$\Delta$$\Phi$*sin($\theta_B$)')
    plt.legend(loc='best')
    plt.ylabel('beam offset [mm]')
    plt.xlabel('Bragg angle  [deg.]')
    print('x_0= ',p1[0],'mm')
    print('\Delta \Phi= ',p1[1]*180.0/np.pi,'deg')
    

def get_ID_calibration(gapstart,gapstop,gapstep=.2,gapoff=0,sl=300):
    """
    by LW 04/20/2015
    function to automatically take a ID calibration curve_fit
    calling sequence: get_ID_calibration(gapstart,gapstop,gapstep=.2,gapoff=0,sl=300)
	gapstart: minimum gap used in calibration (if <5.2, value will be set to 5.2)
	gapstop: maximum gap used in calibration
	gapstep: size of steps between two gap points
	gapoff: offset applied to calculation gap vs. energy from xfuncs.get_Es(gap-gapoff)
	sl: sleep between two gap points (to avoid overheating the DCM Bragg motor) 
    writes outputfile with fitted value for the center of the Bragg scan to:  '/home/xf11id/Repos/chxtools/chxtools/X-ray_database/
	changes 03/18/2016: made compatible with python V3 and latest versio of bluesky (working on it!!!)
    """
    import numpy as np
    #import xfuncs as xf
    #from dataportal import DataBroker as db, StepScan as ss, DataMuxer as dm
    import time
    from epics import caput, caget
    from matplotlib import pyplot as plt
    from scipy.optimize import curve_fit
    gaps=np.arange(gapstart,gapstop,gapstep)-gapoff   # not sure this should be '+' or '-' ...
    print('ID calibration will contain the following gaps [mm]: ',gaps)
    if caget('XF:11IDA-OP{Mono:DCM-Ax:X}Pos-Sts') == 1:
        xtal='Si111cryo'
    elif caget('XF:11IDA-OP{Mono:DCM-Ax:X}Pos-Sts') == 2:
        xtal='Si220cryo'
    else: raise CHX_utilities_Exception('error: trying to do ID gap calibration with no crystal in the beam')
    print('using ',xtal,' for ID gap calibration')
    # create file for writing calibration data:
    fn='id_CHX_IVU20_'+str(time.strftime("%m"))+str(time.strftime("%d"))+str(time.strftime("%Y"))+'.dat'
    fpath='/home/xf11id/Repos/chxtools/chxtools/X-ray_database/'
    try:
      outFile = open(fpath+fn, 'w')
      outFile.write('% data from measurements '+str(time.strftime("%D"))+'\n')
      outFile.write('% K colkumn is a placeholder! \n')
      outFile.write('% ID gap [mm]     K      E_1 [keV] \n')
      outFile.close()
      print('successfully created outputfile: ',fpath+fn)
    except: raise CHX_utilities_Exception('error: could not create output file')
    
    ### do the scanning and data fitting, file writing,....
    center=[]
    E1=[]
    realgap=[]
    detselect(xray_eye1)
    print(gaps)
    for i in gaps:
        if i>= 5.2:
            B_guess=-1.0*xf.get_Bragg(xtal,xf.get_Es(i+gapoff,5)[1])[0]
        else:
         i=5.2
         B_guess=-1.0*xf.get_Bragg(xtal,xf.get_Es(i,5)[1])[0]
        if i > 8:
           exptime=caget('XF:11IDA-BI{Bpm:1-Cam:1}cam1:AcquireTime')
           caput('XF:11IDA-BI{Bpm:1-Cam:1}cam1:AcquireTime',2*exptime)
        print('initial guess: Bragg= ',B_guess,' deg.   ID gap = ',i,' mm')
        if xf.get_Es(i,5)[1] < 9.5 and round(caget('XF:11IDA-OP{Mir:HDM-Ax:Y}Mtr.VAL'),1) != -7.5:
            caput('XF:11IDA-OP{Mir:HDM-Ax:Y}Mtr.VAL',-7.5)  # use HDM Si stripe
            time.sleep(20)
        elif xf.get_Es(i,5)[1] >= 9.5 and round(caget('XF:11IDA-OP{Mir:HDM-Ax:Y}Mtr.VAL'),1) != 7.5:
            caput('XF:11IDA-OP{Mir:HDM-Ax:Y}Mtr.VAL',7.5)   # use HDM Rh stripe
            time.sleep(20)
        if round(caget('XF:11IDA-BI{Foil:Bpm-Ax:Y}Mtr'),1) != 0.0:
            caput('XF:11IDA-BI{Foil:Bpm-Ax:Y}Mtr',0.0)
            time.sleep(30)
        else: pass
        print('moving DCM Bragg angle to: ',B_guess,' deg and ID gap to ',i,' mm')
        dcm.b.timeout=1200	#make sure dcm motions don't timeout...
        dcm.en.timeout=1200
        mov(dcm.b,B_guess)
        mov(ivu_gap,i)
        print('hurray, made it up to here!')
        RE(ascan(dcm.b,float(B_guess-.4),float(B_guess+.4),60))   # do the Bragg scan
        header = db[-1]					#retrive the data (first data point is often "wrong", so don't use
        data = get_table(header)
        B = data.dcm_b[2:]
        intdat = data.xray_eye1_stats1_total[2:] 																	
        B=np.array(B)
        intdat=np.array(intdat)
        A=np.max(intdat)          # initial parameter guess and fitting
        xc=B[np.argmax(intdat)]
        w=.2
        yo=np.mean(intdat)
        p0=[yo,A,xc,w]
        print('initial guess for fitting: ',p0)
        try:
            coeff,var_matrix = curve_fit(gauss,B,intdat,p0=p0)
            center.append(coeff[2])
            E1.append(xf.get_EBragg(xtal,-coeff[2])/5.0)
            realgap.append(caget('SR:C11-ID:G1{IVU20:1-LEnc}Gap'))
#   # append data file by i, 1 & xf.get_EBragg(xtal,-coeff[2]/5.0):
            with open(fpath+fn, "a") as myfile:
                myfile.write(str(caget('SR:C11-ID:G1{IVU20:1-LEnc}Gap'))+'    1.0 '+str(float(xf.get_EBragg(xtal,-coeff[2])/5.0))+'\n')
            print('added data point: ',caget('SR:C11-ID:G1{IVU20:1-LEnc}Gap'),' ',1.0,'     ',str(float(xf.get_EBragg(xtal,-coeff[2])/5.0)))
        except: print('could not evaluate data point for ID gap = ',i,' mm...data point skipped!')
        time.sleep(sl)
    plt.close(234)
    plt.figure(234)
    plt.plot(E1,realgap,'ro-')
    plt.xlabel('E_1 [keV]')
    plt.ylabel('ID gap [mm]')
    plt.title('ID gap calibration in file: '+fpath+fn,size=12)
    plt.grid()
    
    
    
        
class CHX_utilities_Exception(Exception):
    pass
    """
    by LW 03/19/2015
    class to raise xfuncs specific exceptions
    """   
    
    
    
    
    

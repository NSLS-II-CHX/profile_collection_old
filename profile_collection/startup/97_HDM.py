

CHA_Vol_PV = 'XF:11IDB-BI{XBPM:02}CtrlDAC:ALevel-SP'
HDM_Encoder_PV  = 'XF:11IDA-OP{Mir:HDM-Ax:P}Pos-I' 


E=np.arange(9.,11.,.05)
SI_STRIPE = -5
RH_STRIPE = 5

def take_Rdata( voltage, E):
    caput(CHA_Vol_PV, voltage)    
    #yield from bp.abs_set(hdm.y, RH_STRIPE)
    hdm.y.user_setpoint.value = RH_STRIPE
    sleep( 3.0 )
    E_scan(list(E))
    hrh=db[-1]
    #yield from bp.abs_set(hdm.y, Si_STRIPE)
    hdm.y.user_setpoint.value = SI_STRIPE
    sleep( 3.0 )
    E_scan(list(E))
    hsi=db[-1]
    return get_R( hsi, hrh )

voltage_CHA = [ 3.5, 4.0, 4.5, 5.0, 5.5]

r_eng=np.array(np.loadtxt("/home/xf11id/Downloads/R_Rh_0p180.txt"))[:,0]/1e3
rsi_0p18=np.array(np.loadtxt("/home/xf11id/Downloads/R_Si_0p180.txt"))[:,1]
rrh_0p18=np.array(np.loadtxt("/home/xf11id/Downloads/R_Rh_0p180.txt"))[:,1]

def get_Rdata( voltage_CHA, E ):
     
    fig, ax = plt.subplots()
    ax.plot(r_eng,rsi_0p18/rrh_0p18,label="calc 0.18 deg")
    ax.set_xlabel("E [keV]")
    ax.set_ylabel("R_Si/R_Rh")
    for voltage in voltage_CHA:
        R_SiRh =  take_Rdata( voltage, E)
        HDM_Encoder = caget ( HDM_Encoder_PV )
        ax.plot(E,R_SiRh/R_SiRh[1:5].mean(),label="%s V, %s urad"%(voltage,HDM_Encoder) )
    ax.legend()





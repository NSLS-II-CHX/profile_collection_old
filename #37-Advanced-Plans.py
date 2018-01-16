def pre_reflectivity_scan( phh_start=0, phh_end=1.0, number=10,  
        transmission_step = .1, acquisition_time=.1, threshold = 100 ):
'''A tentative scan for reflectivity in order to find the optimal transmission/acquisition_time

    Each scan point should have three parameters, the scan angle( phh), transmission (by attenuator setting), detector acquisition time (short for small angle, long for large angle)
Input:
    phh_start: the start phh ( the angle around x-axis, PV name: XF:11IDB-ES{Dif-Ax:PhH}Mtr.DESC
    phh_end: the end phh
    number: the scan number of phh
    transmission: 
    acquisition time:
Output:
    optimal transmission/acquisition time for each scan point

'''
    for i, phh in enumerate(np.linspace( phh_start, phh_end, number)):
        #yield from bp.abs_set( diff.phh, phh )
        mov( diff.phh, phh)
        att_t = transmission**i #this line should be changed, the transmission should be determined by detector/roi max intensity
        att.set_T( att_t )
        acqt = acquisition_time
        #yield from bp.abs_set(eiger4m.cam.acquire_period, acqt )
        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime',  acqt )
        #yield from count( [eiger4m_single])
        count( [eiger4m_single])
        #img = load_data( uid =None, detector = 'eiger4m_single_image' )
        img= get_image( db[-1], 'eiger4m_single_image'][0]
        inten = get_det_max_roi_inten( img )
        








   
def get_det_max_roi_inten( img, w = 100, h=100 ):
    '''Get intensity of a roi with width and heigth as w and h
      The center of the roi is the pixel with maximun intensity of the image
      Return the value of roi intensity
    '''
    
    pos = np.where( img ==img.max()  )
    roi = [ pos[0] - w//2, pos[0] + w//2, pos[1] - h//2, pos[1]+h//2]
    img_ = img[roi[0]:roi[1], roi[2]:roi[3]]
    return np.sum( img_ )



def load_data( uid=None, detector = 'eiger4m_single_image', fill=True, reverse=False):
    """load bluesky scan data by giveing uid and detector
          
      Parameters
      ----------
      uid: unique ID of a bluesky scan
      detector: the used area detector
      fill: True to fill data
      reverse: if True, reverse the image upside down to match the "real" image geometry (should always be True in the future)
      Returns
      -------
      image data: a pims frames series
      if not success read the uid, will return image data as 0
      Usuage:
      imgs = load_data( uid, detector  )
      md = imgs.md
      """  
    if uid==None:
        uid=-1
    hdr = db[uid]
    flag =1
    while flag<2 and flag !=0:
        try:
            ev, = get_events(hdr, [detector], fill=fill)
            flag = 0
        except:
            flag += 1
            print ('Trying again ...!')

    if flag:
        try:
            imgs = get_images( hdr, detector)
            if len(imgs[0])==1:
                md = imgs[0].md
                imgs = pims.pipeline(lambda img:  img[0])(imgs)
                imgs.md = md
        except:
            print ("Can't Load Data!")
            uid = '00000'  #in case of failling load data
            imgs = 0
    else:
        imgs = ev['data'][detector]
    if reverse:
        md = imgs.md
        imgs=reverse_updown( imgs )
        imgs.md = md
    return imgs

















def detselect(detector_object, suffix="_stats_total1"):
    """Switch the active detector and set some internal state"""
    gs.DETS =[detector_object]
    gs.PLOT_Y = detector_object.name + suffix
    gs.TABLE_COLS = [gs.PLOT_Y] 


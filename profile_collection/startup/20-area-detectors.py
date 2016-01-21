from ophyd import (ProsilicaDetector, SingleTrigger, TIFFPlugin,
                   ImagePlugin, StatsPlugin, DetectorBase)
from ophyd.areadetector.filestore_mixins import FileStoreTIFFIterativeWrite
from ophyd import Component as Cpt


class Elm(SingleTrigger, DetectorBase):
    pass


class TIFFPluginWithFileStore(TIFFPlugin, FileStoreTIFFIterativeWrite):
    pass


class StandardProsilica(SingleTrigger, ProsilicaDetector):
    tiff = Cpt(TIFFPluginWithFileStore, suffix='TIFF1:',
               write_path_template='/XF11ID/data/')
    image = Cpt(ImagePlugin, 'image1:')
    stats1 = Cpt(StatsPlugin, 'Stats1:')
    stats2 = Cpt(StatsPlugin, 'Stats2:')
    stats3 = Cpt(StatsPlugin, 'Stats3:')
    stats4 = Cpt(StatsPlugin, 'Stats4:')
    stats5 = Cpt(StatsPlugin, 'Stats5:')


class EigerDetector(SingleTrigger, AreaDetector):
    pass


xray_eye1 = StandardProsilica('XF:11IDA-BI{Bpm:1-Cam:1}', name='xray_eye1')
# These two are not installed 21 Jan 2016.
# xray_eye2 = StandardProsilica('XF:11IDA-BI{?????}', name='xray_eye2')
xray_eye3 = StandardProsilica('XF:11IDB-BI{Cam:08}', name='xray_eye3')
fs1 = StandardProsilica('XF:11IDA-BI{FS:1-Cam:1}', name='fs1')
fs2 = StandardProsilica('XF:11IDA-BI{FS:2-Cam:1}', name='fs2')
fs_wbs = StandardProsilica('XF:11IDA-BI{BS:WB-Cam:1}', name='fs_wbs')
dcm_cam = StandardProsilica('XF:11IDA-BI{Mono:DCM-Cam:1}', name='dcm_cam')
fs_pbs = StandardProsilica('XF:11IDA-BI{BS:PB-Cam:1}', name='fs_pbs')
# elm = Elm('XF:11IDA-BI{AH401B}AH401B:')

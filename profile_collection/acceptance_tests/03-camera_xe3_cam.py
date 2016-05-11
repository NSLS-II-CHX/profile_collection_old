
from bluesky.plans import DeltaScanPlan
from bluesky.callbacks import LiveTable, LivePlot


subs = [LiveTable(['diff_xh', 'xray_eye3_stats1_total', 'xray_eye3_stats2_total']), 
        LivePlot('xray_eye3_stats1_total', 'diff_xh')]
print ( 'Motor is diff.xh, camera is xray_eye3 with saving images')
RE(DeltaScanPlan([xray_eye3_writing], diff.xh, -.1, .1, 3), subs)

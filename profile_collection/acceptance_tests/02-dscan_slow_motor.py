
from bluesky.plans import DeltaScanPlan
from bluesky.callbacks import LiveTable, LivePlot


#dscan diff.yh


subs = [LiveTable(['diff_yh', 'xray_eye3_stats1_total', 'xray_eye3_stats2_total']), 
        LivePlot('xray_eye3_stats1_total', 'diff_yh')]
print ('A DeltaScan of diff_yh with xray_eye3 as camera')
RE(DeltaScanPlan([xray_eye3], diff.yh, -.1, .1, 3), subs)


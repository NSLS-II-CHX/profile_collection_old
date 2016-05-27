
from bluesky.plans import DeltaScanPlan
from bluesky.callbacks import LiveTable, LivePlot


subs = [LiveTable(['gsl_xc', 'xray_eye3_stats1_total', 'xray_eye3_stats1_total']), 
        LivePlot('xray_eye3_stats1_total', 'gsl_xc')]
print(gsl.xc.read())
RE(DeltaScanPlan([xray_eye3], gsl.xc, -.1, .1, 3), subs)
print(gsl.xc.read())

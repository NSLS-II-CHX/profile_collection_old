
from bluesky.plans import DeltaScanPlan
from bluesky.callbacks import LiveTable, LivePlot


subs = [LiveTable(['diff_xh', 'xray_eye1_stats1_total', 'xray_eye1_stats2_total']), 
        LivePlot('xray_eye1_stats1_total', 'diff_xh')]
RE(DeltaScanPlan([xray_eye1], diff.xh, -.1, .1, 3), subs)

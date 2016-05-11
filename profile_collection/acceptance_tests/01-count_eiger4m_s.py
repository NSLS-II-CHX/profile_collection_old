from bluesky.plans import Count
from bluesky.callbacks import LiveTable, LivePlot



for aq_t, aq_p in zip([1, 1], [1, 2]):
    eiger4m_single.cam.acquire_time.value = aq_t
    eiger4m_single.cam.acquire_period.value = aq_p
    eiger4m_single.cam.num_images.value = 10 
    print("describe what to see")
    RE(Count([eiger4m_single]), 
       LiveTable(['eiger4m_single_stats1_total', 'eiger4m_single_stats2_total']))

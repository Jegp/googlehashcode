from collections import defaultdict
import numpy as np
data_center_capacity = 9999999999999999999999999

caches = {"dc": (data_center_capacity, [])}
endpoints = {"e0": [(10, "v0")]}
videos = {"v0": 100}
latency = {("e0", "dc"): 1000}

def requestFactor(number_requests, latency):
    return number_requests * latency

def requestRatio(global_factor, local_factor):
    return global_factor / local_factor

for c_id, (c_capacity, c_videos) in caches.items():
    video_ratios = defaultdict(list)
    for e_id, requests in endpoints.items():
        for (number_requests, v_id) in requests:
            if (e_id, c_id) in latency:
                local_factor = requestFactor(number_requests, latency[(e_id, c_id)])
                global_factor = requestFactor(number_requests, latency[(e_id, "dc")])
                ratio = requestRatio(global_factor, local_factor)
                video_ratios[v_id].append(ratio)

    video_mean_ratio = {}
    for v_id, ratios in video_ratios.items():
        video_mean_ratio[v_id] = np.array(ratios).mean()
    # Include score for video size

    print(video_mean_ratio)
    remaining_capacity = c_capacity
    for v_id in sorted(video_mean_ratio, key=video_mean_ratio.get, reverse=True):
        if remaining_capacity >= videos[v_id]:
            c_videos.append(v_id)
            remaining_capacity -= videos[v_id]
    

print(len(caches) - 1)
for c_id, (c_capacity, c_videos) in caches.items():
    if c_id != "dc":
        print(c_id[1:], " ".join(list(map(lambda v_id: v_id[1:], c_videos))))


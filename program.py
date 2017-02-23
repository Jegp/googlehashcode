from collections import defaultdict
import numpy as np
import sys

data_center_capacity = 9999999999999999999999999

caches = {}
endpoints = {}
videos = {}
latency = {}

fname = sys.argv[1]

with open(fname) as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 

settings = content[0].split()

for i in range(int(settings[0])):
    index = "v" + str(i)
    videos[index] = -1

for i in range(int(settings[1])):
    endpoints["e" + str(i)] = []

for i in range(int(settings[3])):
    caches["c" + str(i)] = (int(settings[4]),[])
    
caches["dc"] = (data_center_capacity, [])

# videos
video_sizes = [int(x) for x in content[1].split()]

for i, s in enumerate(video_sizes):
    videos['v' + str(i)] = s

#endpoints
line = content[2].split()
i = 2
n_s = 0
e_id = -1
while(len(line) == 2):
    if(n_s == 0):
        e_id += 1
        n_s = int(line[1])
        latency[("e" + str(e_id), "dc")] = int(line[0])
    else:
        n_s -= 1
        latency[("e" + str(e_id), "c" + str(line[0]))] = int(line[1])
    i += 1
    line = content[i].split()

#requests
for index in range(i, len(content)):
    line = content[index].split()
    endpoints["e" + str(line[1])].append((int(line[2]), "v" + str(line[0])))

def requestFactor(number_requests, latency):
    return number_requests * latency

def requestRatio(global_factor, local_factor):
    return global_factor / local_factor

for c_id, (c_capacity, c_videos) in caches.items():
    video_ratios = defaultdict(list)
    for e_id, requests in endpoints.items():
        if (e_id, c_id) in latency:
            for (number_requests, v_id) in requests:
                local_factor = requestFactor(number_requests, latency[(e_id, c_id)])
                global_factor = requestFactor(number_requests, latency[(e_id, "dc")])
                ratio = requestRatio(global_factor, local_factor)
                video_ratios[v_id].append(ratio)

    video_mean_ratio = {}
    for v_id, ratios in video_ratios.items():
        video_mean_ratio[v_id] = np.array(ratios).mean()
    # Include score for video size

    remaining_capacity = c_capacity
    for v_id in sorted(video_mean_ratio, key=video_mean_ratio.get, reverse=True):
        if remaining_capacity >= videos[v_id]:
            c_videos.append(v_id)
            remaining_capacity -= videos[v_id]
    

print(len(caches) - 1)
for c_id, (c_capacity, c_videos) in caches.items():
    if c_id != "dc":
        print(c_id[1:], " ".join(list(map(lambda v_id: v_id[1:], c_videos))))


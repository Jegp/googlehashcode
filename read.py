import numpy as np

data_center_capacity = 9999999999999999999999999

caches = {}
endpoints = {}
videos = {}
latency = {}

fname = 'me_at_the_zoo.in'

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
        latency[("e" + str(e_id), "dc")] = line[0]
    else:
        n_s -= 1
        latency[("e" + str(e_id), "c" + str(line[0]))] = int(line[1])
    i += 1
    line = content[i].split()

#requests
for index in range(i, len(content)):
    line = content[index].split()
    endpoints["e" + str(line[1])].append((int(line[2]), "v" + str(line[0])))
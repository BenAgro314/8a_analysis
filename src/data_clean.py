#!/usr/bin/env python3
import json
import pprint

data = json.load(open('../data/8a_data.json'))

count = 0

for area, value in data.items():
    #print(area,value.keys())
    #pprint.pprint(value['crags'])
    #print(type(value['crags']))
    for crag in value['crags']:
        #pprint.pprint(value['crags'][crag])
        climbs = value['crags'][crag]['climbs']
        if (climbs):
            for climb in climbs:
                print(climb)
                count += 1
            #print(climb)
        #print(crag)
        #for climb in crag:

print(count)

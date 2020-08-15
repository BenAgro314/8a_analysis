#!/usr/bin/env python3
import json
import pprint
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.corpus import wordnet


class Grade:

    def __init__(self, number = None, letter = None, modifier = None, project = False):
        self.number = number
        self.letter = letter
        self.modifier = modifier
        self.project = project 

    def __str__(self):
        if (self.project):
            return 'Project'
        else:
            res = str(self.number)
            if (self.letter):
                res += str(self.letter)
            if (self.modifier):
                res += str(self.modifier)
            return res

    # TODO: fix 
    def __cmp__(self, other):
        if (self.project and other.project) or (self.number == other.number and self.letter == other.letter and self.modifier == other.modifier):
            return 0
        if (self.project):
            return 1
        if (int(self.number) > int(other.number)):
            return 1
        elif (int(self.number) < int(other.number)):
            return -1

data = json.load(open('../data/2020-08-14_8a_data.json'))

crag_count = 0
area_count = 0
climb_count = 0


grades = []
grade_set = set()
freqs = {}
all_words = []

for area, value in data.items():
    area_count += 1
    #print(area)
    for crag,info in value['crags'].items():
        crag_count += 1
        #print(crag)
        if (info['climbs']):
            for climb,stats in info['climbs'].items():
                climb_count += 1
                print(stats['grade'],climb)
                climb = climb.lower()
                climb = climb.strip()
                climb = climb.split(' ')
                for w in climb:
                    all_words.append(w)
                    if (w in freqs):
                        freqs[w] += 1
                    else:
                        freqs[w] = 1
                '''
                print(stats['grade'],climb)
                grade = stats['grade']
                if (grade):
                    grade = grade.lower()
                    grade_set.add(grade)
                '''
                        

#word_list = list(freqs.items())
#word_list.sort(key = lambda x: x[1], reverse = False)
#pprint.pprint(word_list)
print("# of areas:",area_count)
print("# of crags:",crag_count)
print("# of climbs:",climb_count)
#print("# of unique words:",len(word_list))

all_words = nltk.FreqDist(all_words)
print(all_words.most_common(15))

'''
count = 100

x = []
heights = []

for i in range(count):
    if (i >= len(word_list)):
        break
    el = word_list[i]
    x.append(el[0])
    heights.append(el[1])


plt.bar(x, heights)
plt.show()
'''

import os
from random import random
from bisect import bisect

def parseFile(filename):
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in f]
        return lines

def filter(line):
    prefixes = ['%']
    for prefix in prefixes:
        if len(line) == 0 or line.startswith(prefix):
            return False
    return True

rootdir = 'training_data/bach_harpsichord_abc'
file_ = open('training_data/musicData.txt', 'w')
# Read each .abc file and write then into one big text file 
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        fname = os.path.join(subdir, file)
        lines = parseFile(fname)    
        for line in lines:
            if filter(line):
                file_.write(line+'\n')
        file_.write('\n\n\n') 
file_.close()






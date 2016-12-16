import os
from random import random
from bisect import bisect
import sys

def parseFile(filename):
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in f]
        return lines

def isStartHeader(line):
    if line.startswith('X'):
        return True
    return False

def isHeader(line):
    prefixes = ['X','T','M','L','Q','K','V']
    for prefix in prefixes:
        if line.startswith(prefix):
            return True
    return False

def filter(line):
    return (not len(line) == 0) and \
           (not line.startswith('%')) and \
           (not line.startswith('Error')) \

file_interleave = parseFile('song.txt')
file_uninterleave = open('uninterleave.txt', 'w')

melody = []
harmony = []
for line in file_interleave:
    if isHeader(line):
        file_uninterleave.write(line+'\n')
    else:
        line = line.split('|')
        isMel = True
        for bar in line:
            if isMel:
                melody.append(bar)
            else:
                harmony.append(bar)
            isMel = not isMel

melody = '|'.join(melody)
file_uninterleave.write(melody+'\n')
file_uninterleave.write('V:2\n')
harmony = '|'.join(harmony)
file_uninterleave.write(harmony+'\n')
 
file_uninterleave.close()
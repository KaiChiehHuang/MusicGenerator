import os
from random import random
from bisect import bisect
import sys

def parseFile(filename):
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in f]
        return lines

def isHeader(line):
    prefixes = ['X','T','M','L','Q','K']
    for prefix in prefixes:
        if line.startswith(prefix):
            return True
    return False

def filter(line):
    return (not len(line) == 0) and \
           (not line.startswith('%')) and \
           (not line.startswith('Error')) \


melody_lines = parseFile('melodyData.txt')
harmony_lines = parseFile('chordData.txt')
for mel, harm in zip(melody_lines, harmony_lines):
    if isHeader(mel):
        print "1st chunk: "+ mel + " 2nd chunk: " + harm
    else:
        mel = mel.split('|')
        harm = harm.split('|')
        for m, h in zip(mel, harm):
             print "1st chunk: "+ m + " 2nd chunk: " + h
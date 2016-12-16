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

melody_lines = parseFile('melody.txt')
harmony_lines = parseFile('harmony.txt')
file_interleave = open('interleave.txt', 'w')

for mel, harm in zip(melody_lines, harmony_lines):
    if isHeader(mel):
        file_interleave.write(mel+'\n')
    else:
        mel = mel.split('|')
        harm = harm.split('|')
        for idx, (m, h) in enumerate(zip(mel, harm)):
            if idx == len(mel) -1:
                file_interleave.write(m+'|'+h+'\n')
            else:
                file_interleave.write(m+'|'+h+'|')
file_interleave.close()
import os
from random import random
from bisect import bisect
import sys

MELODY = 1 # flag
CHORD = 2  # flag

def parseFile(filename):
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in f]
        return lines

def isStartHeader(line):
    if line.startswith('X'):
        return True
    return False

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

file_melody = open('melody.txt', 'w')
file_chord = open('harmony.txt', 'w')
# Read in the input text file that already has a lot of
# songs with modely and chord (melody denotes V:1, chord denotes V:2).
# This function breaks the input text file into melody.txt and
# chord.txt for training two RNN models separately
flag = CHORD

lines = parseFile('input.txt')
for line in lines:
    if line.startswith('V') and flag == CHORD:
        flag = MELODY
    elif line.startswith('V') and flag == MELODY:
        flag = CHORD
    if filter(line):
        if isStartHeader(line):
            file_melody.write('MELODY\n')
            file_chord.write('HARMONY\n') 

        if isHeader(line):
            file_melody.write(line+'\n')
            file_chord.write(line+'\n') 
        elif flag == MELODY:
            file_melody.write(line+'\n')
        elif flag == CHORD:
            file_chord.write(line+'\n')
file_melody.close()
file_chord.close()
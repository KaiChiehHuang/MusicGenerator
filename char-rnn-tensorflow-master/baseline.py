import os
from random import random
from bisect import bisect

def parseFile(filename):
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in f]
        return lines

def filter(line):
    prefixes = ['%', 'X:', 'T:', 'M:', 'L:', 'Q:', 'C:', 'K:', 'P:', 'w:', 'S:', 'N:', 'H:', 'O:']
    for prefix in prefixes:
        if len(line) == 0 or line.startswith(prefix):
            return False
    return True

def populateVector(lines, prefix, vector):
    def header_filter (line, prefix):
        if line.startswith(prefix):
            return True
        return False

    header_lines = [line for line in lines if header_filter(line, prefix)]
    for line in header_lines:
        vector[line] = vector[line] + 1 if line in vector else 1

def weightedVector(line):
    line = line.replace('\\', '')
    line = countUpdate(line, ':||')
    line = countUpdate(line, '||:')
    line = countUpdate(line, '||')
    line = countUpdate(line, '|:')
    line = countUpdate(line, ':|')
    line = countUpdate(line, '|')
    tokens = line.split(' ')
    for token in tokens:
        if token == '':
            continue
        vector[token] = vector[token] + 1 if token in vector else 1
    return line

def countUpdate(line, substr):
    count = line.count(substr)
    if count > 0:
        vector[substr] = count
    line = line.replace(substr, '')
    return line

def total_weights_values(vector):
    total = 0
    cum_weights = []
    values = []
    for key, value in vector.iteritems():
        values.append(key)
        total += value
        cum_weights.append(total)
    return (total, cum_weights, values)

def weighted_choice(vector):
    total, cum_weights, values = total_weights_values(vector)
    return weighted_choice2(total, cum_weights, values)

def weighted_choice2(total, cum_weights, values):
    x = random() * total
    i = bisect(cum_weights, x)
    return values[i]    

time_vector = {}
key_vector = {}
vector = {}
rootdir = 'training_data/bach_harpsichord_abc'
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        fname = os.path.join(subdir, file)
        lines = parseFile(fname)
        populateVector(lines, 'M:', time_vector)
        populateVector(lines, 'K:', key_vector)
        lines = [weightedVector(line) for line in lines if filter(line)]

total, cum_weights, values = total_weights_values(vector)

for n in range(20):
    notes = []
    for i in range(100):
        notes.append(weighted_choice2(total, cum_weights, values))

    file_ = open('output_data/weighted_vector/'+str(n)+'.abc', 'w')
    file_.write('H:This file contains some example \n')
    file_.write('X:1 \n')
    file_.write('T: Baseline Implementation \n')
    file_.write('T: Weighted Vector \n')
    file_.write('C: Quin, Jen & Jay \n')
    file_.write(weighted_choice(time_vector) + '\n')
    file_.write(weighted_choice(key_vector) + '\n')
    file_.write(' '.join(notes))
    file_.close()







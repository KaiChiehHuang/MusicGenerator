import os
rootdirs = ['./training_data/bach_harpsichord_abc', './training_data/han_scar_viv_abc']

file_input = open('input.txt', 'w')
mashed_line = ""

def isHeader(line):
    prefixes = ['X','T','M','L','Q','K','%']
    for prefix in prefixes:
        if line.startswith(prefix):
            return True
    return False

for rootdir in rootdirs:
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            with open(os.path.join(subdir, file)) as f:
                for line in f:
                    if line.startswith('V'):
                        if len(mashed_line) != 0:
                            file_input.write(mashed_line+'\n')
                        mashed_line = ""
                        file_input.write(line)
                    elif isHeader(line):
                        if len(mashed_line) != 0:
                            file_input.write(mashed_line+'\n')
                        mashed_line = ""
                        file_input.write(line)
                    else:
                        mashed_line += line.rstrip()

file_input.close()
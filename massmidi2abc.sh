#!/bin/bash
_dfiles="/home/ubuntu/MusicGeneratorQuin/training_data/bach_new/*"
 
for f in $_dfiles
do
         b=$(basename $f)
         ../abcmidi/midi2abc.exe $f > ./output/"${b%.*}.abc"
done
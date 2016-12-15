#!/bin/bash
_dfiles="/home/ubuntu/MusicGeneratorQuin/training_data/vivaldi/*"
 
for f in $_dfiles
do
         b=$(basename $f)
         ../abcmidi/midi2abc.exe $f > ./output/"${b%.*}.abc"
done
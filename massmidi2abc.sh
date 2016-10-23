#!/bin/bash
_dfiles="/afs/.ir/users/q/u/quinlanj/cs221/project/training_data/*"
 
for f in $_dfiles
do
         b=$(basename $f)
         ../abcmidi/midi2abc.exe $f > ./training_abc/"${b%.*}.abc"
done
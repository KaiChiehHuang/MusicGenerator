#!/bin/bash
_dfiles="/afs/.ir/users/q/u/quinlanj/cs221/project/output_abc/*"
 
for f in $_dfiles
do
         b=$(basename $f)
         ../abcmidi/abc2midi.exe $f -o ./output_midi/"${b%.*}.mid"
done
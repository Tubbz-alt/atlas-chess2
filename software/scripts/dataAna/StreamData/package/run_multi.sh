#!/bin/sh

for i in /u1/atlas-chess2-Asic-tests/data/data_h/StreamReadout/DaughterBoard_01/StreamRO_externalTrigger_Run10_201812*.txt
do 
    ./StreamToRoot $i
done

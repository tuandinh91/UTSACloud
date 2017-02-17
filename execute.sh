#!/bin/bash 
echo using scale 3
python assign1.py -benchmark=hpcc -sched=byslot>out.txt
python assign1.py -benchmark=hpcc -sched=bynode>>out.txt
#!/bin/bash
# bash script for creating a set of virtual machines using vcsim, create_vm.py / pyc.
# run: `$ bash make_vms.sh -n 
# This can be adapated to 
### TODO: add [create_vm.py[c] [-s <HOST> -o <PORT> -u <USER> -p <PASS> -d <DATACENTER> -c <CLUSTER>]]`

VCS_PID=`pgrep vcsim`

if [ "$#" -eq 0 ];
then 	NUM_VMS=100
	PY_STRING="create_vm.pyc"
elif [ "$#" -eq 1 ];
then	NUM_VMS="$1"
	PY_STRING="create_vm.pyc"
elif [ "$#" -eq 2 ];
then 	NUM_VMS="$1"
	PY_STRING="$2"
fi

i=1
while [ "$i" -le "$NUM_VMS" ];
do
	python "$PY_STRING" -s 127.0.0.1 -o 8989 -u user -p pass -d DC0 -c C0 -v vm_$i;
	ps u $VCS_PID | tail -1 | awk '{print $3,$4,$5,$6,$10}' >> .out.txt;
	i=$(($i + 1))
done



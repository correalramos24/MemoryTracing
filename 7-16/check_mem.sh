#!/bin/bash

jobid=$1

sentence="$(squeue -j $jobid)"            # read job's slurm status
stringarray=($sentence)
jobstatus=(${stringarray[12]})


until [ "$jobstatus" = "R" ]
do
  sleep 5s
  sentence="$(squeue -j $jobid)"            # read job's slurm status
  stringarray=($sentence)
  jobstatus=(${stringarray[12]})
done
NODES=$(sacct --noheader -X -P -oNodeList --jobs=$jobid)
NODES=$(echo $NODES | cut -d "[" -f2 | cut -d "]" -f1)
NODES=$(echo $NODES | perl -pe 's/(\d+)-(\d+)/join(",",$1..$2)/eg')
IFS=', ' read -r -a nodes <<< "$NODES"
for node in "${nodes[@]}"
do
  file=$node"_mem.txt"
  node2="nid["$node"]"
  (srun --overlap --jobid=$jobid -w $node2 free -s 1 &) &> $file
done


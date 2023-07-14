#!/bin/bash
SAMPLING_TIME=2
MEM_FILE="$HOSTNAME-mem.log"

echo "Enable mem tracing with sampling every $SAMPLING_TIME"

free -s $SAMPLING_TIME &> $MEM_FILE &
PID_FREE=$!

#Run your program:
sleep 10

#Stop memory tracing
echo "Stop memory tracing. Results @ $MEM_FILE (units in KiB)"
kill $PID_FREE

echo "All done"

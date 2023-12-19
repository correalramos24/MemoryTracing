#!/bin/bash


if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <folder path (absolute path)> <sampling time>"
    exit 1
fi

INPUT_DIR=$1
SAMP=$2

if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: First argument must be an absolut path."
    echo "Unable to find $INPUT_DIR"
    exit 1
fi

if ! [[ "$SAMP" =~ ^[0-9]+$ ]]; then
    echo "Error: Second argument must be the sampling frequency (integer value)"
    echo "got $SAMP"
    exit 1
fi

# Execute in a container, deleted after the run
# the output will be placed on the same directory as the input
# WARNING! INPUT_DIR must be an absolute path

docker run -it --rm -v ${INPUT_DIR}:/home/mnt_point memory_tracing:latest --folder /home/mnt_point -s $SAMP --save /home/mnt_point/plot.png

echo "Output placed at $INPUT_DIR/plot.png"
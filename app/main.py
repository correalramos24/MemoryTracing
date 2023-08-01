#!/bin/python3

import argparse
from ProfileMemory import *

def main():
    # Arg parsing:
    parser = argparse.ArgumentParser(description="Memory tracing postprocessing")
    parser.add_argument('-f', required=True, help="Input files", nargs="+")
    parser.add_argument('-s', required=True, help='Sampling time')
    parser.add_argument('-u', required=False, default="KiB", help="Memory units")
    parser.add_argument('--save', required=False, default=None, help="Enable and define save file name")
    args = parser.parse_args()

    # Parse & plot:

    pf_mem = ProfileMemory.from_files(args.f, args.s, args.u)
    pf_mem.plotDataPLT(args.save)


if __name__ == "__main__":
    main()

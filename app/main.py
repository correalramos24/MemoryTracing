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
    parser.add_argument('--swap', required=False, action='store_true', help="Enable swap plotting")
    parser.add_argument('--total', required=False, action='store_true', help="Enable total memory available?")
    parser.add_argument('--percentatge', required=False, action='store_true', help="Plot % of usage")
    args = parser.parse_args()

    # Parse & plot:

    pf_mem = ProfileMemory.from_files(args.f, args.s, args.u)
    if not args.percentatge:
        pf_mem.plotDataPLT( save_name=args.save, plot_total=args.total, 
                            plot_swap=args.swap)
    else:
        pf_mem.plotPercentatgePLT(args.swap, args.save)

if __name__ == "__main__":
    main()

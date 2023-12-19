#!/bin/python3

import argparse
from ProfileMemory import *

def main():
    # Arg parsing:
    parser = argparse.ArgumentParser(description="Memory tracing postprocessing")
    parser.add_argument('-f', required=False, help="Input files", nargs="+")
    parser.add_argument('--folder', required=False, help="Input folder")
    parser.add_argument('-s', required=True, help='Sampling time')
    parser.add_argument('-u', required=False, default="KiB", help="Memory units")
    parser.add_argument('--save', required=False, default=None, help="Enable and define save file name")
    parser.add_argument('--swap', required=False, action='store_true', help="Enable swap plotting")
    parser.add_argument('--total', required=False, action='store_true', help="Enable total memory available?")
    parser.add_argument('--percentatge', required=False, action='store_true', help="Plot % of usage")
    args = parser.parse_args()

    # Parse & plot:
    files : list[str] = args.f
    folder : str = args.folder
    sampl  : int = args.s
    save   : str = args.save
    swap   : bool = args.swap
    total  : bool = args.total
    percnt : bool = args.percentatge

    if files is not None:
        pf_mem = ProfileMemory.from_files(files, sampl, args.u)
    elif folder is not None:
        print(f"Parsing directory {folder}!")
        pf_mem = ProfileMemory.from_folder(folder, sampl, args.u)
    else:
        print("You must either provide files or a folder (-f or --folder)")
        exit(1)

    if not percnt:
        print("Plotting data with units")
        pf_mem.plotDataPLT( save_name=save, plot_total=total, 
                            plot_swap=swap)
    else:
        print("Plotting data with %")
        pf_mem.plotPercentatgePLT(swap, save)

if __name__ == "__main__":
    main()

#!/bin/python3

import argparse
import matplotlib.pyplot as plt
import numpy as np
from definitions import *

def parseFile(fName="mem.log", sampTime=2) -> MemoryTrace:
    ret = MemoryTrace(fName.split(".")[0])
    print(f"Parsing {fName} with sampling each {sampTime} seconds...", end='')

    extractDataFromFreeLine = lambda l : l.strip().split()[1:4]

    with open(fName, mode='r') as memFile:
        for l in memFile.readlines():
            if "total" in l: continue
            if "Mem:" in l: 
                aux = MemoryRecord._make(extractDataFromFreeLine(l))
                ret.addMainMemRecord(aux)    
            if "Swap: " in l:
                aux = MemoryRecord._make(extractDataFromFreeLine(l))
                ret.addSwapMemRecord(aux)
    print(f" DONE! Found {ret.getRecords()}")
    return ret

def plotMemory(NodeMemRecords, saveName=None):
    if len(NodeMemRecords) == 0: 
        print("Empty data, can't generate any plot :(")
        return
    for k in NodeMemRecords:
        print(f"Plotting {k} data...", end='')

        total=list(NodeMemRecords[k].getTotal())
        used=list(NodeMemRecords[k].getUsed())
        timing=np.arange(0, NodeMemRecords[k].getTotalTime(), NodeMemRecords[k].sampling)

        plt.plot(timing, used, label="Used " + k)
        plt.plot(timing, total, label="Total "+k)
        print("Done!")

    plt.ylabel("Memory (MiB)")
    plt.xlabel("Time (s)")
    plt.title("Memory tracing")
    plt.legend()
    if saveName is not None:
        print(f"Saving plot to {saveName}")
        plt.savefig(saveName+".png")
    else: 
        plt.show()

def main():
    # Arg parsing:
    parser = argparse.ArgumentParser(description="Memory tracing postprocessing")
    parser.add_argument('-f',  required=True, help="Input files", nargs="+")
    parser.add_argument('-s', required=True, help='Sampling time')
    parser.add_argument('--save', required=False, default=None, help="Enable and define save file name")
    args= parser.parse_args()

    # Parse & plot:
    resultsPerHost=dict()
    for file in args.f:
        try:
            info = parseFile(file, 2)
            if info.host in resultsPerHost:
                print("WARNING! Same node name in the log files detected!")
                print("This file will not be plotted!")
            else: resultsPerHost[info.host] = info
        except:
            print(f"Can't parse {file} file, next one")

    plotMemory(resultsPerHost, args.save)

if __name__ == "__main__":
    main()
#!/bin/python3

import argparse
import matplotlib.pyplot as plt
import numpy as np
from definitions import *


def parseFile(file_name="mem.log", sampling_time=2) -> MemoryTrace:
    ret = MemoryTrace(file_name.split(".")[0])
    print(f"Parsing {file_name} with sampling each {sampling_time} seconds...", end='')

    with open(file_name, mode='r') as memFile:
        for line in memFile.readlines():
            if "total" in line:
                continue
            if "Mem:" in line:
                aux = MemoryRecord._make(line.strip().split()[1:4])
                ret.addMainMemRecord(aux)
            if "Swap: " in line:
                aux = MemoryRecord._make(line.strip().split()[1:4])
                ret.addSwapMemRecord(aux)
    print(f" DONE! Found {ret.getRecords()}")
    return ret


def plotMemory(NodeMemRecords, save_name=None):
    if len(NodeMemRecords) == 0:
        print("Empty data, can't generate any plot :(")
        return
    for k in NodeMemRecords:
        print(f"Plotting {k} data...", end='')

        total = list(NodeMemRecords[k].getTotal())
        used = list(NodeMemRecords[k].getUsed())
        timing = np.arange(0, NodeMemRecords[k].getTotalTime(), NodeMemRecords[k].sampling)

        plt.plot(timing, used, label="Used " + k)
        plt.plot(timing, total, label="Total " + k)
        print("Done!")

    plt.ylabel("Memory (MiB)")
    plt.xlabel("Time (s)")
    plt.title("Memory tracing")
    plt.legend()
    if save_name is not None:
        print(f"Saving plot to {save_name}")
        plt.savefig(save_name + ".png")
    else:
        plt.show()


def main():
    # Arg parsing:
    parser = argparse.ArgumentParser(description="Memory tracing postprocessing")
    parser.add_argument('-f', required=True, help="Input files", nargs="+")
    parser.add_argument('-s', required=True, help='Sampling time')
    parser.add_argument('--save', required=False, default=None, help="Enable and define save file name")
    args = parser.parse_args()

    # Parse & plot:
    results_per_host = dict()
    for file in args.f:
        try:
            info = parseFile(file, 2)
            if info.host in results_per_host:
                print("WARNING! Same node name in the log files detected!")
                print("This file will not be plotted!")
            else:
                results_per_host[info.host] = info
        except:
            print(f"Can't parse {file} file, next one")

    plotMemory(results_per_host, args.save)


if __name__ == "__main__":
    main()

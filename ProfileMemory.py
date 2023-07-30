from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt

MemoryRecord = namedtuple("MemRecord", "total used free")

class MemoryTrace:

    def __init__(self, host, sampling_time=2, units="MiB") -> None:
        self.host = host
        self.sampling = sampling_time
        self.units = units
        self.main_meminfo = []
        self.swap_meminfo = []

    def addMainMemRecord(self, info):
        self.main_meminfo.append(info)

    def addSwapMemRecord(self, info):
        self.swap_meminfo.append(info)

    def getUsed(self, main_mem_or_swap_mem='mem'):
        if main_mem_or_swap_mem == 'mem':
            return map(lambda mem_record: float(mem_record.used), self.main_meminfo)
        elif main_mem_or_swap_mem == 'swap':
            return map(lambda mem_record: float(mem_record.used), self.swap_meminfo)
        else:
            raise Exception("Invalid argument getUsed!")

    def getTotal(self, main_mem_or_swap_mem='mem'):
        if main_mem_or_swap_mem == 'mem':
            return map(lambda mem_record: float(mem_record.total), self.main_meminfo)
        elif main_mem_or_swap_mem == 'swap':
            return map(lambda mem_record: float(mem_record.total), self.swap_meminfo)
        else:
            raise Exception("Invalid argument getUsed!")

    def getRecords(self):
        return len(self.main_meminfo)

    def getTotalTime(self):
        return self.getRecords() * self.sampling

    def getSampling(self):
        return self.sampling

class ProfileMemory:

    def __init__(self, memData=None) -> None:
        if memData is None:
            self.data_per_host = {}
        else:
            self.data_per_host = memData

    def plotDataPLT(self, save_name) -> None:
        if len(self.data_per_host) == 0:
            print("Empty data, can't generate any plot :(")
        for k in self.data_per_host.values():
            host = k.host
            print(f"Plotting {host} data...", end='')
            total = list(k.getTotal())
            used = list(k.getUsed())
            timing = np.arange(0, k.getTotalTime(), k.getSampling())

            plt.plot(timing, used, label="Used " + host)
            plt.plot(timing, total, label="Total " + host)
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

    @staticmethod
    def __parsefile__(file_name, sampling_time) -> MemoryTrace:
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

    @classmethod
    def from_files(cls, file_names, sampling_time): 
        aux_info=dict()
        for file in file_names:
            try:
                info = cls.__parsefile__(file, sampling_time)
                if info.host in aux_info:
                    print("WARNING! Same node name in the log files detected!")
                    print("This file will not be plotted!")
                else:
                    aux_info[info.host] = info
            except:
                print(f"Can't parse {file} file, skipping")
        return ProfileMemory(aux_info)
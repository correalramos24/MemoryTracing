from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt




class ProfileMemory:

    MemRecord = namedtuple("MemRecord", "total used free")
    MemTrace = namedtuple("MemTrace", "host main_mem_info swap_meminfo", defaults=([], []))

    def __init__(self, memData: dict[MemTrace] = None, sampling_time: int = None, units: str = None) -> None:
        self.sampling_time = int(sampling_time)
        self.units = units
        if memData is None:
            self.data_per_host = {}
        else:
            self.data_per_host = memData

    def plotDataPLT(self, plot_swap: bool = False, save_name: str = None) -> None:
        if len(self.data_per_host) == 0:
            print("Empty data, can't generate any plot :(")

        for k in self.data_per_host.values():
            host = k.host
            print(f"Plotting {host} data...", end='')

            main_mem_total = list(map(lambda x: float(x.used), k.main_mem_info))
            main_mem_used = list(map(lambda x: float(x.total), k.main_mem_info))

            timing = np.arange(0, self.getSamplingTime() * len(main_mem_used), self.getSamplingTime())

            plt.plot(timing, main_mem_used, label="Used " + host)
            plt.plot(timing, main_mem_total, label="Total " + host)

            if plot_swap:
                raise Exception("Not implemented yet!")

            print("Done!")

        plt.ylabel(f"Memory {self.units}")
        plt.xlabel("Time (s)")
        plt.title("Memory tracing")
        plt.legend()

        if save_name is not None:
            print(f"Saving plot to {save_name}")
            plt.savefig(save_name + ".png")
        else:
            plt.show()

    def getSamplingTime(self):
        return self.sampling_time

    @staticmethod
    def __parsefile__(file_name) -> MemTrace:
        hostName = file_name.split("-mem.log")[0]
        ret = MemTrace(hostName, [], [])
        print(f"Parsing {file_name} ({hostName})", end='')

        with open(file_name, mode='r') as memFile:
            for line in memFile.readlines():
                if "total" in line:
                    continue
                if "Mem:" in line:
                    aux = MemRecord._make(line.strip().split()[1:4])
                    ret.main_mem_info.append(aux)
                if "Swap: " in line:
                    aux = MemRecord._make(line.strip().split()[1:4])
                    ret.swap_meminfo.append(aux)

        if len(ret.main_mem_info) != len(ret.swap_meminfo):
            raise Exception("File corrupted, different swap and mem information")
        else:
            print(f" DONE! Found {len(ret.main_mem_info)} records")

        return ret

    @classmethod
    def from_files(cls, file_names, sampling_time, units="KiB"):
        aux_info = dict()
        for file in file_names:
            try:
                info = cls.__parsefile__(file)
                if info.host in aux_info:
                    print(f"WARNING! Same node name in the log files detected! ({info.host})")
                    print("This file will not be plotted!")
                else:
                    aux_info[info.host] = info
            except Exception:
                print(f"Can't parse {file} file, skipping")
        return ProfileMemory(aux_info, sampling_time, units)

    @classmethod
    def from_tracing_file(cls, file_name, sampling_time):
        pass

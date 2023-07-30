from collections import namedtuple

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

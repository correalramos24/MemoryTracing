
from collections import namedtuple
from typing import List
MemoryRecord = namedtuple("MemRecord", "total used free")

class MemoryTrace:

    def __init__(self, host, samplingTime=2, units="MiB") -> None:
        self.host=host
        self.sampling=samplingTime
        self.units=units
        self.mainmeminfo=[]
        self.swapmeminfo=[]

    def addMainMemRecord(self, info):
        self.mainmeminfo.append(info)

    def addSwapMemRecord(self, info):
        self.swapmeminfo.append(info)

    def getUsed(self, MainMemOrSwap='mem'):
        aux= lambda memrecord : float(memrecord.used)
        if MainMemOrSwap == 'mem':
            return map(aux, self.mainmeminfo)
        elif MainMemOrSwap == 'swap':
            return map(aux, self.swapmeminfo)
        else:
            raise Exception("Invalid argumentin getUsed!")
    
    def getTotal(self, MainMemOrSwap='mem'):
        aux= lambda memrecord : float(memrecord.total)
        if MainMemOrSwap == 'mem':
            return map(aux, self.mainmeminfo)
        elif MainMemOrSwap == 'swap':
            return map(aux, self.swapmeminfo)
        else:
            raise Exception("Invalid argumentin getUsed!")

    def getRecords(self):
        return len(self.mainmeminfo)

    def getTotalTime(self):
        return self.getRecords()*self.sampling

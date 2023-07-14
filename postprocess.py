

def parseFile(fName="mem.log"):
    #triplets of (total, used, free)
    mem = [] 
    swap = []
    with open(fName, mode='r') as memFile:
        for l in memFile.readlines():
            #Is a 
            if "total" in l:
                continue
            if "Mem:" in l:
                total, used, free =l.strip().split()[1:4]
                #print(f"Found mem record with {total}, {used}, {free} (MiB)")
                mem.append((total, used, free))
            if "Swap: " in l:
                total, used, free =l.strip().split()[1:4]
                #print(f"Found swap record with {total}, {used}, {free} (MiB)")
                swap.append((total, used, free))
    print(f"Found {len(mem)} memory records")
    return mem, swap

def plot(memRecords=[], samplingTime=2):
    import matplotlib.pyplot as plt
    
    total =list(map(lambda x: float(x[0]), memRecords)) 
    used = list(map(lambda x: float(x[1]), memRecords))
    #free =
    timing=list([2*x for x in list(range(len(memRecords)))])

    plt.plot(timing, used, 'r', label="Memory usage")
    plt.plot(timing, total, 'b--', label="Available memory" )
    plt.ylabel("Memory (MiB)")
    plt.xlabel("Time (s)")
    plt.legend()

    plt.show()

def main():
    mem, swap = parseFile()
    plot(mem, swap)
    



if __name__ == "__main__":
    main()

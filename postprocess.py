import argparse
import glob
import matplotlib.pyplot as plt


def parseFile(fName="mem.log"):
    host=fName.split(".")[0]
    #triplets of (total, used, free)
    mem = [] 
    swap = []
    print(f"Parsing {fName} from host {host}...", end='')
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
    return host, mem, swap

def plot(memRecords=[], samplingTime=2):
    total =list(map(lambda x: float(x[0]), memRecords)) 
    used = list(map(lambda x: float(x[1]), memRecords))
    timing=list([2*x for x in list(range(len(memRecords)))])

    plt.plot(timing, used, 'r', label="Memory usage")
    plt.plot(timing, total, 'b--', label="Available memory" )
    plt.ylabel("Memory (MiB)")
    plt.xlabel("Time (s)")
    plt.legend()

    plt.show()

def plotMultiNode(NodeMemRecords={}, samplingTime=2): 
    #Id inside each dict record:
    memId=0 
    swpId=1    

    for k in NodeMemRecords:
        total = list(map(lambda x : float(x[0]), NodeMemRecords[k][memId]))
        used  = list(map(lambda x : float(x[1]), NodeMemRecords[k][memId]))
        timing= list([2*x for x in list(range(len(total)))])
        plt.plot(timing, used, label=k)
        plt.plot(timing, total, label="total"+k)

    plt.ylabel("Memory (MiB)")
    plt.xlabel("Time (s)")
    plt.legend()
    plt.show()

def main():
    # Arg parser
    parser = argparse.ArgumentParser(description="Memory tracing postprocessing")
    #Add flag-type args:
    parser.add_argument('-f',   required=False, help="Input file")
    parser.add_argument('-mf',  required=False, help="Input files", nargs="*")
    args= parser.parse_args()
        
    if args.f is not None and args.mf is not None:
        print("Specify only one input. Exit")
        exit(2)

    if args.f is not None:
        mem, swap = parseFile()
        plot(mem, swap)
        exit(0)

    if args.mf is not None:
        results=dict()  #each node points to pair [mem], [swap]
        for file in args.mf:
            print(file)
            node, mem, swap = parseFile(file)
            if node in results:
                print("ERROR! Same node name in the log files detected!")
                exit(1) 
            results[node] = (mem,swap)
        plotMultiNode(results)
        exit(0)

    print("Specify one input. Exit")
    exit(2)


if __name__ == "__main__":
    main()

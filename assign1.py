import argparse
import os
import numpy as np

import matplotlib

matplotlib.use('Agg')

from matplotlib import pyplot as plt

#global arrays
OYPTRANS = []
OYHPL = []

def draw_chart(OY,file_name_modifier=""):

    #x-axis data
    OX = []
    OX.append(1)
    OX.append(2)
    OX.append(3)
    OX.append(4)

    fig = plt.figure()

    width = .35
    ind = np.arange(len(OY))
    plt.bar(ind, OY, width=width)
    plt.xticks(ind + width / 2, OX)

    #saves the chart as a pdf
    plt.savefig("figure-"+args.benchmark+"-"+file_name_modifier+"-"+args.sched+".pdf")
    
    print "Output graph is written on "+os.getcwd()+"/figure-"+args.benchmark+"-"+file_name_modifier+"-"+args.sched+".pdf"

def tachyon():
    print 'tachyon'
    print args.sched

    #changing directory to run tachyon
    os.chdir("tachyon/compile/linux-mpi/")
    
    #Y-axis data for the graph
    OY = []
    for cluster in range(1,5):    
        os.system("mpirun -np "+str(cluster*2)+" --hostfile ~/mpi_host"+str(cluster)+" -"+args.sched+" ./tachyon ../../scenes/teapot.dat>result.txt")
        
        print "\nCluster "+str(cluster)+": "
        file = open('result.txt','r')
        rtTime = file.read().split('Ray Tracing Time:     ',1)[1].split(' seconds',1)[0]
        print "Time required for ray tracing: "+rtTime
        OY.append(float(rtTime))
   
    draw_chart(OY)

#deletes the output file before running hpcc    
def delete_output_file():
    if os.path.exists("hpccoutf.txt"):
        os.remove("hpccoutf.txt")
        #print "previous output file deleted"

def change_input_parameter(P,Q,NB,N):
    with open('hpccinf.txt','r') as infile:
        content = infile.read().split('\n')
    
    content[10] = str(P)+'            Ps' 
    content[11] = str(Q)+'            Qs' 
    content[7] = str(NB)+'          NBs' 
    content[5] = str(N)+'        Ns' 

    with open('hpccinf.txt','w') as infile:
        for item in content:
            infile.write("%s\n" % item)


def calculate_hpl():
    with open('hpccoutf.txt','r') as infile:
        content = infile.read().split('\n')
        for item in content:
            if item.startswith('WR11C2R4'):
                return float(item.split()[-1])
                
def process_cluster(cluster, nb, n, scale):
    global OYPTRANS
    global OYHPL
    delete_output_file()
    change_input_parameter(1,cluster,nb,n/scale)

    os.system("mpirun -np "+str(cluster*2)+" --hostfile ~/mpi_host"+str(cluster)+" -"+args.sched+" ./hpcc")
    
    print "\nCluster "+str(cluster)+": "
    file = open('hpccoutf.txt','r')
    PTRANS_GBs =  file.read().split('PTRANS_GBs=',1)[1].split('\nPTRANS_time',1)[0]
    HPL_Gflops=calculate_hpl()
    print 'PTRANS_GBs: '+str(PTRANS_GBs)
    print 'HPL_Gflops: '+str(HPL_Gflops)
    OYPTRANS.append(float(PTRANS_GBs))  
    OYHPL.append(float(HPL_Gflops))                
                    
def hpcc():
    global OYPTRANS
    global OYHPL
    print 'hpcc'
    print args.sched
    os.chdir("hpcc-1.4.3/")
    #scale down the data to speedup testing
    scale = 3
    process_cluster(1, 224, 14560, scale); 
    process_cluster(2, 224, 20832, scale); 
    process_cluster(3, 224, 25536, scale); 
    process_cluster(4, 224, 29280, scale); 
    draw_chart(OYPTRANS,"PTRANS")
    draw_chart(OYPTRANS,"HPL")

#program starts here
    
parser = argparse.ArgumentParser()

parser.add_argument('-benchmark')

parser.add_argument('-sched')

args = parser.parse_args()


if args.sched != 'byslot' and args.sched != 'bynode':
    print args.sched
    print 'Scheduling policy is invalid. Should be byslot or bynode'
    quit();
if args.benchmark == 'tachyon':
    tachyon()
elif args.benchmark == 'hpcc':
    hpcc()
else:
    print 'Benchmark not supported'


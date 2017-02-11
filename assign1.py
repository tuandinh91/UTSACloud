import optparse
import os
import numpy as np

import matplotlib

matplotlib.use('Agg')

from matplotlib import pyplot as plt



def tachyon():
	print 'tachyon'
	print options.sched
	#print os.getcwd()
	os.chdir("tachyon/compile/linux-mpi/")
	#print os.getcwd()
	
	os.system("mpirun -np 1 --hostfile ~/mpi_hosts -"+options.sched+" ./tachyon ../../scenes/teapot.dat>result.txt")
	file = open('result.txt','r')
	rtTime1 = file.read().split('Ray Tracing Time:     ',1)[1].split(' seconds',1)[0]
	
	os.system("mpirun -np 2 --hostfile ~/mpi_hosts -"+options.sched+" ./tachyon ../../scenes/teapot.dat>result.txt")
	file = open('result.txt','r')
	rtTime2 =  file.read().split('Ray Tracing Time:     ',1)[1].split(' seconds',1)[0]
	
	os.system("mpirun -np 3 --hostfile ~/mpi_hosts -"+options.sched+" ./tachyon ../../scenes/teapot.dat>result.txt")
	file = open('result.txt','r')
	rtTime3 =  file.read().split('Ray Tracing Time:     ',1)[1].split(' seconds',1)[0]
	
	os.system("mpirun -np 4 --hostfile ~/mpi_hosts -"+options.sched+" ./tachyon ../../scenes/teapot.dat>result.txt")
	file = open('result.txt','r')
	rtTime4 =  file.read().split('Ray Tracing Time:     ',1)[1].split(' seconds',1)[0]
	
	print rtTime1;
	print rtTime2;
	print rtTime3;
	print rtTime4;
	
	OX = []
	OX.append(1)
	OX.append(2)
	OX.append(3)
	OX.append(4)
	
	OY = []
	OY.append(float(rtTime1))
	OY.append(float(rtTime2))
	OY.append(float(rtTime3))
	OY.append(float(rtTime4))
	
	fig = plt.figure()

	width = .35
	ind = np.arange(len(OY))
	plt.bar(ind, OY, width=width)
	plt.xticks(ind + width / 2, OX)

	fig.autofmt_xdate()

	plt.savefig("figure.pdf")

def hpcc():
	print 'hpcc'
	

parser = optparse.OptionParser()

parser.add_option('--benchmark',
    action="store", dest="benchmark",
    help="benchmark string", default="tachyon")
	
parser.add_option('--sched',
    action="store", dest="sched",
    help="scheduling policy", default="byslot")

options, args = parser.parse_args()

if options.benchmark == 'tachyon':
	tachyon()
elif options.benchmark == 'hpcc':
	hpcc()
else:
	print 'Benchmark not supported'


import optparse
import os
import numpy as np

import matplotlib

matplotlib.use('Agg')

from matplotlib import pyplot as plt

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
	plt.savefig("figure-"+options.benchmark+"-"+file_name_modifier+"-"+options.sched+".pdf")
	
	print "Output graph is written on "+os.getcwd()+"/figure-"+options.benchmark+"-"+file_name_modifier+"-"+options.sched+".pdf"

def tachyon():
	print 'tachyon'
	print options.sched

	#changing directory to run tachyon
	os.chdir("tachyon/compile/linux-mpi/")
	
	#running tachyon for 2 process in 1 host
	os.system("mpirun -np 2 --hostfile ~/mpi_host1 -"+options.sched+" ./tachyon ../../scenes/teapot.dat>result.txt")
	file = open('result.txt','r')
	rtTime1 = file.read().split('Ray Tracing Time:     ',1)[1].split(' seconds',1)[0]
	
	#running tachyon for 4 process in 2 hosts
	os.system("mpirun -np 4 --hostfile ~/mpi_host2 -"+options.sched+" ./tachyon ../../scenes/teapot.dat>result.txt")
	file = open('result.txt','r')
	rtTime2 =  file.read().split('Ray Tracing Time:     ',1)[1].split(' seconds',1)[0]
	
	#running tachyon for 6 process in 3 hosts
	os.system("mpirun -np 6 --hostfile ~/mpi_host3 -"+options.sched+" ./tachyon ../../scenes/teapot.dat>result.txt")
	file = open('result.txt','r')
	rtTime3 =  file.read().split('Ray Tracing Time:     ',1)[1].split(' seconds',1)[0]
	
	#running tachyon for 8 process in 4 hosts
	os.system("mpirun -np 8 --hostfile ~/mpi_host4 -"+options.sched+" ./tachyon ../../scenes/teapot.dat>result.txt")
	file = open('result.txt','r')
	rtTime4 =  file.read().split('Ray Tracing Time:     ',1)[1].split(' seconds',1)[0]
	
	print "Time required for ray tracing"
	print "################################"
	print "1 cluster: "+rtTime1
	print "2 cluster: "+rtTime2
	print "3 cluster: "+rtTime3
	print "4 cluster: "+rtTime4
	
	#Y-axis data for the graph
	OY = []
	OY.append(float(rtTime1))
	OY.append(float(rtTime2))
	OY.append(float(rtTime3))
	OY.append(float(rtTime4))
	
	draw_chart(OY)

#deletes the output file before running hpcc	
def delete_output_file():
	if os.path.exists("hpccoutf.txt"):
		os.remove("hpccoutf.txt")
		#print "previous output file deleted"

def hpcc():
	print 'hpcc'
	print options.sched
	os.chdir("hpcc-1.4.3/")
	
	delete_output_file()
	# TODO #read the input file and change the inputs. How to modify a file : http://stackoverflow.com/questions/13808252/i-need-to-open-and-rewrite-a-line-in-a-file-in-python
	os.system("mpirun -np 2 --hostfile ~/mpi_host1 -"+options.sched+" ./hpcc")
	file = open('hpccoutf.txt','r')
	PTRANS_GBs1 =  file.read().split('PTRANS_GBs=',1)[1].split('PTRANS_time',1)[0]
	
	delete_output_file()
	# TODO #read the input file and change the inputs.
	os.system("mpirun -np 4 --hostfile ~/mpi_host2 -"+options.sched+" ./hpcc")
	file = open('hpccoutf.txt','r')
	PTRANS_GBs2 =  file.read().split('PTRANS_GBs=',1)[1].split('PTRANS_time',1)[0]
	
	delete_output_file()
	# TODO #read the input file and change the inputs.
	os.system("mpirun -np 6 --hostfile ~/mpi_host3 -"+options.sched+" ./hpcc")
	file = open('hpccoutf.txt','r')
	PTRANS_GBs3 =  file.read().split('PTRANS_GBs=',1)[1].split('PTRANS_time',1)[0]
	
	delete_output_file()
	# TODO #read the input file and change the inputs.
	os.system("mpirun -np 8 --hostfile ~/mpi_host4 -"+options.sched+" ./hpcc")
	file = open('hpccoutf.txt','r')
	PTRANS_GBs4 =  file.read().split('PTRANS_GBs=',1)[1].split('PTRANS_time',1)[0]

	
	print "GBs for PTRANS"
	print "################################"
	print "1 cluster: "+PTRANS_GBs1
	print "2 cluster: "+PTRANS_GBs2
	print "3 cluster: "+PTRANS_GBs3
	print "4 cluster: "+PTRANS_GBs4
	
	OY = []
	OY.append(float(PTRANS_GBs1))
	OY.append(float(PTRANS_GBs2))
	OY.append(float(PTRANS_GBs3))
	OY.append(float(PTRANS_GBs4))
	
	draw_chart(OY,"PTRANS")
	


#program starts here
	
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


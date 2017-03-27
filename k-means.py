from __future__ import print_function

import sys

import numpy as np
from pyspark import SparkContext


def parseVector(line):
    parts = line.split(',')
    if len(parts[6])>2 and len(parts[7])>2 and parts[6]!="LONGITUDE":
        if ("THEFT" in parts[1]) or ("BURGLARY" in parts[1]): 
            return "DATA",(float(parts[6]),float(parts[7]))
    return "NODATA",[0,0]


def closestPoint(p, centers):
    bestIndex = 0
    closest = float("+inf")
    for i in range(len(centers)):
        tempDist = ((p[0] - centers[i][0]) ** 2) + ((p[1] - centers[i][1]) ** 2)
        if tempDist < closest:
            closest = tempDist
            bestIndex = i
    return bestIndex


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage: kmeans <file> <k> <convergeDist>", file=sys.stderr)
        exit(-1)


    sc = SparkContext(appName="PythonKMeans")
    lines = sc.textFile((sys.argv[1]),3)
    data = lines.map(parseVector).groupByKey().mapValues(list).cache()
    data = data.filter(lambda x : "NODATA" not in x[0]).flatMap(lambda s: s[1]).cache()

    K = int(sys.argv[2])
    
    convergeDist = float(sys.argv[3])
   
    kPoints = data.takeSample(False, K, 1)
    tempDist = 1.0

    while tempDist > convergeDist:
        closest = data.map(
            lambda p: (closestPoint(p, kPoints), (p, 1)))
        pointStats = closest.reduceByKey(
            lambda p1_c1, p2_c2: ((p1_c1[0][0] + p2_c2[0][0],p1_c1[0][1] + p2_c2[0][1]), p1_c1[1] + p2_c2[1]))
       
        newPoints = pointStats.map(
            lambda st: (st[0], (st[1][0][0] / st[1][1], st[1][0][1] / st[1][1]))).collect()
        #for x in newPoints:
        #    print (x)
        tempDist = sum(((kPoints[iK][0] - p[0]) ** 2+(kPoints[iK][1] - p[1]) ** 2) for (iK, p) in newPoints)
        print ("tempdist",tempDist)
        for (iK, p) in newPoints:
            kPoints[iK] = p

    print("Final centers: " + str(kPoints))
    sc.stop()

    

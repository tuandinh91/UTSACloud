from __future__ import print_function

import sys

import numpy as np
from pyspark import SparkContext

#this function reports the GPS of thefts and burglaries
def parseVector(line):
    parts = line.split(',')
    if "THEFT" in parts[1]: 
        return parts[5],(1.0,0.0)
    if "BURGLARY" in parts[1]:
        return parts[5],(0.0,1.0)
    return "NODATA",(0.0,0.0)

#finds the closest centroid
def closestPoint(p, centers):
    bestIndex = 0
    closest = float("+inf")
    for i in range(len(centers)):
        tempDist = ((p[0] - centers[i][0]) ** 2) + ((p[1] - centers[i][1]) ** 2)
        if tempDist < closest:
            closest = tempDist
            bestIndex = i
    return bestIndex

#save create CSVLine
def toCSVLine(data):
  return ','.join(str(d) for d in data)

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage: kmeans <file> <k> <convergeDist>", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="PythonKMeans")
    lines = sc.textFile((sys.argv[1]),3)
    #filter out data not related to theft or burglaries
    data = lines.map(parseVector).filter(lambda x : "NODATA" not in x[0])
    data = data.reduceByKey(lambda p1_c1, p2_c2:(p1_c1[0]+p2_c2[0],p1_c1[1]+p2_c2[1])).cache()
   
    dataValue = data.map(lambda s: s[1]).cache()
    
    K = int(sys.argv[2])
    
    convergeDist = float(sys.argv[3])

    #initialization k points 
    kPoints = dataValue.takeSample(False, K, 1)
    tempDist = 1.0

    while tempDist > convergeDist:
        #assigning to nearest centroid and keeping count
        closest = dataValue.map(
            lambda p: (closestPoint(p, kPoints), (p, 1)))
            
        #adding all values under same cluster
        pointStats = closest.reduceByKey(
            lambda p1_c1, p2_c2: ((p1_c1[0][0] + p2_c2[0][0],p1_c1[0][1] + p2_c2[0][1]), p1_c1[1] + p2_c2[1]))
            
        #calculating new positions
        newPoints = pointStats.map(
            lambda st: (st[0], (st[1][0][0] / st[1][1], st[1][0][1] / st[1][1]))).collect()
          
        #new distance to test for convergence          
        tempDist = sum(((kPoints[iK][0] - p[0]) ** 2+(kPoints[iK][1] - p[1]) ** 2) for (iK, p) in newPoints)
        
        #assigning new points
        for (iK, p) in newPoints:
            kPoints[iK] = p
    clusters = data.map(lambda s: (closestPoint(s[1],kPoints),str(s[0])));
    
    f = open('hw3-output.txt', 'w')
    f.truncate()
    f.write('********OUTPUT********\n')
    f.write('Final centers: ' + str(kPoints))
    f.close()
    sc.stop()

    

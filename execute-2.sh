#!/bin/bash
cd $HADOOP_PREFIX
#remove the old output
bin/hadoop fs -rmr /hw2-output-p2
#run part 2
bin/hadoop jar contrib/streaming/hadoop-streaming-1.2.1.jar \
-input /hw2-input/*.csv -output /hw2-output-p2 \
-file /home/hduser/mapper-2.py -mapper /home/hduser/mapper-2.py \
-file /home/hduser/reducer-2.py -reducer /home/hduser/reducer-2.py
#copy output to local
rm -rf ~/out-2
bin/hadoop fs -copyToLocal /hw2-output-p2 ~/out-2
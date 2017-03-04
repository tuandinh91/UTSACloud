#!/bin/bash
cd $HADOOP_PREFIX
#remove the old output
bin/hadoop fs -rmr /hw2-output
#run part 1
bin/hadoop jar contrib/streaming/hadoop-streaming-1.2.1.jar \
-input /hw2-input/*.csv -output /hw2-output \
-file /home/hduser/mapper.py -mapper /home/hduser/mapper.py \
-file /home/hduser/reducer.py -reducer /home/hduser/reducer.py
#copy output to local
bin/hadoop fs -copyToLocal -f /hw2-output ~/out

# UTSACloud
Used for projects in UTSA Cloud and Big Data
http://cs-cloud.cs.utsa.edu/
acc: group8
pass: in your mail
server: 129.115.26.160
tracking: http://129.115.26.160:50030

#Always login to hduser
login 
su - hduser
pass: cloud9

#to start cluster, running now:
$HADOOP_PREFIX/bin/start-dfs.sh
$HADOOP_PREFIX/bin/start-mapred.sh
or 
$HADOOP_PREFIX/bin/start-all.sh

#to stop cluster:
$HADOOP_PREFIX/bin/stop-dfs.sh
$HADOOP_PREFIX/bin/stop-mapred.sh
or
$HADOOP_PREFIX/bin/stop-all.sh

#step to go, or just run 'execute.sh'
cd $HADOOP_PREFIX
#remove the old output
bin/hadoop fs -rmr /hw2-output
#run part 1
bin/hadoop jar contrib/streaming/hadoop-streaming-1.2.1.jar \
-input /hw2-input/*.csv -output /hw2-output \
-file /home/hduser/mapper.py -mapper /home/hduser/mapper.py \
-file /home/hduser/reducer.py -reducer /home/hduser/reducer.py
#copy output to local
rm -rf ~/out
bin/hadoop fs -copyToLocal /hw2-output ~/out

file will be ~/out/
# Hadoop speed test

In this experiment I research hadoop map/reduce job execution speed by using different programming languages and hadoop modes;

Used programming languages:  Python and Java
Used hadoop modes: Local (Standalone) and Pseudo-Distributed

Test map/reduce task:

	Given: NASA Apache Web Logs(http://opensource.indeedeng.io/imhotep/docs/sample-data/)
	
	Task: Count number of each url request root

I used same algorithm for Python and Java(You can find code in corresponding directories)

Also you can find jar for more simple Java implemention

Run command looks like:

Python(Hadoop Streaming used):

	Hadoop local mode: bin/hadoop jar $HADOOP_STREAM -file *.py -mapper mapper.py -reducer reducer.py -input input/*.tsv -output output

	Hadoop pseudo-distributed mode: bin/hadoop jar $HADOOP_STREAM -file *.py -mapper mapper.py -reducer reducer.py -input /input/*.tsv -output output

Where $HADOOP_STREAM - hadoop streaming jar path, input - input directory with tsv logs, output - output directory

Java: 	

	Hadoop local mode: bin/hadoop jar wc.jar Test /input output

	Hadoop pseudo-distributed mode: bin/hadoop jar wc.jar Test input output

Where wc.jar - jar archive with Test.java, input - input directory with tsv logs, output - output directory

Here you can see approximately execution time for each combination:
  Python local hadoop mode: 1 min, 10 sec
  Python pseudo-distributed hadoop mode: 1 min, 15 sec
  Java local hadoop mode: 55 sec
  Java pseudo-distributed hadoop mode: 58 sec

We can calculate, what Python runs slover for ~25%, when pseudo-distributed lose ~5% from execution speed

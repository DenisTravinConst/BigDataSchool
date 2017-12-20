# Hadoop
Hadoop Streaming command looks like($HADOOP_STREAM - path to hadoop streaming jar, In - folder with .tsv log):
hadoop jar $HADOOP_STREAM -file *.py -mapper mapper.py -reducer reducer.py -input In -output output

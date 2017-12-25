# Hadoop
Hadoop Streaming command looks like($HADOOP_STREAM - path to hadoop streaming jar, In - folder with .tsv log, *.py - python files with mapper and reducer):
hadoop jar $HADOOP_STREAM -mapper mapper.py -reducer reducer.py -input In -output output

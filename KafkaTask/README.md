Links for log files:

1)http://indeedeng.github.io/imhotep/files/nasa_19950630.22-19950728.12.tsv.gz
2)http://indeedeng.github.io/imhotep/files/nasa_19950731.22-19950831.22.tsv.gz

Current settings:

1)producer.py - send batch of lines to 'test' topic

#2)spark.py - read 'test' topic, count categories and send result to 'output' topic

2)spark_multi_node_stream.py - read 'test' topic, count categories in each batch and send result to 'output' topic

3)comsumer.py - read 'output' topic, addition stream categories count result;

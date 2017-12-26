Links for log files:

1)http://indeedeng.github.io/imhotep/files/nasa_19950630.22-19950728.12.tsv.gz
2)http://indeedeng.github.io/imhotep/files/nasa_19950731.22-19950831.22.tsv.gz

Current settings:
1)producer.py - send batch of lines to 'third' topic

2)spark.py - read 'third' topic, count categories and send result to 'output' topic

3)comsumer.py - read 'output' topic

"""Spark module"""
import os
import ConfigParser
import urllib
from kafka import KafkaProducer
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

RESPONSE = 'response'
INDEX_ERROR = 'indexError'
STATUS_CODE_ERROR = 'error-{}XX'

CONFIG = ConfigParser.RawConfigParser()
CONFIG.read('config.properties')
TOPIC_NAME = CONFIG.get('KafkaProperties', 'topic_name')
BROKERS = CONFIG.get('KafkaProperties', 'brokers')
OUTPUT_TOPIC = CONFIG.get('SparkProperties', 'output_topic')
CATCH_TIMEOUT = CONFIG.get('SparkProperties', 'catch_timeout')
REFRESH_STREAM_STAT_MESSAGE = CONFIG.get('SparkProperties', 'refresh_stream_stat_message')

os.environ['PYSPARK_SUBMIT_ARGS'] = CONFIG.get('SparkProperties', 'environ_settings')

PRODUCER = KafkaProducer(bootstrap_servers=BROKERS)
CATEGORIES = dict()


def main():
    """Main spark module method"""
    spark_context = SparkSession.builder.appName('MultiNodeStream').getOrCreate().sparkContext
    streaming_context = StreamingContext(spark_context, int(CATCH_TIMEOUT))
    direct_stream = KafkaUtils.createDirectStream(streaming_context, [TOPIC_NAME], {'metadata.broker.list': BROKERS})
    direct_stream.foreachRDD(handler)

    streaming_context.start()
    streaming_context.awaitTermination()


def handler(message):
    """Message handler"""
    records = message.collect()
    refresh_flag = False
    for record in records:
        line = record[1]
        if line == REFRESH_STREAM_STAT_MESSAGE:
            refresh_flag = True
        else:
            dir_set(get_root(line), CATEGORIES)
    output(CATEGORIES)
    CATEGORIES.clear()
    if refresh_flag:
        PRODUCER.send(OUTPUT_TOPIC, key = REFRESH_STREAM_STAT_MESSAGE, value=REFRESH_STREAM_STAT_MESSAGE)


def get_root(line):
    """Line analysis method"""
    try:
        line_array = line.strip().split('\t')
        status_code = line_array[5].strip()
        if status_code == RESPONSE:
            return 'log.file'
        elif status_code[0] != '2' and status_code[0] != '3':
            return STATUS_CODE_ERROR.format(status_code[0])
        else:
            url_root_array = line.strip().split('\t')[4].strip().split('/')
            url_root = url_root_array[0] + '/' + url_root_array[1]
            return urllib.unquote_plus(url_root)
    except IndexError:
        return INDEX_ERROR


def dir_set(word, dirs):
    """Directories set method"""
    if word in dirs:
        dirs[word] = int(dirs[word]) + 1
    else:
        dirs[word] = int(1)


def output(dirs):
    """Spark output method"""
    for key in dirs.keys():
        PRODUCER.send(OUTPUT_TOPIC, key=str(key), value=str(dirs[key]))


if __name__ == "__main__":
    main()

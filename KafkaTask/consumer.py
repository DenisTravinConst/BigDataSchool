"""Consumer module"""
import ConfigParser
from kafka import KafkaConsumer

BATCH_COUNT_TO_OUTPUT = 10


def main():
    """Main consumer method"""
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=BROKERS)
    categories = dict()
    output_iterator = 0
    for msg in consumer:
        category = str(msg[5])
        if category == REFRESH_STREAM_STAT_MESSAGE or output_iterator >= int(BATCH_SIZE) * BATCH_COUNT_TO_OUTPUT:
            output_iterator = 0
            backup_file = open(BACKUP_FILE_PATH, 'w')
            for key in categories.keys():
                print >> backup_file, '{}\t{}'.format(key, categories[key])
            backup_file.close()
        else:
            output_iterator += int(msg[6])
            if category in categories:
                categories[category] += int(msg[6])
            else:
                categories[category] = int(1)


if __name__ == "__main__":
    CONFIG = ConfigParser.RawConfigParser()
    CONFIG.read('resources/config.properties')
    TOPIC_NAME = CONFIG.get('SparkProperties', 'output_topic')
    BROKERS = CONFIG.get('KafkaProperties', 'brokers')
    BACKUP_FILE_PATH = CONFIG.get('SparkProperties', 'backup_file_path')
    REFRESH_STREAM_STAT_MESSAGE = CONFIG.get('SparkProperties', 'refresh_stream_stat_message')
    BATCH_SIZE = CONFIG.get('ProducerProperties', 'batch_line_size')
    main()

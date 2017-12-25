"""Producer module"""
import ConfigParser
import time
from kafka import KafkaProducer


def main():
    """Main producer method"""
    producer = KafkaProducer(bootstrap_servers=BROKERS)
    for file_path in FILES.split(','):
        log = open('{}/{}'.format(RESOURCE_FOLDER, file_path), 'r')
        batch = ''
        batch_counter = 0
        last_batch_sent = 0
        for line in log:
            batch += line
            batch_counter += 1
            if batch_counter >= int(BATCH_SIZE):
                batch += '\n BATCH END \n'
                if not time.time() - last_batch_sent > float(SENT_TIMEOUT):
                    time.sleep(float(SENT_TIMEOUT) + last_batch_sent - time.time())
                producer.send(TOPIC_NAME, batch).get()
                last_batch_sent = time.time()
                batch = ''
                batch_counter = 0
        if batch_counter != 0:
            producer.send(TOPIC_NAME, batch).get()


if __name__ == "__main__":
    CONFIG = ConfigParser.RawConfigParser()
    CONFIG.read('resources/config.properties')
    TOPIC_NAME = CONFIG.get('KafkaProperties', 'topic_name')
    BROKERS = CONFIG.get('KafkaProperties', 'brokers')
    RESOURCE_FOLDER = CONFIG.get('KafkaProperties', 'resource_folder')
    FILES = CONFIG.get('KafkaProperties', 'logs')
    BATCH_SIZE = CONFIG.get('ProducerProperties', 'batch_line_size')
    SENT_TIMEOUT = CONFIG.get('ProducerProperties', 'sent_timeout')
    main()

"""Producer module"""
import ConfigParser
import time
import Queue
from kafka import KafkaProducer


def main():
    """Main producer method"""
    producer = KafkaProducer(bootstrap_servers=BROKERS)
    for file_path in FILES.split(','):
        log = open('{}/{}'.format(RESOURCE_FOLDER, file_path.strip()), 'r')
        batch = Queue.Queue()
        last_batch_sent = 0
        for line in log:
            batch.put(line)
            if batch.qsize() >= int(BATCH_SIZE):
                if not time.time() - last_batch_sent > float(SENT_TIMEOUT):
                    time.sleep(float(SENT_TIMEOUT) + last_batch_sent - time.time())
                send_batch(producer, batch)
                last_batch_sent = time.time()
        if batch.qsize() != 0:
            send_batch(producer, batch)


def send_batch(producer, batch):
    """Batch send method"""
    while not batch.qsize() == 0:
        line = batch.get()
        try:
            request_method = line.split('\t')[3]
            producer.send(TOPIC_NAME, key=request_method, value=line).get()
        except IndexError:
            print '{}\nThis line have wrong format, SKIPPED'.format(line)


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

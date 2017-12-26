"""Consumer module"""
import ConfigParser
from kafka import KafkaConsumer


def main():
    """Main consumer method"""
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=BROKERS)
    for msg in consumer:
        print msg


if __name__ == "__main__":
    CONFIG = ConfigParser.RawConfigParser()
    CONFIG.read('resources/config.properties')
    TOPIC_NAME = CONFIG.get('KafkaProperties', 'topic_name')
    BROKERS = CONFIG.get('KafkaProperties', 'brokers')
    main()

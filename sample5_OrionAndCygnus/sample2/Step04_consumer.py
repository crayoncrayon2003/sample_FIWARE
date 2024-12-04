import os
import configparser
from kafka import KafkaConsumer, TopicPartition

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

SERVERS = '{}:{}'.format(config_ini['DEFAULT']['HOST_IP'],'9092')

def main():
    consumer = KafkaConsumer(
        bootstrap_servers=SERVERS,
        enable_auto_commit=True,
        group_id='my_group',
        value_deserializer=lambda x: x.decode('utf-8')
    )
    topic = 'my_topic'
    partition = 0
    topic_partition = TopicPartition(topic, partition)
    consumer.assign([topic_partition])
    consumer.seek_to_beginning(topic_partition)

    for message in consumer:
        print(f"Received message: {message.value}")


if __name__ == '__main__':
    main()
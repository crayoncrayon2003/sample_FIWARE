import sys
import six
import json
import re
# Compatibility with python3.12
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves
from kafka import KafkaConsumer

# kafka setting
TOPIC_NAME = "text_topic"
PARTITIONS = 1
REPLICATION = 1

def replace_last_occurrence(input, target, replacement):
    pattern = re.compile(re.escape(target) + r'(?!.*' + re.escape(target) + ')')
    return pattern.sub(replacement, input)

def main():
    # Create Kafka KafkaConsumer
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="my-group",
        value_deserializer=lambda x: x.decode('utf-8')
    )

    # Received topic
    for message in consumer:
        msg = message.value
        # Remove delimiter
        msg = replace_last_occurrence(msg, 'xffff', '')
        print(json.dumps(json.loads(msg), indent=2))

if __name__ == "__main__":
    main()

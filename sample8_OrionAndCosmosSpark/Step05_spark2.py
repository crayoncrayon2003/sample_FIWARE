from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.receiver import Receiver
import requests
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyspark.storagelevel import StorageLevel

class OrionCustomReceiver(Receiver):
    def __init__(self, host, port):
        super().__init__(StorageLevel.MEMORY_AND_DISK_2)
        self.host = host
        self.port = port

    def onStart(self):
        self.thread = threading.Thread(target=self.receive)
        self.thread.start()

    def onStop(self):
        pass

    def receive(self):
        server = HTTPServer((self.host, self.port), OrionHTTPHandler)
        server.stream = self
        server.serve_forever()

class OrionHTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        event = json.loads(post_data)
        self.server.stream.store(event)
        self.send_response(200)
        self.end_headers()

class Sensor:
    def __init__(self, device_type):
        self.device = device_type

    def __repr__(self):
        return f"Sensor(device={self.device})"


conf = SparkConf() \
    .setAppName("KafkaConsumer") \
    .setMaster('local') \
    .set("spark.local.ip", "localhost") \
    .set("spark.pyspark.driver.python", "/usr/bin/python3.12") \
    .set("spark.pyspark.python", "/usr/bin/python3.12") \
    .set("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3,org.apache.kafka:kafka-clients:2.3.0") \
    .set("spark.sql.adaptive.enabled", "false") \
    .set("spark.executor.memory", "2g") \
    .set("spark.driver.memory", "2g") \
    .set("spark.executor.cores", "4")

sc = SparkContext(conf=conf)
ssc = StreamingContext(sc, 60)

def main():

    # Create Custom Receiver to receive notifications on port 9001
    eventStream = ssc.receiverStream(OrionCustomReceiver("localhost", 9001))

    # Process event stream
    processedDataStream = (eventStream
        .flatMap(lambda event: event["data"])
        .map(lambda ent: Sensor(ent["type"]))
        .countByValue()
        .window(60))

    processedDataStream.pprint()

    ssc.start()
    ssc.awaitTermination()

if __name__ == "__main__":
    main()

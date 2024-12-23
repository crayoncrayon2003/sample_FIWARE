from fpc import connector

from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf, StorageLevel

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

def start_http_server(host, port, stream):
    server = HTTPServer((host, port), OrionHTTPHandler)
    server.stream = stream
    threading.Thread(target=server.serve_forever).start()

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

    # Start HTTP server to receive notifications on port 9001
    start_http_server("localhost", 9002, ssc)

    # Process event stream
    eventStream = ssc.queueStream([], default=True)

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

import os
import shutil
import sys
import six
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import from_json, col, window, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType, MapType, TimestampType

# Compatibility with python3.12
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

# create workdir
DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
DIR_OUTPUT = os.path.join(DIR_ROOT, "output")
DIR_CHECKPOINT = os.path.join(DIR_ROOT, "checkpoint")
if os.path.exists(DIR_OUTPUT): shutil.rmtree(DIR_OUTPUT)
if os.path.exists(DIR_CHECKPOINT): shutil.rmtree(DIR_CHECKPOINT)
os.makedirs(DIR_OUTPUT, exist_ok=True)
os.makedirs(DIR_CHECKPOINT, exist_ok=True)

# Spark configuration
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

spark = SparkSession.builder.config(conf=conf).getOrCreate()

# Set log level to INFO to reduce verbosity
spark.sparkContext.setLogLevel("INFO")

def main():
    # Define schema for the incoming data
    schema = StructType([
        StructField("subscriptionId", StringType(), True),
        StructField("data", ArrayType(
            StructType([
                StructField("id", StringType(), True),
                StructField("type", StringType(), True),
                StructField("humidity", StructType([
                    StructField("type", StringType(), True),
                    StructField("value", IntegerType(), True),
                    StructField("metadata", MapType(StringType(), StringType()), True)
                ]), True),
                StructField("name", StructType([
                    StructField("type", StringType(), True),
                    StructField("value", StringType(), True),
                    StructField("metadata", MapType(StringType(), StringType()), True)
                ]), True),
                StructField("temperature", StructType([
                    StructField("type", StringType(), True),
                    StructField("value", IntegerType(), True),
                    StructField("metadata", MapType(StringType(), StringType()), True)
                ]), True)
            ])
        ), True)
    ])

    # Reading stream from socket
    df = spark \
        .readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", 9001) \
        .load()

    # Parse JSON payload
    parsed_df = df \
        .select(from_json(col("value").cast("string"), schema) \
        .alias("parsed_value"))

    # Flatten the structure and extract necessary fields
    exploded_df = parsed_df  \
        .selectExpr("parsed_value.data", "explode(parsed_value.data) as event") \
        .selectExpr("event.id", "event.type", "event.humidity.value as humidity", "event.temperature.value as temperature", "current_timestamp() as timestamp")

    # Add watermark to handle late data
    exploded_df = exploded_df.withWatermark("timestamp", "1 minute")

    # Perform windowed aggregation
    windowedCounts = exploded_df \
        .groupBy(
            window(col("timestamp"), "20 seconds"),
            col("id"),
            col("type")
        ) \
        .count() \
        .selectExpr("window.start as window_start", "window.end as window_end", "id", "type", "count")

    # Start running the query that prints the running counts to the file
    query = windowedCounts.writeStream \
        .format("csv") \
        .option("path", DIR_OUTPUT) \
        .option("checkpointLocation", DIR_CHECKPOINT) \
        .outputMode("append") \
        .start()

    # setting to stop after 60 seconds
    query.awaitTermination()

if __name__ == '__main__':
    main()

from flask import Flask, request
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.sql.functions import col, avg
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType
import threading
import os
import shutil
from datetime import datetime

DIR_ROOT   = os.path.dirname(os.path.abspath(__file__))
DIR_OUTPUT = os.path.join(DIR_ROOT, "output")

# Output Dir
shutil.rmtree(DIR_OUTPUT, ignore_errors=True)
os.mkdir(DIR_OUTPUT)

# REST API
app = Flask(__name__)
data_queue = []

class Sensor:
    def __init__(self, id, type, humidity, temperature):
        self.id = id
        self.type = type
        self.humidity = humidity
        self.temperature = temperature

def parse_json(data):
    sensors = []
    for item in data["data"]:
        id = item["id"]
        type = item["type"]
        humidity = item["humidity"]["value"]
        temperature = item["temperature"]["value"]
        sensors.append(Sensor(id, type, humidity, temperature))
    return sensors

@app.route('/sensor', methods=['POST'])
def sensor_data():
    data = request.json
    sensors = parse_json(data)
    for sensor in sensors:
        data_queue.append(sensor.__dict__)
    return 'Data received', 200

# spark
def process_spark(spark, schema, rdd):
    if not rdd.isEmpty():
        sensor_df = spark.createDataFrame(rdd, schema=schema)
        sensor_df = sensor_df.dropna()

        if sensor_df.count() > 0:
            humidity_avg = sensor_df.select(avg(col("humidity"))).first()[0]
            temperature_avg = sensor_df.select(avg(col("temperature"))).first()[0]
            print("Average humidity: {0}, Average temperature: {1}".format(humidity_avg, temperature_avg))

            # Save averages
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            ## Save averages to Parquet files
            avg_schema = StructType([StructField("avg_value", FloatType(), True)])

            humidity_df = spark.createDataFrame([(humidity_avg,)], avg_schema)
            temperature_df = spark.createDataFrame([(temperature_avg,)], avg_schema)

            humidity_df.write.mode("overwrite").parquet(f"{DIR_OUTPUT}/{timestamp}/humidity_avg")
            temperature_df.write.mode("overwrite").parquet(f"{DIR_OUTPUT}/{timestamp}/temperature_avg")

            ## Save averages to CSV
            avg_data = [(timestamp, humidity_avg, temperature_avg)]
            avg_schema = StructType([
                StructField("timestamp", StringType(), True),
                StructField("humidity_avg", FloatType(), True),
                StructField("temperature_avg", FloatType(), True)
            ])

            avg_df = spark.createDataFrame(avg_data, schema=avg_schema)
            temp_output_path = os.path.join(DIR_OUTPUT, "temp")

            if not os.path.exists(temp_output_path):
                avg_df.coalesce(1).write.mode("overwrite").option("header", "true").csv(temp_output_path)
            else:
                avg_df.coalesce(1).write.mode("append").option("header", "false").csv(temp_output_path)

            # Merge part files into a single CSV
            output_path = os.path.join(DIR_OUTPUT, "averages.csv")
            temp_csv_files = [f for f in os.listdir(temp_output_path) if f.startswith("part-") and f.endswith(".csv")]
            if temp_csv_files:
                temp_csv_file = os.path.join(temp_output_path, temp_csv_files[0])
                if not os.path.exists(output_path):
                    shutil.move(temp_csv_file, output_path)
                else:
                    with open(output_path, "a") as output_csv:
                        with open(temp_csv_file, "r") as temp_csv:
                            next(temp_csv)  # Skip header line
                            shutil.copyfileobj(temp_csv, output_csv)
                    os.remove(temp_csv_file)
        else:
            print("No valid data to process")
    else:
        print("No data received")

def run_spark():
    spark = SparkSession.builder.appName("CustomSparkApp").getOrCreate()
    ssc = StreamingContext(spark.sparkContext, 5)  # Batch interval

    def create_rdd(time, rdd):
        if data_queue:
            rdd = spark.sparkContext.parallelize(data_queue)
            data_queue.clear()
        else:
            rdd = spark.sparkContext.emptyRDD()
        return rdd

    schema = StructType([
        StructField("id", StringType(), True),
        StructField("type", StringType(), True),
        StructField("humidity", IntegerType(), True),
        StructField("temperature", IntegerType(), True)
    ])

    rdd_queue = [ssc.sparkContext.parallelize(data_queue)]
    input_stream = ssc.queueStream(rdd_queue)

    windowed_stream = input_stream.window(10, 5)  # Window size
    windowed_stream.foreachRDD(lambda time, rdd: process_spark(spark, schema, create_rdd(time, rdd)))

    ssc.start()
    ssc.awaitTermination()

if __name__ == "__main__":
    threading.Thread(target=run_spark).start()
    app.run(host='0.0.0.0', port=9001)

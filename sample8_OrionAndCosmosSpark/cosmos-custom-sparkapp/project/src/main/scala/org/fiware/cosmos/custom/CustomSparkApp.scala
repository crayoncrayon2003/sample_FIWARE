package org.fiware.cosmos.custom

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.rdd.RDD
import org.fiware.cosmos.orion.spark.connector.{NgsiEvent, OrionReceiver}
import org.json4s._
import org.json4s.jackson.JsonMethods._
import java.io._
import java.nio.file.{Paths, Files}
import java.util.logging.{Logger, Level}

object CustomSparkApp {
  implicit val formats: DefaultFormats.type = DefaultFormats
  val logger: Logger = Logger.getLogger(CustomSparkApp.getClass.getName)

  case class Sensor(id: String, `type`: String, humidity: Attribute, temperature: Attribute)
  case class Attribute(`type`: String, value: Any)
  case class Notification(subscriptionId: String, data: List[Sensor])

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setAppName("CustomSparkApp")
      .set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")

    val ssc = new StreamingContext(conf, Seconds(5))
    val eventStream = ssc.receiverStream(new OrionReceiver(9001))

    eventStream.foreachRDD {
      rdd => logger.log(Level.INFO, s"Received ${rdd.count()} events")
      rdd.collect().foreach(event => logger.log(Level.INFO, event.toString))
    }

    val processedDataStream = eventStream.flatMap { record =>
      logger.log(Level.INFO, s"Processing record: $record")
      try {
        val ngsiEvent = record.asInstanceOf[NgsiEvent]
        val jsonString = ngsiEvent.toString
        val json = parse(jsonString)
        val notification = json.extract[Notification]
        notification.data
      } catch {
        case e: Exception =>
          logger.log(Level.SEVERE, s"Error parsing JSON: ${record.toString}", e)
          List.empty[Sensor]
      }
    }.window(Seconds(10))

    processedDataStream.print()

    processedDataStream.foreachRDD { rdd =>
      val count = rdd.count()
      if (count > 0) {
        val humiditySum = rdd.map(sensorData => sensorData.humidity.value.toString.toDouble).reduce(_ + _)
        val temperatureSum = rdd.map(sensorData => sensorData.temperature.value.toString.toDouble).reduce(_ + _)
        val humidityAvg = humiditySum / count
        val temperatureAvg = temperatureSum / count
        logger.log(Level.INFO, s"Average humidity: $humidityAvg, Average temperature: $temperatureAvg")
        saveToCSV(rdd)
      } else {
        logger.log(Level.INFO, "No data received")
      }
    }

    ssc.start()
    ssc.awaitTermination()
  }

  def saveToCSV(rdd: RDD[Sensor]): Unit = {
    val outputDir = Paths.get("/opt/spark-apps/output").toFile
    if (!outputDir.exists()) {
      outputDir.mkdir()
    }
    val outputFile = new File(outputDir, "sensor_data.csv")

    val header = "ID,Type,Humidity,Temperature"
    val data = rdd.map(sensor => s"${sensor.id},${sensor.`type`},${sensor.humidity.value},${sensor.temperature.value}").collect()

    val bw = new BufferedWriter(new FileWriter(outputFile, true))
    if (outputFile.length() == 0) {
      bw.write(header)
      bw.newLine()
    }
    data.foreach { line =>
      bw.write(line)
      bw.newLine()
    }
    bw.close()
  }
}

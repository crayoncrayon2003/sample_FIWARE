# case1 : scala
## Note
I could not get “orion.spark.connector” to work.
Because the versions of scala and spark are old.

## Build spark application
ref : https://sparkbyexamples.com/pyspark/spark-submit-python-file/

```
cd cosmos-custom-sparkapp/project
curl -LO https://github.com/ging/fiware-cosmos-orion-spark-connector/releases/download/FIWARE_7.9.1/orion.spark.connector-1.2.2.jar
mvn install:install-file \
  -Dfile=./orion.spark.connector-1.2.2.jar \
  -DgroupId=org.fiware.cosmos \
  -DartifactId=orion.spark.connector \
  -Dversion=1.2.2 \
  -Dpackaging=jar
```

```
cd cosmos-custom-sparkapp/project
mvn clean package
```

## Copy Jar
```
FROM : cosmos-custom-sparkapp/project/target/cosmos-custom-1.0-SNAPSHOT-jar-with-dependencies.jar
TO   : spark-apps/cosmos-custom-1.0-SNAPSHOT-jar-with-dependencies.jar
```

## Run spark application
```
docker compose up -d
docker exec -it spark-worker1 bash

(spark-worker1) : /opt/bitnami/spark/bin/spark-submit --class org.fiware.cosmos.custom.CustomSparkApp --master spark://spark-master:7077 --deploy-mode client /opt/spark-apps/cosmos-custom-1.0-SNAPSHOT-jar-with-dependencies.jar --conf "spark.driver.extraJavaOptions=-Dlog4jspark.root.logger=DEBUG,console"
```

## run test
```
python Step01_orion_make_entities.py
python Step02_orion_subscriptions.py
python Step03_orion_subscriptions.py

```

## down
```
docker compose down
```

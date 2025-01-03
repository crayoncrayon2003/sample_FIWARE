
# Install JarFile
https://spark.apache.org/docs/3.5.3/submitting-applications.html

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

# Make JarFile
```
cd cosmos-custom-sparkapp/project
mvn clean package
```

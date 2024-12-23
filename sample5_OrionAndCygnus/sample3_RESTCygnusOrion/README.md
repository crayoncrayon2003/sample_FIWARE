# 0. Abstract
![image](https://github.com/crayoncrayon2003/sample_FIWARE/blob/main/sample5_OrionAndCygnus/sample3_RESTCygnusOrion/figure.png)

# 1.Preparation

## 1.1. Source

### 1.1.1. Make source Jar
```
cd flume-custom-source-const/project
mvn clean package
```

### 1.1.2. Copy JAR files into cygnus
```
From : flume-custom-source-const/project/target/flume-custom-source-const-0.0.1-SNAPSHOT.jar
To   : cygnus/lib/flume-custom-source-const-0.0.1-SNAPSHOT.jar
```

## 1.2. Sink

### 1.2.1 Make Sink Jar
```
cd flume-custom-sink-orion/project
mvn clean package
```

### 1.2.2. Copy JAR files into cygnus
```
From : flume-custom-sink-orion/project/target/flume-custom-sinks-orion-0.0.1-SNAPSHOT.jar
To   : cygnus/lib/flume-custom-sinks-orion-0.0.1-SNAPSHOT.jar
```

# 2. build and run
```
docker compose up -d
```

# 3. Confirm
```
python3.12 Step01_orion_get_entities.py
```

# 4. down
```
docker compose down
```

# case2 : python
## Run spark application
```
docker compose up -d
docker exec -it spark-worker1 bash

(spark-worker1) : pip install Flask
(spark-worker1) : /opt/bitnami/spark/bin/spark-submit --master spark://spark-master:7077 --deploy-mode client /opt/spark-apps/cosmos-custom-py-app.py --conf spark.executor.extraJavaOptions=-Djava.net.preferIPv4Stack=true
```

## run test
```
python Step01_orion_make_entities.py
python Step02_orion_subscriptions.py
python Step03_orion_subscriptions.py
```

## Confirmation of results
see ./spark-apps/output

## down
```
docker compose down
```

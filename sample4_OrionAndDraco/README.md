# make dir
```
mkdir -p ./draco/fileprocessor ./draco/database ./draco/flow_storage
```

# build and run
```
docker compose up -d
```
wait for 3 minutes.

# control by GUI
Access the following URL using the Web browser.
```
http://localhost:8080/nifi/
```

# control by python
```
pip install nipyapi
```

# down
```
docker compose down
```

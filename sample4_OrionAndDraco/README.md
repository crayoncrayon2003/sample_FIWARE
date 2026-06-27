# make dir
```bash
mkdir -p ./draco/fileprocessor ./draco/database ./draco/flow_storage
```

# build and run
```bash
docker compose up -d
```
wait for 5 minutes.

# control using GUI
Access the following URL using the Web browser.
```bash
http://localhost:8080/nifi/
```

# control using python
```bash
pip install nipyapi
```

# down
```bash
docker compose down
```

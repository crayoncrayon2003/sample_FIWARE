# build and run
```
docker compose up -d
```

# control using GUI
## Access URL
Access the following URL using the Web browser.
```
http://localhost:1337/
```

## First Setting
First Access, Input Access Info
* username         : any  ex: kongadmin
* Email            : any  ex:
* password         : any  ex: kongadmin
* confirm password : any  ex: kongadmin

DASHBOARD -> DEFAULT, input following info
* Name            :　kong-admin
* Kong Admin URL  :　http://kong:8001

## Sample1 : api request(GET) to orion from client via kong
### make service (kong to orion)
1. SERVICES
2. ADD NEW SERVICE
3. Input info
* Name      : Sample1
* Protocol  : http
* Host      : orion1
* Port      : 1026

### service routing (cliant to kong)
1. SERVICES
2. select Sample1
3. Routes　
4. ADD ROUTE
5. Input info
* Name      : sample1-api
* Host      : localhost     (input enter)
* Paths     : /sample1-api  (input enter)
* Methods   : GET           (input enter)
* Protocols : http          (delete https)

### exec cliant request
```
python Step01_sample1.py
```

## Sample2 : api request(GET/POST) to orion from client via kong
### make service (kong to orion)
1. SERVICES
2. ADD NEW SERVICE
3. Input info
* Name      : Sample2
* Protocol  : http
* Host      : orion1
* Port      : 1026

### service routing (cliant to kong)
1. SERVICES
2. select Sample2
3. Routes　
4. ADD ROUTE
5. Input info
* Name      : sample2-api
* Host      : localhost     (input enter)
* Paths     : /sample2-api  (input enter)
* Methods   : GET           (input enter),  POST(input enter)
* Protocols : http          (delete https)

### exec cliant request
```
python Step02_sample2.py
```

## Sample3 : api request to orion from client via kong with API Key
### make service (kong to orion)
1. SERVICES
2. ADD NEW SERVICE
3. Input info
* Name      : Sample3
* Protocol  : http
* Host      : orion1
* Port      : 1026

### service routing (cliant to kong)
1. SERVICES
2. select Sample3
3. Routes　
4. ADD ROUTE
5. Input info
* Name      : sample3-api
* Host      : localhost     (input enter)
* Paths     : /sample3-api  (input enter)
* Methods   : GET           (input enter),  POST(input enter)
* Protocols : http          (delete https)

### create consumers
1. CONSUMERS
2. Create Consumer
3. Input info
* username  : sample3-user
* custom_id : sample3-user
* Tags      : (blank)

### create API Key
1. CONSUMERS
2. select sample3-user
3. Credencials
4. Api Keys
5. CREATE API KEYS
6. Input "sample3-apikey"

### create api-key for consumers
1. SERVICES
2. select Sample3
3. Plugins
4. ADD PLUGIN
5. AUTHENTICATION
6. select "key auth", click "ADD PLUGIN"
5. Input info
* consumer          : (blank)
* key names         : api-key (input enter)
* hide credentials  : NO
* key in header     : YES
* key in query      : YES
* key in body       : NO
* run on preflight  : YES

### exec cliant request
```
python Step03_sample3.py
```


# down
```
docker compose down
```

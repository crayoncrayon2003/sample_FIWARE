# build and run
```
./Step01_makedir.sh
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

## Step1 : Setting Kong
```
python Step11_SettingKong
```

## Step2 : Exec REST API
### this sample is ng respons
```
python Step21_sample.py
```

### this sample is ok respons
this sample is error respons
```
python Step22_sample.py
```

# down
```
docker compose down
./Step99_rmdir.sh
```

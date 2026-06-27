# build and run
```bash
./Step01_makedir.sh
docker compose up -d
```

# control using GUI
## Access URL
Access the following URL using the Web browser.
```bash
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
```bash
python Step11_SettingKong
```

## Step2 : Exec REST API
### this sample is ng respons
```bash
python Step21_sample.py
```

### this sample is ok respons
this sample is error respons
```bash
python Step22_sample.py
```

# down
```bash
docker compose down
./Step99_rmdir.sh
```

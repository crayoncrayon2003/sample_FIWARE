import os
import configparser
from FiwareAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

ORION1 = 'http://{}:1026'.format(config_ini['DEFAULT']['HOST_IP'])
ORION2 = 'http://{}:1027'.format(config_ini['DEFAULT']['HOST_IP'])
ORION3 = 'http://{}:1028'.format(config_ini['DEFAULT']['HOST_IP'])
WEBSERVER = 'http://{}:8080'.format(config_ini['DEFAULT']['HOST_IP'])

SERVICE = 'service1'            # multi-tenant name
SERVICEPATH = '/servicepath1'   # data storage path

URN  = "urn:ngsi-ld:Sensor:002" # data identifier
TYPE = "Sensor"                 # data type

def makeSensor():
    fiware = FiwareAPI(ORION3,SERVICE,SERVICEPATH)

    body = {
        "id": URN,
        "type": TYPE,
        "name": {
            "type": "Text",
            "value": TYPE,
            "metadata": {}
        },
        "temperature": {
            "type": "Integer",
            "value": 20,
            "metadata": {}
        },
        "humidity": {
            "type": "Integer",
            "value": 20,
            "metadata": {}
        }
    }
    [rsp, body] = fiware.postEntities(body=body)
    fiware.printResponse(rsp)
    # fiware.printJsonString(body)

def main():
    print("make a storage area in orion to store sensor values (temperature and humidity).")
    makeSensor()

if __name__=='__main__':
    main()

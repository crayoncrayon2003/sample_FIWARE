import os
import configparser
from FiwareAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

ORION = 'http://{}:1026'.format(config_ini['DEFAULT']['HOST_IP'])
CYGNUS = 'http://{}:5080'.format(config_ini['DEFAULT']['HOST_IP'])

SERVICE = 'service1'            # multi-tenant name
SERVICEPATH = '/servicepath1'   # data storage path

URN  = "urn:ngsi-ld:Sensor:001" # data identifier
TYPE = "Sensor"                 # data type

def makeSensor():
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

    body = {
        "id": URN,
        "type": TYPE,
        "name": {
            "type": "Text",
            "value": TYPE,
        },
        "temperature": {
            "type": "Integer",
            "value": 20,
        },
        "humidity": {
            "type": "Integer",
            "value": 20,
        }
    }
    [rsp, body] = fiware.postEntities(body=body)
    fiware.printResponse(rsp)
    # fiware.printJsonString(body)

def getSensor():
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

    query = {'type' : TYPE}
    urn = URN
    [rsp, body] = fiware.getEntities(query=query, urn=urn)
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def main():
    print("make a storage area in orion to store sensor values (temperature and humidity).")
    makeSensor()

    print("get sensor values (temperature and humidity) from orion")
    getSensor()


if __name__=='__main__':
    main()

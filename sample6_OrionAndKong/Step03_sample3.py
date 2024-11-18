import os
import configparser
from FiwareAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

ORION1 = 'http://localhost:8000/sample3-api'

SERVICE = 'service1'            # multi-tenant name
SERVICEPATH = '/servicepath1'   # data storage path

URN  = "urn:ngsi-ld:Sensor:001" # data identifier
TYPE = "Sensor"                 # data type
API_KEY ="sample3-apikey"

def getVersion():
    fiware = FiwareAPI(ORION1,SERVICE,SERVICEPATH)
    query = {
        "api-key" : API_KEY
    }

    [rsp, body] = fiware.getVersion(query=query)
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def makeSensor():
    fiware = FiwareAPI(ORION1,SERVICE,SERVICEPATH)

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
    query = {
        "api-key" : API_KEY
    }

    [rsp, body] = fiware.postEntities(query=query, body=body)
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def getSensor():
    fiware = FiwareAPI(ORION1,SERVICE,SERVICEPATH)

    query = {
        'type' : TYPE,
        "api-key" : API_KEY
    }

    urn = URN
    [rsp, body] = fiware.getEntities(query=query, urn=urn)
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def main():
    print("get orion version")
    getVersion()

    print("post sensor values. kong allow pots method")
    makeSensor()

    print("get sensor values.")
    getSensor()

if __name__=='__main__':
    main()

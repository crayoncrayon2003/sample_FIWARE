import os
import configparser
from FiwareAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

ORION1 = 'http://localhost:8000/orion-service'

SERVICE = 'service1'            # multi-tenant name
SERVICEPATH = '/servicepath1'   # data storage path

URN  = "urn:ngsi-ld:Sensor:001" # data identifier
TYPE = "Sensor"                 # data type

fiware = FiwareAPI(ORION1,SERVICE,SERVICEPATH)

def makeSensor():
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
    fiware.printJsonString(body)

def getSensor():
    query = {'type' : TYPE}
    urn = URN
    [rsp, body] = fiware.getEntities(query=query, urn=urn)
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def main():
    print("post sensor values.")
    makeSensor()

    print("get sensor values.")
    getSensor()

if __name__=='__main__':
    main()

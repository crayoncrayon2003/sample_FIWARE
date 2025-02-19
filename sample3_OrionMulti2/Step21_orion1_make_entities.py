import os
import configparser
import random
from FiwareAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

ORION1 = 'http://{}:1026'.format(config_ini['DEFAULT']['HOST_IP'])

SERVICE = 'service3'            # multi-tenant name
SERVICEPATH = '/servicepath3'   # data storage path

URN  = "urn:ngsi-ld:Sensor:{}"  # data identifier
TYPE = "Sensor"                 # data type

def makeSensor():
    fiware = FiwareAPI(ORION1,SERVICE,SERVICEPATH)

    body = {
        "actionType": "append",
        "entities": []
    }
    for idx in range(1, 1+3):
        temp = {
            "id"         : f"urn:ngsi-ld:Sensor:{idx:03d}",
            "type"       : TYPE,
            "name"       : {"type": "Text",    "value": TYPE, "metadata": {}},
            "temperature": {"type": "Integer", "value": random.randint(1, 10), "metadata": {}},
            "humidity"   : {"type": "Integer", "value": random.randint(1, 10), "metadata": {}}
        }
        body["entities"].append(temp)

    [rsp, body] = fiware.postOpUpdate(body=body)
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

    # fiware.printJsonString(body)

def getSensor():
    fiware = FiwareAPI(ORION1,SERVICE,SERVICEPATH)

    query = {
        'type' : TYPE,
        'limit': 100
    }
    for idx in range(1, 1+3):
        urn = f"urn:ngsi-ld:Sensor:{idx:03d}"
        [rsp, body] = fiware.getEntities(query=query, urn=urn)
        fiware.printResponse(rsp)
        fiware.printJsonString(body)

def main():
    print("make a storage area in orion to store sensor values (temperature and humidity).")
    makeSensor()

if __name__=='__main__':
    main()

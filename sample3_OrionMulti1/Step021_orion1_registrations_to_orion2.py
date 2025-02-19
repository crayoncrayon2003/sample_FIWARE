import os
import configparser
import json
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

def getRegistrations():
    fiware = FiwareAPI(ORION1,SERVICE,SERVICEPATH)

    [rsp, body] = fiware.getRegistrations()
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def setRegistrations():
    fiware = FiwareAPI(ORION1,SERVICE,SERVICEPATH)

    body = {
        "dataProvided": {
            "entities": [
                {
                    "id": URN,
                    "type": TYPE
                }
            ],
        },
        "provider": {
            "http": {
                "url": "http://orion2:1026/v2"
            },
            "supportedForwardingMode": "all"
        },
    }
    [rsp, body] = fiware.postRegistrations(body=body)
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def deleteRegistrationsAll():
    fiware = FiwareAPI(ORION1,SERVICE,SERVICEPATH)

    [rsp, body] = fiware.getRegistrations()
    # fiware.printResponse(rsp)
    # fiware.printJsonString(body)

    for item in json.loads(body):
        [rsp, body] = fiware.deleteRegistrations(urn=item["id"])
        # fiware.printResponse(rsp)
        # fiware.printJsonString(body)

def main():
    # Initialize Registrations Setting to avoid duplicate settings
    deleteRegistrationsAll()

    print("client requests a Http Get to ORION, orion will forward the request to webserver")
    setRegistrations()
    print("get settings from ORION")
    getRegistrations()


if __name__=='__main__':
    main()

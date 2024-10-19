import os
import configparser
import json
from FiwareAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

ORION = 'http://{}:1026'.format(config_ini['DEFAULT']['HOST_IP'])
QUANTUMLEAP = 'http://{}:8668'.format(config_ini['DEFAULT']['HOST_IP'])
WEBSERVER = 'http://{}:8080'.format(config_ini['DEFAULT']['HOST_IP'])

SERVICE = 'service1'            # multi-tenant name
SERVICEPATH = '/servicepath1'   # data storage path

URN  = "urn:ngsi-ld:Product:002"# data identifier
TYPE = "Product"                # data type

def getRegistrations():
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

    [rsp, body] = fiware.getRegistrations()
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def setRegistrations():
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

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
                "url": WEBSERVER+"/v2/notify"
            },
        },
    }
    [rsp, body] = fiware.postRegistrations(body=body)
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def deleteRegistrations(id):
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

    urn = id
    [rsp, body] = fiware.deleteRegistrations(urn=urn)
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def deleteRegistrationsAll():
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

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

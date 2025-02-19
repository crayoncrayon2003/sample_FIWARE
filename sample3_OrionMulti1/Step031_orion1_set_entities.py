import os
import configparser
import time
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

def getSensor():
    fiware = FiwareAPI(ORION1,SERVICE,SERVICEPATH)

    query = {'type' : TYPE}
    urn = URN
    [rsp, body] = fiware.getEntities(query=query, urn=urn)
    fiware.printResponse(rsp)
    fiware.printJsonString(body)


def updateSensorAll(temperature,humidity):
    fiware = FiwareAPI(ORION1,SERVICE,SERVICEPATH)

    body = {
        "temperature": { "type": "Integer", "value": temperature, "metadata": {} },
        "humidity":    { "type": "Integer", "value": humidity,    "metadata": {} }
    }
    query = {'type' : TYPE}
    urn = URN+"/attrs/"
    [rsp, body] = fiware.patchEntities(query=query, urn=urn, body=body)
    fiware.printResponse(rsp)
    # fiware.printJsonString(body)

def main():
    print("update sensor values (temperature and humidity) for orion")
    updateSensorAll(100,200)

    print("wait")
    time.sleep(3)

    print("get sensor values (temperature and humidity) from orion")
    getSensor()

if __name__=='__main__':
    main()

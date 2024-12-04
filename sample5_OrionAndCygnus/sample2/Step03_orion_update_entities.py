import os
import configparser
import time
from FiwareAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

ORION = 'http://{}:1026'.format(config_ini['DEFAULT']['HOST_IP'])
CYGNUS = 'http://{}:5080'.format(config_ini['DEFAULT']['HOST_IP'])

SERVICE = 'service1'            # multi-tenant name
SERVICEPATH = '/servicepath1'   # data storage path

URN  = "urn:ngsi-ld:Sensor:001" # data identifier
TYPE = "Sensor"                 # data type

def getSensor():
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

    query = {'type' : TYPE}
    urn = URN
    [rsp, body] = fiware.getEntities(query=query, urn=urn)
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def updateSensorAll(temperature,humidity):
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

    body = {
        "temperature": { "type": "Integer", "value": temperature, "metadata": {} },
        "humidity":    { "type": "Integer", "value": humidity,    "metadata": {} }
    }
    query = {'type' : TYPE}
    urn = URN+"/attrs/"
    [rsp, body] = fiware.patchEntities(query=query, urn=urn, body=body)
    fiware.printResponse(rsp)
    # fiware.printJsonString(body)

def updateSensorTemperature(temperature):
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

    query = {'type' : TYPE}
    body = str(temperature)
    urn = URN+"/attrs/temperature/value"
    [rsp, body] = fiware.putEntities(query=query, urn=urn, body=body)
    fiware.printResponse(rsp)
    # fiware.printJsonString(body)

def updateSensorHumidity(humidity):
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

    query = {'type' : TYPE}
    body = str(humidity)
    urn = URN+"/attrs/humidity/value"
    [rsp, body] = fiware.putEntities(query=query, urn=urn, body=body)
    fiware.printResponse(rsp)
    # fiware.printJsonString(body)

def main():
    temperature = 3
    humidity    = 4
    for idx in range(0, 1, 10):
        temperature+=1
        humidity+=1
        print("update sensor values (temperature) for orion")
        updateSensorAll(idx*10+temperature, idx*10+humidity)
        print("get sensor values (temperature) from orion")
        getSensor()
        print("wait")
        time.sleep(3)


if __name__=='__main__':
    main()

import os
import time
import random
import configparser
from FiwareAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

ORION = 'http://{}:1026'.format(config_ini['DEFAULT']['HOST_IP'])
SPARK = 'http://{}:9001'.format(config_ini['DEFAULT']['HOST_IP'])

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
    temperature = 10
    humidity    = 10
    time_interval = 2
    for idx in range(0, 50, 1):
        temperature += random.randint(1, 10)
        humidity    += random.randint(1, 10)
        updateSensorAll(temperature,humidity)
        print("temperature={0}, humidity={0}".format(temperature,humidity))
        print("wait")
        time.sleep(time_interval)


if __name__=='__main__':
    main()

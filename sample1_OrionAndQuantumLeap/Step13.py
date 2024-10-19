import os
import configparser
import time
from FiwareAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

ORION = 'http://{}:1026'.format(config_ini['DEFAULT']['HOST_IP'])
QUANTUMLEAP = 'http://{}:8668'.format(config_ini['DEFAULT']['HOST_IP'])
WEBSERVER = 'http://{}:8080'.format(config_ini['DEFAULT']['HOST_IP'])

SERVICE = 'service1'            # multi-tenant name
SERVICEPATH = '/servicepath1'   # data storage path

URN  = "urn:ngsi-ld:Sensor:001" # data identifier
TYPE = "Sensor"                 # data type

def updateSensorTemperature(temperature):
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

    query = {'type' : TYPE}
    body = str(temperature)
    urn = URN+"/attrs/temperature/value"
    [rsp, body] = fiware.putEntities(query=query, urn=urn, body=body)
    fiware.printResponse(rsp)
    #fiware.printJsonString(body)

def main():
    print("update sensor values (temperature) for orion")
    temperature = 10
    for idx in range(0, 9, 1):
        temperature+=1
        updateSensorTemperature(temperature)
        print("wait")
        time.sleep(3)

if __name__=='__main__':
    main()

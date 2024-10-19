import os
import configparser
from FiwareAPI import *
import time

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

ORION = 'http://{}:1026'.format(config_ini['DEFAULT']['HOST_IP'])
QUANTUMLEAP = 'http://{}:8668'.format(config_ini['DEFAULT']['HOST_IP'])
WEBSERVER = 'http://{}:8080'.format(config_ini['DEFAULT']['HOST_IP'])


SERVICE = 'service1'
SERVICEPATH = '/servicepath1'

URN  = "urn:ngsi-ld:Sensor:001"
TYPE = "Sensor"

def updateSensorTemperature(temperature):
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

    query = {'type' : TYPE}
    body = str(temperature)
    urn = URN+"/attrs/temperature/value"
    [rsp, body] = fiware.putEntities(query=query, urn=urn, body=body)
    print("resp : ", rsp)
    fiware.printJsonString(body)

def main():
    print("update sensor values (temperature) for orion")
    temperature = 10
    for idx in range(0, 9, 1):
        temperature+=1
        updateSensorTemperature(temperature)
        print("wait")
        print("confirm the WebServer log.")
        time.sleep(3)



if __name__=='__main__':
    main()

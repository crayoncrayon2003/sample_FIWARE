import os
import configparser
import random
from FiwareAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

ORION1 = 'http://{}:1026'.format(config_ini['DEFAULT']['HOST_IP'])

SERVICE = 'service1'            # multi-tenant name
SERVICEPATH = '/servicepath1'   # data storage path

URN  = "urn:ngsi-ld:Sensor:001" # data identifier
TYPE = "Sensor"                 # data type

def updateSensorAll():
    fiware = FiwareAPI(ORION1,SERVICE,SERVICEPATH)

    body = {
        "temperature": { "type": "Integer", "value": random.randint(50, 100), "metadata": {} },
        "humidity":    { "type": "Integer", "value": random.randint(50, 100),    "metadata": {} }
    }
    query = {'type' : TYPE}
    urn = URN+"/attrs/"
    [rsp, body] = fiware.patchEntities(query=query, urn=urn, body=body)
    fiware.printResponse(rsp)
    # fiware.printJsonString(body)

def main():
    print("update sensor values (temperature and humidity) for orion")
    updateSensorAll()


if __name__=='__main__':
    main()

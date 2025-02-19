import os
import configparser
import random
from FiwareAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

ORION1 = 'http://{}:1026'.format(config_ini['DEFAULT']['HOST_IP'])

SERVICE = 'service4'            # multi-tenant name
SERVICEPATH = '/servicepath4'   # data storage path

URN  = "urn:ngsi-ld:Sensor:*"  # data identifier
TYPE = "Sensor"                 # data type

def getSensor():
    fiware = FiwareAPI(ORION1,SERVICE,SERVICEPATH)

    query = {
        'type' : TYPE,
        'limit': 100,
        'idPattern': URN
    }

    [rsp, body] = fiware.getEntities(query=query)
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def main():
    print("make a storage area in orion to store sensor values (temperature and humidity).")
    getSensor()

if __name__=='__main__':
    main()

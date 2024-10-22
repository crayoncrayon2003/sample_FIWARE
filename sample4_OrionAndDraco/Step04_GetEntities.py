import os
import configparser
from FiwareAPI import *
import datetime
import time

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

ORION = 'http://{}:1026'.format(config_ini['DEFAULT']['HOST_IP'])

SERVICE = 'service1'            # multi-tenant name
SERVICEPATH = '/servicepath1'   # data storage path

URN  = "urn:ngsi-ld:Sensor:001" # data identifier
TYPE = "Sensor"                 # data type

def main():
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

    query = {'type' : TYPE}
    urn = URN

    for i in range(6):
        [rsp, body] = fiware.getEntities(query=query, urn=urn)
        fiware.printResponse(rsp)
        fiware.printJsonString(body)
        print(datetime.datetime.now())
        time.sleep(5)

if __name__=='__main__':
    main()

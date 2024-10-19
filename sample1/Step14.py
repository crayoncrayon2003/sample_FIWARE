import os
import configparser
from FiwareAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

ORION = 'http://{}:1026'.format(config_ini['DEFAULT']['HOST_IP'])
QUANTUMLEAP = 'http://{}:8668'.format(config_ini['DEFAULT']['HOST_IP'])
WEBSERVER = 'http://{}:8080'.format(config_ini['DEFAULT']['HOST_IP'])

SERVICE = 'service1'
SERVICEPATH = '/servicepath1'

URN  = "urn:ngsi-ld:Sensor:001"
TYPE = "Sensor"

def getHistory():
    fiware = FiwareAPI(QUANTUMLEAP,SERVICE,SERVICEPATH)

    query = {
        'type' : TYPE,
        'limit': 100
    }
    urn = URN
    [rsp, body] = fiware.getEntities(query=query, urn=urn)
    fiware.printResponse(rsp)
    fiware.printJsonString(body)


def main():
    print("get time series sensor values (temperature and humidity) from quantumleap")
    getHistory()

    print("Time series data exist.")


if __name__=='__main__':
    main()

import os
import configparser
from FiwareAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

ORION = 'http://{}:1026'.format(config_ini['DEFAULT']['HOST_IP'])
CYGNUS         = 'http://{}:5080'.format(config_ini['DEFAULT']['HOST_IP'])
CYGNUS_MYSQL   = 'http://{}:5050'.format(config_ini['DEFAULT']['HOST_IP'])
CYGNUS_MONGO   = 'http://{}:5051'.format(config_ini['DEFAULT']['HOST_IP'])
CYGNUS_CKAN    = 'http://{}:5052'.format(config_ini['DEFAULT']['HOST_IP'])
CYGNUS_HDFS    = 'http://{}:5053'.format(config_ini['DEFAULT']['HOST_IP'])
CYGNUS_CARTO   = 'http://{}:5054'.format(config_ini['DEFAULT']['HOST_IP'])
CYGNUS_POSTGRE = 'http://{}:5055'.format(config_ini['DEFAULT']['HOST_IP'])
CYGNUS_ORION   = 'http://{}:5050'.format(config_ini['DEFAULT']['HOST_IP'])
CYGNUS_POSTGIS = 'http://{}:5057'.format(config_ini['DEFAULT']['HOST_IP'])
CYGNUS_ELASTICSEARCH = 'http://{}:5058'.format(config_ini['DEFAULT']['HOST_IP'])
CYGNUS_ARCGIS  = 'http://{}:5059'.format(config_ini['DEFAULT']['HOST_IP'])
WEBSERVER = 'http://{}:8080'.format(config_ini['DEFAULT']['HOST_IP'])

SERVICE = 'service1'            # multi-tenant name
SERVICEPATH = '/servicepath1'   # data storage path

URN  = "urn:ngsi-ld:Sensor:001" # data identifier
TYPE = "Sensor"                 # data type

def setSubscriptions():
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

    body = {
        "description": "Notify Cygnus of all context changes",
        "subject": {
            "entities": [
                {
                    "id": URN,
                    "type": TYPE
                }
            ],
            "condition": {
                "attrs": [ "temperature", "humidity" ]
            },
        },
        "notification": {
            "http": {
                "url": CYGNUS_ORION+"/notify"
            },
            "attrs": [ "temperature", "humidity" ],
            "attrsFormat": "legacy"
        },
        "expires": "2025-12-31T00:00:00.000Z",
        "throttling": 1
    }
    [rsp, body] = fiware.postSubscriptions(body=body)
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def getSubscriptions():
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

    [rsp, body] = fiware.getSubscriptions()
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def deleteSubscriptions(id):
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

    urn = id
    [rsp, body] = fiware.deleteSubscriptions(urn=urn)
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def deleteSubscriptionsAll():
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

    [rsp, body] = fiware.getSubscriptions()
    # fiware.printResponse(rsp)
    # fiware.printJsonString(body)

    for item in json.loads(body):
        [rsp, body] = fiware.deleteSubscriptions(urn=item["id"])
        # fiware.printResponse(rsp)
        # fiware.printJsonString(body)


def main():
    # Initialize to avoid duplicate settings
    deleteSubscriptionsAll()

    print("settings to notify QUANTUMLEAP, when there is a change in the sensor value of ORION")
    setSubscriptions()
    print("get notify settings from ORION")
    getSubscriptions()


if __name__=='__main__':
    main()

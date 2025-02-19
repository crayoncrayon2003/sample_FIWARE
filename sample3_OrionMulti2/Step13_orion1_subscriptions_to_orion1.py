import os
import configparser
from FiwareAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

ORION1 = 'http://{}:1026'.format(config_ini['DEFAULT']['HOST_IP'])

FROM_SERVICE = 'service1'            # multi-tenant name
FROM_SERVICEPATH = '/servicepath1'   # data storage path

TO_SERVICE = 'service2'            # multi-tenant name
TO_SERVICEPATH = '/servicepath2'   # data storage path

URN  = "urn:ngsi-ld:Sensor:001" # data identifier
TYPE = "Sensor"                 # data type

def setSubscriptions():
    fiware = FiwareAPI(ORION1,FROM_SERVICE,FROM_SERVICEPATH)

    body = {
        "subject": {
            "entities": [
                {
                    "id": URN,
                    "type": TYPE
                }
            ],
            "condition": {
                "attrs": [],
                "notifyOnMetadataChange": True
            }
        },
        "notification": {
            "httpCustom": {
                "url": "http://orion1:1026/v2/op/update/",
                "headers": {
                    "Content-Type"      : "application/json",
                    "Fiware-Service"    : TO_SERVICE,
                    "Fiware-ServicePath": TO_SERVICEPATH
                },
                "method": "POST",
                "json":{
                    "actionType": "append",
                    "entities": [
                        {
                            "id"    : "${id}",
                            "type"  : "${type}",
                            "temperature": { "type": "Integer", "value": "${temperature}", "metadata": {} },
                            "humidity":    { "type": "Integer", "value": "${humidity}",    "metadata": {} }                            
                        }
                    ]
                },
            }
        },
    }
    [rsp, body] = fiware.postSubscriptions(body=body)
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def getSubscriptions():
    fiware = FiwareAPI(ORION1,FROM_SERVICE,FROM_SERVICEPATH)

    [rsp, body] = fiware.getSubscriptions()
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def deleteSubscriptions(id):
    fiware = FiwareAPI(ORION1,FROM_SERVICE,FROM_SERVICEPATH)

    urn = id
    [rsp, body] = fiware.deleteSubscriptions(urn=urn)
    fiware.printResponse(rsp)
    fiware.printJsonString(body)

def deleteSubscriptionsAll():
    fiware = FiwareAPI(ORION1,FROM_SERVICE,FROM_SERVICEPATH)

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

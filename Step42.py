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

URN  = "urn:ngsi-ld:Product:002"
TYPE = "Product"

def getProduct():
    fiware = FiwareAPI(ORION,SERVICE,SERVICEPATH)

    # ボディ作成
    query = {'type' : TYPE}
    urn = URN
    [rsp, body] = fiware.getEntities(query=query, urn=urn)
    print("resp : ", rsp)
    fiware.printJsonString(body)


def main():
    print("最新データを保持するORIONの商品データを取得します")
    getProduct()


if __name__=='__main__':
    main()

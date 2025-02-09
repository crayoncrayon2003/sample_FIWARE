import os
import configparser
from AuthzforceAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

KEYROCK = 'http://{}:8080'.format(config_ini['DEFAULT']['HOST_IP'])
# KEYROCK = 'http://localhost:3000'.format(config_ini['DEFAULT']['HOST_IP'])

keyrock = AuthzforceAPI(KEYROCK)

def postAuthzforceCeDomains():
    body = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><domainProperties xmlns="http://authzforce.github.io/rest-api-model/xmlns/authz/5" externalId="airplane"/>'
    [rsp, headers, body] = keyrock.postAuthzforceCeDomains(body=body)
    print(rsp)
    keyrock.printDict(headers)
    keyrock.printDict(body)
    # token = body["access_token"]

    return 


def main():
    access_token  = postAuthzforceCeDomains()



if __name__=='__main__':
    main()

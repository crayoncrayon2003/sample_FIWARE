import os
import configparser
from KeyrockAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

KEYROCK = 'http://{}:3000'.format(config_ini['DEFAULT']['HOST_IP'])
# KEYROCK = 'http://localhost:3000'.format(config_ini['DEFAULT']['HOST_IP'])

keyrock = KeyrockAPI(KEYROCK)

def getOauth2Token(grant_type, username, password, client_id, client_secret):
    body = {
        "grant_type"    : grant_type,
        "username"      : username,
        "password"      : password,
        "client_id"     : client_id,
        "client_secret" : client_secret
    }
    [rsp, headers, body] = keyrock.postOauth2Token(body=body)
    print(rsp)
    keyrock.printDict(headers)
    keyrock.printDict(body)
    token = body["access_token"]

    return [token]


def main():
    # get token
    grant_type    = "password"
    admin_name    = "admin@test.com"
    admin_pass    = "admin"
    client_id     = "a2e35826-296c-4978-9174-1a873597aff2"
    client_secret = "c182e5c5-153d-42c3-b652-97561e5496df"
    access_token  = getOauth2Token(grant_type, admin_name, admin_pass, client_id, client_secret)



if __name__=='__main__':
    main()

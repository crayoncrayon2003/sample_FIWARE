import os
import configparser
from KeyrockAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

KEYROCK = 'http://{}:3000'.format(config_ini['DEFAULT']['HOST_IP'])
# KEYROCK = 'http://localhost:3000'.format(config_ini['DEFAULT']['HOST_IP'])

keyrock = KeyrockAPI(KEYROCK)

def getToken(name, password):
    body = {
        "name": name,
        "password": password
    }
    [rsp, headers, body] = keyrock.postAuthTokens(body=body)
    print(rsp)
    keyrock.printDict(headers)
    keyrock.printDict(body)
    token = headers["X-Subject-Token"]

    # get token info
    header={
        "X-Auth-token"    : token, # my token
        "X-Subject-token" : token  # Obtain information about the specified token
    }
    [rsp, headers, body] = keyrock.getAuthTokens(header=header)
    print(rsp)
    keyrock.printDict(headers)
    keyrock.printDict(body)
    id = body["User"]["id"]

    return [id, token]

def getAllUser(token):
    header={
        "X-Auth-token"    : token
    }
    [rsp, headers, body] = keyrock.getUsers(header=header)
    print(rsp)
    keyrock.printDict(headers)
    keyrock.printDict(body)
    return body['users']

def getOneUser(token,id):
    header={
        "X-Auth-token"    : token
    }
    [rsp, headers, body] = keyrock.getUsers(header=header,path=id)
    print(rsp)
    keyrock.printDict(headers)
    keyrock.printDict(body)

def deleteUser(token,id):
    header={
        "X-Auth-token"    : token
    }
    [rsp, headers, body] = keyrock.deleteUsers(header=header,path=id)
    print(rsp)
    # keyrock.printDict(headers)
    # keyrock.printDict(body)

def createUser(token, user_name,user_pass,user_mail):
    header={
        "X-Auth-token"    : token
    }
    body = {
        "user": {
            "username"  : user_name,
            "password"  : user_pass,
            "email"     : user_mail
        }
    }
    [rsp, headers, body] = keyrock.postUsers(header=header, body=body)
    print(rsp)
    keyrock.printDict(headers)
    keyrock.printDict(body)

    id = None
    if (rsp!=False):
      id = body["user"]["id"]

    return id

def getAllOrganizations(token):
    header={
        "X-Auth-token"    : token
    }
    [rsp, headers, body] = keyrock.getOrganizations(header=header)
    print(rsp)
    keyrock.printDict(headers)
    keyrock.printDict(body)
    return body['organizations']

def getOneOrganizations(token,id):
    header={
        "X-Auth-token"    : token
    }
    [rsp, headers, body] = keyrock.getOrganizations(header=header,path=id)
    print(rsp)
    keyrock.printDict(headers)
    keyrock.printDict(body)

def deleteOrganizations(token,id):
    header={
        "X-Auth-token"    : token
    }
    [rsp, headers, body] = keyrock.deleteOrganizations(header=header,path=id)
    print(rsp)
    # keyrock.printDict(headers)
    # keyrock.printDict(body)

def createOrganizations(token):
    header={
        "X-Auth-token"    : token
    }
    body = {
        "organization": {
            "name": "Security",
            "description": "This group is for the store detectives"
        }
    }
    [rsp, headers, body] = keyrock.postOrganizations(header=header, body=body)
    print(rsp)
    keyrock.printDict(headers)
    keyrock.printDict(body)

    id = None
    if (rsp!=False):
      id = body["organization"]["id"]

    return id

def addUserOrganizations(token, org_id, user_id, org_role):
    header={
        "X-Auth-token"    : token
    }
    path = f'{org_id}/users/{user_id}/organization_roles/{org_role}'
    [rsp, headers, body] = keyrock.putOrganizations(header=header, path=path)
    print(rsp)
    keyrock.printDict(headers)
    keyrock.printDict(body)

def getUserOrganizations(token, org_id):
    header={
        "X-Auth-token"    : token
    }
    path = f'{org_id}/users/'
    [rsp, headers, body] = keyrock.getOrganizations(header=header, path=path)
    print(rsp)
    keyrock.printDict(headers)
    keyrock.printDict(body)

def deleteUserOrganizations(token, org_id, user_id, org_role):
    header={
        "X-Auth-token"    : token
    }
    path = f'{org_id}/users/{user_id}/organization_roles/{org_role}'
    [rsp, headers, body] = keyrock.deleteOrganizations(header=header, path=path)
    print(rsp)
    keyrock.printDict(headers)
    keyrock.printDict(body)

def main():
    # get token
    admin_name = "admin@test.com"
    admin_pass = "admin"
    [admin_id, admin_token] = getToken(admin_name, admin_pass)

    # create user
    userIDs= []
    user_name = "userX",
    user_pass = "userX"
    user_mail = "userX@example.com"
    user_id = createUser(admin_token, user_name,user_pass,user_mail)
    if(user_id != None):
        userIDs.append(user_id)

    # get all user
    users = getAllUser(admin_token)
    # get one user
    for user in users:
        getOneUser(admin_token, user['id'])

    # create Organizations
    orgIDs=[]
    org_id = createOrganizations(admin_token)
    if(org_id != None):
        orgIDs.append(org_id)

    # get all Organizations
    orgs = getAllOrganizations(admin_token)
    # get one Organizations
    for org in orgs:
        getOneOrganizations(admin_token, org['Organization']['id'])


    # add user to Organizations
    addUserOrganizations(admin_token, org_id, admin_id, 'owner')
    # addUserToOrganizations(admin_token, org_id, user_id, 'member')

    # get user from Organizations
    getUserOrganizations(admin_token, org_id)

    # delete user from Organizations
    deleteUserOrganizations(admin_token, org_id, user_id, 'owner')

    # delete user
    for userID in userIDs:
        deleteUser(admin_token, userID)

    # delete Organizations
    for orgID in orgIDs:
        deleteOrganizations(admin_token, orgID)

if __name__=='__main__':
    main()

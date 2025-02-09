
# How to Use
# Login
## GUI
* http://localhost:3000

## REST API
### login
'''
curl -iX POST http://localhost:3000/v1/auth/tokens -H 'Content-Type: application/json' -d '{ "name": "admin@test.com", "password": "1234"}'
'''

X-Subject-Token in the response header is a token
ex.
X-Subject-Token: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX

### get token info
X-Auth-token is authenticated token.
X-Subject-token is the token for which information is to be obtained.
'''
curl -iX GET http://localhost:3000/v1/auth/tokens -H 'Content-Type: application/json' -H 'X-Auth-token:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX' -H 'X-Subject-token:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
'''

### token Refresh
'''
curl -iX POST http://localhost:3000/v1/auth/tokens -H 'Content-Type:application/json' -d '{ "token": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"}'
'''

X-Subject-Token in the response header is new token
ex.
X-Subject-Token: YYYYYYYY-YYYY-YYYY-YYYY-YYYYYYYYYYYY


# Create User
## GUI
User -> Registration
* user name    : userX
* e-mail       : userX@test.com
* password     : userX
* discription  : ""
* send e-mail  : OFF
* enable       : ON

## REST API
'''
curl -iX POST 'http://localhost:3000/v1/users' -H 'Content-Type: application/json'  -H 'X-Auth-token:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX' -d '{ "user": { "username": "userX", "email": "userX@test.com","password": "userX" }}'
'''

user id in the response body
ex.
ZZZZZZZZ-ZZZZ-ZZZZ-ZZZZ-ZZZZZZZZZZZZ

## User Info
### GUI
User -> select user

### REST
#### get information for all users
'''
curl -X GET 'http://localhost:3000/v1/users' -H 'Content-Type:application/json' -H 'X-Auth-token:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
'''

#### get information for one user
'''
curl -X GET 'http://localhost:3000/v1/users/ZZZZZZZZ-ZZZZ-ZZZZ-ZZZZ-ZZZZZZZZZZZZ' -H 'Content-Type: application/json' -H 'X-Auth-token:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
'''

## Delete User
### GUI
User -> select user

### REST
'''
curl -iX DELETE http://localhost:3000/v1/users/ZZZZZZZZ-ZZZZ-ZZZZ-ZZZZ-ZZZZZZZZZZZZ -H 'Content-Type:application/json' -H 'X-Auth-token:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
'''

# organizations
## Create organizations
### GUI
organizations -> Registration
* name :
* discription :

### REST
'''
curl -iX POST 'http://localhost:3000/v1/organizations' -H 'Content-Type:application/json'  -H 'X-Auth-token:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX' -d '{ "organization": { "name": "Security", "description": "This group is for the store detectives"}}'
'''

## Get organizations
### GUI
organizations -> select organizations

### REST API
#### get information for all organizations
'''
curl -X GET 'http://localhost:3000/v1/organizations' -H 'Content-Type:application/json' -H 'X-Auth-token:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
'''

#### get information for one organizations
'''
curl -X GET 'http://localhost:3000/v1/organizations/8bf6020a-0d57-47ab-acf5-4341ee4a2329' -H 'Content-Type:application/json' -H 'X-Auth-token:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
'''

## Delete organizations
### GUI
User -> select user

### REST API
'''
curl -iX DELETE 'http://localhost:3000/v1/organizations/WWWWWWWW-WWWW-WWWW-WWWW-WWWWWWWWWWWW' -H 'Content-Type: application/json' -H 'X-Auth-token:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
'''

## Adding Users to an Organization
### GUI
Organization -> Management
select users to be added to the organization

### REST
#### Adding users with user roles to the organization
'''
curl -iX PUT 'http://localhost:3000/v1/organizations/WWWWWWWW-WWWW-WWWW-WWWW-WWWWWWWWWWWW/users/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/organization_roles/member' -H 'Content-Type:application/json' -H 'X-Auth-token:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
'''

#### Adding users with owner roles to the organization
'''
curl -iX PUT 'http://localhost:3000/v1/organizations/WWWWWWWW-WWWW-WWWW-WWWW-WWWWWWWWWWWW/users/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/organization_roles/owner' -H 'Content-Type:application/json' -H 'X-Auth-token:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
'''

#### get users in the organization
'''
curl -X GET 'http://localhost:3000/v1/organizations/WWWWWWWW-WWWW-WWWW-WWWW-WWWWWWWWWWWW/users' -H 'Content-Type: application/json' -H 'X-Auth-token:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
'''

#### delete users in the organization
'''
curl -X DELETE 'http://localhost:3000/v1/organizations/WWWWWWWW-WWWW-WWWW-WWWW-WWWWWWWWWWWW/users/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/organization_roles/owner' -H 'Content-Type: application/json' -H 'X-Auth-token:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
'''

## Registration Application
### GUI
Application -> admin's apps
authorization -> Registration

* name                  ：OrionApp
* discription           ：this is orion client
* URL                   ：http://localhost
* Callback URL          ：http://localhost
* Sign-out Callback Url ：
* grant type            ：
  * Authorization Code  : On
  * Implicit            : Off
  * Resouce owner pass  : Off
  * Cliant Credencial   : Off
  * Refresh Token       : On
* provider              ：admin

Provider
* Get and assign only public owned roles          : on
* Get and assign all public application roles     : on
* Manage authorizations                           : on
* Manage roles                                    : on
* Manage the application                          : on
* Get and assign all internal application roles   : on

Purchaser
* Get and assign only public owned roles          : off
* Get and assign all public application roles     : on
* Manage authorizations                           : off
* Manage roles                                    : off
* Manage the application                          : off
* Get and assign all internal application roles   : off

Enable PEP Proxy

Edit Role -> Add Role
* role name : OrionUser

Edit Role -> OrionUser -> parmision
* parmision name : ReadOrion
* discription    ：
* HTTP action    : GET
* Resoce         : /v2/entities

# OAuth2 credentials
Application -> my-app -> OAuth2 credentials
Client ID    ：0d97b8d5-6e9e-4324-9928-3deada41a9c0
Client Secret：935a9a0e-b9ba-4e72-aef2-82bbcbf7f68e

#
## Add User
* username : user1
* e-maile  : user1@test.com
* password : user1


パーミッション名: ReadOrion
HTTP メソッド: GET
リソースパス: /v2/entities
ロールにパーミッションを割り当てる

OrionUser → ReadOrion を追加
ユーザーにロールを割り当てる

user1 → OrionUser

:を使って、[Client ID]:[Client Secret]で、Authorization キーをつくる
```
echo 0d97b8d5-6e9e-4324-9928-3deada41a9c0:935a9a0e-b9ba-4e72-aef2-82bbcbf7f68e | base64
```

curl -iX POST 'http://localhost:3000/oauth2/token' -H 'Accept: application/json' -H 'Authorization: Basic MGQ5N2I4ZDUtNmU5ZS00MzI0LTk5MjgtM2RlYWRhNDFhOWMwOjkzNWE5YTBlLWI5YmEtNGU3Mi1hZWYyLTgyYmJjYmY3ZjY4ZQ==' -H 'Content-Type: application/x-www-form-urlencoded' -d "username=admin@test.com&password=1234&grant_type=password"


'{ "name": "admin@test.com", "password": "1234"}'

# 認可コードのグラント 
/oauth/authorize?response_type=code&client_id={{client-id}}&state=xyz&redirect_uri={{callback_url}}

# 暗黙のグラント (Implicit Grant)
 /oauth/authorize?response_type=token&client_id={{client-id}}&state=xyz&redirect_uri={{callback_url}}

 アプリケーションとしてのログイン

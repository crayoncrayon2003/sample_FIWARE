import json
import requests

class FiwareAPI():
    def __init__(self, baseURL=None,Service=None,ServicePath=None,Type=None):
        if( baseURL==None):
            self.baseURL = 'http://0.0.0.0:1026'
        else:
            self.baseURL = baseURL
        self.SERVICE = Service
        self.SERVICEPATH = ServicePath
        self.HEADERS={}
        self.setFiwareService(Service)
        self.setFiwareServicePath(ServicePath)

    def setFiwareService(self, Service):
        self.HEADERS['Fiware-Service']=Service

    def setFiwareServicePath(self, ServicePath):
        self.HEADERS['Fiware-ServicePath']=ServicePath

    def printResponse(self,resp):
        print("REST API Response : ")
        print(resp)

    def printJsonString(self,body):
        print("REST API Body : ")
        try:
            print(json.dumps(json.loads(body), indent=2))
        except Exception as e:
            print("empty")

    def __makeURI(self, path, urn):
        uri = self.baseURL + path
        if((urn!=None) and (len(urn)!=0)):
            uri = self.baseURL + path + urn
        return uri

    def __httpReq(func):
        def wrapper(self, query=None, urn=None, body=None):
            [method, path, headers] = func(self)
            url = self.__makeURI(path, urn)

            if(body==None):
                response = requests.request(method, url=url, headers=headers, params=query, timeout=5)
            else:
                response = requests.request(method, url=url, headers=headers, params=query, data=json.dumps(body), timeout=5)

            return [response.ok, response.text]

        return wrapper

    # version
    @__httpReq
    def getVersion(self):
        path = "/version"
        return ["get", path, None]

    # statistics
    @__httpReq
    def getStatistics(self):
        path = "/statistics"
        return ["get", path, None]

    @__httpReq
    def deleteStatistics(self):
        path = "/statistics"
        return ["delete", path, None]

    @__httpReq
    def getCacheStatistics(self):
        path = "/cache/statistics"
        return ["get", path, None]

    @__httpReq
    def deleteCacheStatistics(self):
        path = "/cache/statistics"
        return ["delete", path, None]

    # log
    @__httpReq
    def getAdminLog(self):
        path = "/admin/log"
        return ["get", path, None]

    @__httpReq
    def putAdminLog(self):
        path = "/admin/log"
        return ["put", path, None]

    # entities
    @__httpReq
    def postEntities(self):
        path = "/v2/entities/"
        headers = self.HEADERS
        headers['Content-Type'] = 'application/json'

        return ["post", path, headers]

    @__httpReq
    def putEntities(self):
        path = "/v2/entities/"
        headers = self.HEADERS
        headers['Content-Type'] = 'text/plain'

        return ["put", path, headers]

    @__httpReq
    def patchEntities(self):
        path = "/v2/entities/"
        headers = self.HEADERS
        headers['Content-Type'] = 'application/json'

        return ["patch", path, headers]

    @__httpReq
    def getEntities(self):
        path = "/v2/entities/"
        headers = self.HEADERS
        headers['Accept'] = 'application/json'

        return ["get", path, headers]

    # types
    @__httpReq
    def getTypes(self):
        path = "/v2/types/"
        headers = self.HEADERS
        headers['Accept'] = 'application/json'

        return ["get", path, headers]

    # subscriptions
    @__httpReq
    def getSubscriptions(self):
        path = "/v2/subscriptions/"
        headers = self.HEADERS
        headers['Accept'] = 'application/json'

        return ["get", path, headers]

    @__httpReq
    def postSubscriptions(self):
        path = "/v2/subscriptions/"
        headers = self.HEADERS
        headers['Content-Type'] = 'application/json'

        return ["post", path, headers]

    @__httpReq
    def deleteSubscriptions(self):
        path = "/v2/subscriptions/"
        headers = self.HEADERS

        return ["delete", path, headers]

    # registrations
    @__httpReq
    def getRegistrations(self):
        path = "/v2/registrations/"
        headers = self.HEADERS
        headers['Accept'] = 'application/json'

        return ["get", path, headers]

    @__httpReq
    def postRegistrations(self):
        path = "/v2/registrations/"
        headers = self.HEADERS
        headers['Content-Type'] = 'application/json'

        return ["post", path, headers]

    @__httpReq
    def deleteRegistrations(self):
        path = "/v2/registrations/"
        headers = self.HEADERS

        return ["delete", path, headers]

    # op/update
    @__httpReq
    def postUpdate(self):
        path = "/v2/op/update/"
        headers = self.HEADERS
        headers['Content-Type'] = 'application/json'

        return ["post", path, headers]

    # op/query
    @__httpReq
    def postOpQuery(self):
        path = "/v2/op/query/"
        headers = self.HEADERS
        headers['Content-Type'] = 'application/json'

        return ["post", path, headers]

    # op/notify
    @__httpReq
    def postNotify(self):
        path = "/v2/op/notify/"
        headers = self.HEADERS
        headers['Content-Type'] = 'application/json'

        return ["post", path, headers]


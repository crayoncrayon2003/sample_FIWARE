import json
import requests

class KongAPI():
    def __init__(self, baseURL):
        self.baseURL = baseURL

        __HEADERS={
        }
        __METHODS_TABLE = {
            # method name   : return value
            "getServices"   : lambda self: ["/services",  "get",     {**__HEADERS, **{'Content-Type':'application/json'}}],
            "postServices"  : lambda self: ["/services",  "post",    {**__HEADERS, **{'Content-Type':'application/json'}}],
            "getRoutes"     : lambda self: ["/routes",    "get",     {**__HEADERS, **{'Content-Type':'application/json'}}],
            "postRoutes"    : lambda self: ["/routes",    "post",    {**__HEADERS, **{'Content-Type':'application/json'}}],
            "getPlugins"    : lambda self: ["/plugins",   "get",     {**__HEADERS, **{'Content-Type':'application/json'}}],
            "postPlugins"   : lambda self: ["/plugins",   "post",    {**__HEADERS, **{'Content-Type':'application/json'}}],
        }

        for name, method in __METHODS_TABLE.items():
            # setting decorator to method
            decorated_method = self.__httpReq(method)
            # setting method to class
            setattr(self.__class__, name, decorated_method)

    def printDict(self,temp):
        print("printDict")
        try:
            print(json.dumps(temp, indent=2))
        except Exception as e:
            print("empty")

    def printString(self,temp):
        print("printString")
        try:
            print(json.dumps(json.loads(temp), indent=2))
        except Exception as e:
            print("empty")

    def saveJson(self,path, body):
        try:
            with open(path, 'w') as f:
                json.dump(body, f, indent=2)
        except Exception as e:
            print("empty")

    # Decorator for each method
    def __httpReq(self, func):
        def makeURI(paths, path):
            ret = self.baseURL + paths
            if( path != None ):
                ret = self.baseURL + paths + "/" + path
            return ret

        def makeHeaders(headers, header):
            ret = headers
            if(header != None):
                ret = headers | header
            return ret

        def wrapper(*args, **kwargs):
            # get param
            header = kwargs.get('header')
            path = kwargs.get('path')
            query = kwargs.get('query')
            body = kwargs.get('body')

            # call method of __METHODS_TABLE
            [paths, method, headers] = func(self)

            paths   = makeURI(paths, path)
            headers = makeHeaders(headers, header)

            # call REST API
            if(body==None):
                response = requests.request(method, url=paths, headers=headers, params=query, timeout=5)
            else:
                response = requests.request(method, url=paths, headers=headers, params=query, data=json.dumps(body), timeout=5)

            headers = dict(response.headers)
            try:
                body = response.json()
            except ValueError:
                body = {}

            return [response.ok, headers, body]

        return wrapper

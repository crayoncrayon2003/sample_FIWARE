import json
import requests

class FiwareAPI():
    def __init__(self, baseURL,Service,ServicePath):
        self.baseURL = baseURL

        __HEADERS={
            'Fiware-Service'    : Service,
            'Fiware-ServicePath': ServicePath
        }
        __METHODS_TABLE = {
            # method name                           : return value
            "getVersion"                            : lambda self: ["/version",                                 "get",     None],
            "getStatistics"                         : lambda self: ["/statistics",                              "get",     None],
            "deleteStatistics"                      : lambda self: ["/statistics",                              "delete",  None],
            "getCacheStatistics"                    : lambda self: ["/cache/statistics",                        "get",     None],
            "deleteCacheStatistics"                 : lambda self: ["/cache/statistics",                        "delete",  None],
            "getAdminLog"                           : lambda self: ["/admin/log",                               "get",     None],
            "putAdminLog"                           : lambda self: ["/admin/log",                               "put",     None],
            "getEntities"                           : lambda self: ["/v2/entities/",                            "get",     {**__HEADERS, **{'Accept'      :'application/json'}} ],
            "postEntities"                          : lambda self: ["/v2/entities/",                            "post",    {**__HEADERS, **{'Content-Type':'application/json'}} ],
            "putEntities"                           : lambda self: ["/v2/entities/",                            "put",     {**__HEADERS, **{'Content-Type':'text/plain'      }} ],
            "patchEntities"                         : lambda self: ["/v2/entities/",                            "patch",   {**__HEADERS, **{'Content-Type':'application/json'}} ],
            "getTypes"                              : lambda self: ["/v2/types/",                               "get",     {**__HEADERS, **{'Accept'      :'application/json'}} ],
            "getSubscriptions"                      : lambda self: ["/v2/subscriptions/",                       "get",     {**__HEADERS, **{'Accept'      :'application/json'}} ],
            "postSubscriptions"                     : lambda self: ["/v2/subscriptions/",                       "post",    {**__HEADERS, **{'Content-Type':'application/json'}} ],
            "deleteSubscriptions"                   : lambda self: ["/v2/subscriptions/",                       "delete",  __HEADERS, ],
            "getRegistrations"                      : lambda self: ["/v2/registrations/",                       "get",     {**__HEADERS, **{'Accept'      :'application/json'}} ],
            "postRegistrations"                     : lambda self: ["/v2/registrations/",                       "post",    {**__HEADERS, **{'Content-Type':'application/json'}} ],
            "deleteRegistrations"                   : lambda self: ["/v2/registrations/",                       "delete",  __HEADERS, ],
            "postOpUpdate"                          : lambda self: ["/v2/op/update/",                           "post",    {**__HEADERS, **{'Content-Type':'application/json'}} ],
            "postOpQuery"                           : lambda self: ["/v2/op/query/",                            "post",    {**__HEADERS, **{'Content-Type':'application/json'}} ],
            "postOpNotify"                          : lambda self: ["/v2/op/notify/",                           "post",    {**__HEADERS, **{'Content-Type':'application/json'}} ],
            "postNotify"                            : lambda self: ["/v2/notify",                               "post",    {**__HEADERS, **{'Content-Type':'application/json'}} ],
            "getHealth"                             : lambda self: ["/health",                                  "get",     {**__HEADERS, **{'Accept'      :'application/json'}} ],
            "postSubscribe"                         : lambda self: ["/v2/subscribe",                            "post",    {**__HEADERS, **{'Content-Type':'application/json'}} ],
            "postManagementConfig"                  : lambda self: ["/management/config/",                      "post",    {**__HEADERS, **{'Content-Type':'application/json'}} ],
            "getManagementQueueNotifications"       : lambda self: ["/management/queue/notifications",          "get",     {**__HEADERS, **{'Accept'      :'application/json'}} ],
            "deleteManagementQueueNotifications"    : lambda self: ["/management/queue/notifications",          "delete",  {**__HEADERS, **{'Content-Type':'application/json'}} ],
            "getManagementQueueNotificationsSummary": lambda self: ["/management/queue/notifications/summary",  "get",     {**__HEADERS, **{'Accept'      :'application/json'}} ],
            "getManagementQueueNotificationsCount"  : lambda self: ["/management/queue/notifications/count",    "get",     {**__HEADERS, **{'Accept'      :'application/json'}} ],
        }

        for name, method in __METHODS_TABLE.items():
            # setting decorator to method
            decorated_method = self.__httpReq(method)
            # setting method to class
            setattr(self.__class__, name, decorated_method)

    def printResponse(self,resp):
        print("REST API Response : ")
        print(resp)

    def printJsonString(self,body):
        print("REST API Response Body : ")
        try:
            print(json.dumps(json.loads(body), indent=2))
        except Exception as e:
            print("empty")

    # Decorator for each method
    def __httpReq(self, func):
        def makeURI(path, urn):
            uri = self.baseURL + path
            if((urn!=None) and (len(urn)!=0)):
                uri = self.baseURL + path + urn
            return uri

        def wrapper(*args, **kwargs):
            # get param
            query = kwargs.get('query')
            urn = kwargs.get('urn')
            body = kwargs.get('body')

            # call method of __METHODS_TABLE
            [path, method, headers] = func(self)
            url = makeURI(path, urn)

            # call REST API
            if(body==None):
                response = requests.request(method, url=url, headers=headers, params=query, timeout=5)
            else:
                response = requests.request(method, url=url, headers=headers, params=query, data=json.dumps(body), timeout=5)

            return [response.ok, response.text]

        return wrapper

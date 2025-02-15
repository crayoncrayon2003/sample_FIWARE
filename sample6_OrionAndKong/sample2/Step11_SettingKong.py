import os
import configparser
from KongAPI import *

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

ORION = 'http://orion1:1026'
# KONG = 'http://{}:8001'.format(config_ini['DEFAULT']['HOST_IP'])
KONG = 'http://localhost:8001'
kong  = KongAPI(KONG)

def makePreFunctionPluginForPOST(routesID):
    body = {
        "name": "pre-function",
        "route": {"id": routesID},
        "config": {
            "access": [
                """
                local cjson = require "cjson"
                local req_method = kong.request.get_method()

                -- Only apply check for POST method
                if req_method == "POST" then
                    local req_body = kong.request.get_raw_body()

                    if req_body then
                        local data = cjson.decode(req_body)
                        -- Check if the 'type' is 'location' in POST request body
                        if data.type ~= "location" then
                            kong.response.set_status(400)
                            kong.response.set_body(cjson.encode({
                                error = "Invalid type: Only 'location' is allowed in POST request",
                                received_body = req_body
                            }))
                            return kong.response.send()
                        end
                    else
                        kong.response.set_status(400)
                        kong.response.set_body(cjson.encode({
                            error = "Request body is empty",
                            received_body = req_body
                        }))
                        return kong.response.send()
                    end
                end
                """
            ]
        }
    }

    [rsp, headers, body] = kong.postPlugins(body=body)
    kong.printDict(rsp)
    kong.printDict(headers)
    kong.printDict(body)


def makePostFunctionPluginForGET(routesID):
    body = {
        "name": "post-function",
        "route": {"id": routesID},
        "config": {
            "access": [
                """
                local cjson = require "cjson"
                local req_method = kong.request.get_method()

                -- Only apply check for GET method
                if req_method == "GET" then
                    local res_body = kong.response.get_raw_body()

                    if res_body then
                        local data = cjson.decode(res_body)
                        -- Check if the 'type' is 'location' in GET response body
                        if data.type ~= "location" then
                            kong.response.set_status(400)
                            kong.response.set_body(cjson.encode({
                                error = "Invalid type in response: Only 'location' is allowed",
                                received_body = res_body
                            }))
                            return kong.response.send()
                        end
                    else
                        kong.response.set_status(400)
                        kong.response.set_body(cjson.encode({
                            error = "Response body is empty",
                            received_body = res_body
                        }))
                        return kong.response.send()
                    end
                end
                """
            ]
        }
    }

    [rsp, headers, body] = kong.postPlugins(body=body)
    kong.printDict(rsp)
    kong.printDict(headers)
    kong.printDict(body)



def main():
    services_name_orion = "orion-service"
    routes_name_orion_v2entities = "v2_entities"

    # make services
    body = {
        "name" : services_name_orion,
        "url"  : "http://orion1:1026"
    }
    [rsp, headers, body] = kong.postServices(body=body)
    kong.printDict(rsp)
    kong.printDict(headers)
    kong.printDict(body)

    # get services
    [rsp, headers, body] = kong.getServices(path=services_name_orion)
    kong.printDict(rsp)
    kong.printDict(headers)
    kong.printDict(body)
    services_id_orion = body["id"]

    # make routes
    body = {
        "service": {
            "id": services_id_orion
        },
        "name": routes_name_orion_v2entities,
        "hosts": ["localhost"],
        "paths": ["/sample1-api"],
        "methods": ["POST", "GET", "PUT", "PATCH", "DELETE"],
        "path_handling": "v1",
        "protocols": ["http"]
    }
    [rsp, headers, body] = kong.postRoutes(body=body)
    kong.printDict(rsp)
    kong.printDict(headers)
    kong.printDict(body)

    # get routes
    [rsp, headers, body] = kong.getRoutes(path=routes_name_orion_v2entities)
    kong.printDict(rsp)
    kong.printDict(headers)
    kong.printDict(body)
    routes_id_orion_v2entities = body["id"]

    # setting Plugin
    # makePreFunctionPluginForPOST(routes_id_orion_v2entities)
    # makePostFunctionPluginForGET(routes_id_orion_v2entities)

if __name__=='__main__':
    main()



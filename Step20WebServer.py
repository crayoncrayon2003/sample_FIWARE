import os
import configparser
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import random

config_ini = configparser.ConfigParser()
config_ini.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"), encoding='utf-8')

class HTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        ###############################################################################################
        # RX HTTP request data
        parsed_path = urlparse(self.path)
        print(parsed_path.path)
        print(parse_qs(parsed_path.query))
        print(self.headers)
        req_body = self.rfile.read(int(self.headers['content-length'])).decode('utf-8')
        dct_body = json.loads(req_body)
        print(json.dumps(dct_body, indent=2))

        ###############################################################################################
        # TX HTTP response data
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        if "subscriptionId" in req_body :
            # receiving Subscription notifications from Orion
            # this case, data transfer is Orion to WebServer
            pass
        elif "entities" in req_body :
            # receiving Registrations notifications from Orion
            # this case, data transfer is WebServer to Orion
            rsp_body=[]
            for item in dct_body['entities']:
                tmp = {
                    "id": item['id'],
                    "type": item['type'],
                    "value":{
                        "type":"Integer",
                        "value": random.randint(50, 100)
                    }
                }
                rsp_body.append(tmp)
            print(rsp_body)
            self.wfile.write( json.dumps(rsp_body).encode('utf-8') )

if __name__ == "__main__":
    print("Start the Web server.")
    print("Keep it running and proceed to the next step.")

    server = HTTPServer((config_ini['DEFAULT']['HOST_IP'], 8080), HTTPHandler)

    server.serve_forever()

from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import random
import logging

HOST = '0.0.0.0'
PORT = 8080

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# setting docker handler to logger
handler_docker = logging.FileHandler(filename="/proc/1/fd/1")
handler_docker.setFormatter(logging.Formatter("%(asctime)s %(threadName)s %(levelname)8s %(message)s"))
logger.addHandler(handler_docker)

class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logger.info('this is GET')
        ###############################################################################################
        # RX HTTP request data
        parsed_path = urlparse(self.path)
        logger.info(parsed_path.path)
        logger.info(parse_qs(parsed_path.query))
        logger.info(self.headers)
        req_body = self.rfile.read(int(self.headers['content-length'])).decode('utf-8')
        dct_body = json.loads(req_body)
        logger.info(json.dumps(dct_body, indent=2))

        ###############################################################################################
        self.send_response(200)
        self.end_headers()


    def do_POST(self):

        ###############################################################################################
        # RX HTTP request data
        parsed_path = urlparse(self.path)
        logger.info(parsed_path.path)
        logger.info(json.dumps(parse_qs(parsed_path.query)))
        logger.info(str(self.headers))
        req_body = self.rfile.read(int(self.headers['content-length'])).decode('utf-8')
        dct_body = json.loads(req_body)
        logger.info(json.dumps(dct_body, indent=2))

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
            logger.info(rsp_body)
            self.wfile.write( json.dumps(rsp_body).encode('utf-8') )

if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), HTTPHandler)
    server.serve_forever()

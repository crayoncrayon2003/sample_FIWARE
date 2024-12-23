from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import random
import logging

HOST = '0.0.0.0'
PORT = 8081

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# setting docker handler to logger
handler_docker = logging.FileHandler(filename="/proc/1/fd/1")
handler_docker.setFormatter(logging.Formatter("%(asctime)s %(threadName)s %(levelname)8s %(message)s"))
logger.addHandler(handler_docker)

class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        ###############################################################################################
        # RX HTTP request data
        parsed_path = urlparse(self.path)
        print(parsed_path.path)
        print(parse_qs(parsed_path.query))
        print(self.headers)

        ###############################################################################################
        # TX HTTP response data
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        body = {
            "temperature": random.randint(50, 100),
            "humidity"   : random.randint(50, 100)
        }
        print(body)
        self.wfile.write( json.dumps(body).encode('utf-8') )


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), HTTPHandler)
    server.serve_forever()

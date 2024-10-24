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
    counter = 0
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

if __name__ == "__main__":
    print("Start the Web server.")
    print("Keep it running and proceed to the next step.")

    server = HTTPServer((config_ini['DEFAULT']['HOST_IP'], 8081), HTTPHandler)

    server.serve_forever()

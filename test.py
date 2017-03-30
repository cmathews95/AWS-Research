#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import random

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        loop = int(argv[2])
        for i in range(0,loop):
            for j in range(0,loop):
                rand = i * j
        self._set_headers()

        
        new = 'Good'
        data = "<html><body><h1>"
        data += new
        data += "</h1></body></html>"
        self.wfile.write(data)

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Started httpd server...'
    try:
        httpd.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()

if __name__ == "__main__":
    from sys import argv

    if len(argv) >= 2:
        run(port=int(argv[1]))
    else:
        run()

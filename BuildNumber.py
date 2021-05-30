from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import os
from urllib.parse import urlparse

class NumberServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        
        update = 'n'

        query = urlparse(self.path).query
        if query:
            query_components = dict(qc.split("=") for qc in query.split("&"))
            update = query_components["update"]

        # Try and open number file and read number
        try:
            index = self.path.index("?")-1 if self.path.find("?") != -1 else len(self.path)
            fname = os.path.join("data", self.path[1:1+index] + "_releasenumber.txt")
            f = open(fname, "r")
            number = int(f.read())
            f.close()
        except (IOError, ValueError):
            # if we fail then just assume 0
            number = 0

        # send the number to the client
        result = number+1 if update == 'y' else number
        self.wfile.write(str(result).encode(encoding='utf_8'))
        
        if update == 'y':
            # write incremented number back to file
            try:
                f = open(fname, "w")
                numb = str(number+1)
                f.write(numb)
                f.close()
            except (IOError, ValueError):
                print ('Error')

    def do_HEAD(self):
        self._set_headers()

def run(server_class=HTTPServer, handler_class=NumberServer, port=80):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting number server...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    print (len(argv))
    print (argv[1])

    if len(argv) > 2:
        run(port=int(argv[1]))
    else:
        run()

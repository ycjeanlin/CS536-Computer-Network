from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import sys
import thread

class HttpS(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>Hello World</h1></body></html>")

def run(server_class=HTTPServer, handler_class=HttpS, port = 1119):
    server_addr = ('127.0.0.1', port)
    httpd = server_class(server_addr, handler_class)
    print 'Server is running...'
    httpd.serve_forever()

if __name__ == '__main__':
    run(port=int(sys.argv[1]))


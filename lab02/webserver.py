from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
#import thread


class SimpleServer(BaseHTTPRequestHandler):

    def _set_headers(self, file):
        self.send_response(200)
        if file.split('.')[-1] == 'jpeg':
            self.send_header('Content-type','image/jpeg')
        elif file.split('.')[-1] == 'gif':
            self.send_header('Content-type', 'image/gif')
        else:
            self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        try:
            self.root_path = './Upload'

            if self.path == '/':
                self.path = '/index.html'

            fr = open(self.root_path + self.path, 'rb')
            self._set_headers(self.path)

            self.wfile.write(bytes(fr.read()))
            fr.close()

            return
        except IOError:
            self.send_error(404, 'File not found')




def run(server_class=HTTPServer, handler_class=SimpleServer, port = 1119):
    server_addr = ('127.0.0.1', port)
    httpd = server_class(server_addr, handler_class)
    print('Server is running...')
    httpd.serve_forever()


if __name__ == '__main__':
    run(port=int(sys.argv[1]))


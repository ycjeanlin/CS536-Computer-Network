import socket
import sys
import threading
import time
import os

class SimpleServer:

    def __init__(self, server_ip, server_port):
        self.root_path = './Upload'
        self.ip = server_ip
        self.port = server_port

    def active_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.sock.bind((self.ip, self.port))
            print('Server Active...')
        except Exception:
            print('ERROR: Failed to bind sockets for {}:{}'.format(self.ip, self.port))
            self.shutdown()
            sys.exit(1)

        self._start_listen()

    def _start_listen(self):
        self.sock.listen(5)
        threads = []
        while True:
            connection, client_addr = self.sock.accept()
            t = threading.Thread(target=self._new_client_handler, args=(connection, client_addr))
            threads.append(t)
            t.start()

    def _new_client_handler(self, client_sock, client_addr):
        print('New client {}:{}'.format(client_addr[0], client_addr[1]))

        data = client_sock.recv(1024)
        request = bytes.decode(data)
        request_method = request.split(' ')[0]
        print("Method: ", request_method)
        print("Request body: ", request)

        if request_method == 'GET':
            request_file = request.split(' ')[1]
            self._do_get(request_file, client_sock)

        client_sock.close()

    def shutdown(self):
        self.sock.socket.shutdown(socket.SHUT_RDWR)
        print('Shutting down the server...')

    def _set_headers(self, code, file):
        server_header = ''
        if code == 200:
            server_header = 'HTTP/1.1 200 OK\r\n'
        elif code == 404:
            server_header = 'HTTP/1.1 404 Not Found\r\n'

        current_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        server_header += 'Date: {}\r\n'.format(current_time)
        server_header += 'Server: Simple-Server\r\n'
        server_header += 'Connection: close\r\n\r\n'

        #if (file.split('.')[-1] == 'jpeg' or file.split('.')[-1] == 'gif') and code == 200:
        #   server_header = ''
        return bytes(server_header, encoding='utf-8')

    def _check_permission(self, file_path):
        st = os.stat(file_path)
        return bool(st.st_mode)

    def _do_get(self, path, conn):
        response_content = b''
        try:
            if path == '/':
                path = '/index.html'

            permission = self._check_permission(self.root_path + path)

            if permission:
                fr = open(self.root_path + path, 'rb')
                response_content = fr.read()
                fr.close()
            conn.sendall(self._set_headers(200, path))
        except IOError:
            conn.sendall(self._set_headers(404, path))

        conn.sendall(response_content)


def main(server_ip, server_port):
    s = SimpleServer(server_ip, server_port)
    s.active_server()


if __name__ == '__main__':
    main('127.0.0.1', int(sys.argv[1]))



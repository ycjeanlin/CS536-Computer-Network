import socket
import sys


def main(server_ip, port, file_name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('Connecting to {}:{}'.format(server_ip, port))
    sock.connect((server_ip, port))

    if file_name == '/':
        file_name = '/index.html'

    try:
        request = 'GET {}'.format(file_name)

        sock.sendall(bytes(request, encoding='utf-8'))
        print('Requesting "{}"'.format(file_name))

        resp_data = b''
        while True:
            data = sock.recv(1024)
            if not data:
                break
            resp_data += data
        output_data = b''
        is_content = False
        for line in resp_data.split(b'\n'):
            if is_content:
                output_data += line
            if line == '':
                is_content = True
        print(resp_data)
        with open('./Download' + file_name, 'wb') as fw:
            fw.write(resp_data)

    finally:
        print('Close socket')
        sock.close()


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3])








import http.client
import sys

def main(server_ip, server_port, file_path):

    connect_server = http.client.HTTPConnection(server_ip, int(server_port))
    if file_path == '/':
        file_path = '/index.html'

    connect_server.request('GET', file_path)

    response = connect_server.getresponse()

    print(response.status, response.reason)
    rcv_data = response.read()
    with open('./Download/' + file_path, 'wb') as fw:
        fw.write(rcv_data)

    print(rcv_data)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])

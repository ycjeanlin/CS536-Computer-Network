import socket
import sys

if __name__ == '__main__':
    server_ip= sys.argv[1]
    port = int(sys.argv[2])


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print >> sys.stderr, 'Connecting to {}:{}'.format(server_ip, port)
    sock.connect((server_ip, port))

    try:
        while True:
            msg = raw_input('Enter message (enter "q" for disconnecting): ')
            if msg == 'q':
                sock.sendall(msg)
                break

            sock.sendall(msg)
            print >> sys.stderr, 'Sending "{}"'.format(msg)

            data = sock.recv(1024)
            print >> sys.stderr, 'Receiving "{}" from server {}:{}'.format(data, server_ip, port)

    finally:
        print >>sys.stderr, 'Close socket'
        sock.close()

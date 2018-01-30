import socket
import sys
import thread

def new_client_handler(client_sock, client_addr):
    print >>sys.stderr, 'New client {}:{}'.format(client_addr[0], client_addr[1])
    while True:
        msg = client_sock.recv(1024)
        if msg == 'q':
            break
        print >> sys.stderr, 'Message from [{}, {}]:{}'.format(client_addr[0], client_addr[1], msg)
        client_sock.sendall(msg)
        print >> sys.stderr, 'Sending message back to client {}:{}'.format(client_addr[0], client_addr[1])
    client_sock.close()

if __name__ == '__main__':
    ip_addr = '127.0.0.1'
    port = int(sys.argv[1])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip_addr, port))

    sock.listen(5)
    print >>sys.stderr, 'Server active...'

    while True:
        connection, client_addr = sock.accept()
        thread.start_new_thread(new_client_handler, (connection, client_addr))
            
    sock.close()

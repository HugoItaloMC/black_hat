import socket
from threading import Thread

from tests_handlers import test_client_handler

def socket_loop(target, port):
    global sa
    for res in socket.getaddrinfo(target, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
    else:
        try:
            server = socket.socket(af, socktype, proto)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(sa)
            server.listen(5)
            print('[*] - Listening only %s:%d' % sa)
            while True:
                client_socket, addr = server.accept()
                print('[*] - Accepted Connection only %s:%d' % (addr[0], addr[1]))
                threads = [(Thread(target=test_client_handler, args=(client_socket,)))]
                [thread.start() for thread in threads]

        except Exception as err:
            print('Error %s' % str(err))

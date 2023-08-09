import socket
import threading


class Netting:

    @staticmethod
    def socket_loop(target, port):
        for res in socket.getaddrinfo(target, port, socket.AF_UNSPEC,
                                      socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            af, socktype, proto, canonname, sa = res
        else:
            try:
                server = socket.socket(af, socktype, proto)
            except Exception as err:
                raise 'Error %s' % str(err)
            else:
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind(sa)
                server.listen(5)
                print('[*] - Listening only %s:%d' % sa)
                while True:
                    client, addr = server.accept()
                    print('[*] - Accpted Connection only %s:%d' % (addr[0], addr[1]))
                    threads = []
                    thread = threading.Thread(target=client_handler, args=(client,))
                    threads.append(thread)
                    for line in threads:
                        line.start()
                        line.join()

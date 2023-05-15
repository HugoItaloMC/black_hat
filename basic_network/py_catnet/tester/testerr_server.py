import socket
import sys


class Netting:
    def __getattr__(self, item):
        value = item
        setattr(self, item, value)
        return value

    def sockparser(self):
        raise NotImplementedError


class NettingServer(Netting):
    # The bind object from socket
    def __getattr__(self, item):
        return super().__getattr__(item)

    def sockparser(self):
        # Begin server bind in host from socket
        # Server create thread to client_socket
        if hasattr(self, 'target') and hasattr(self, 'port'):
            server = None
            for res in socket.getaddrinfo(self.target, self.port,
                                          socket.AF_UNSPEC,
                                          socket.SOCK_STREAM,
                                          0,
                                          socket.AI_PASSIVE):
                af, socktype, proto, canonname, sa = res
                try:
                    server = socket.socket(af, socktype, proto)
                except OSError as err:
                    server = None
                    continue
                try:
                    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    server.bind(sa)
                    server.listen(5)
                    print("[*] - Listening only %s:%d" % (self.target, self.port))
                except OSError as err:
                    server.close()
                    server = None

            if server is None:
                print('Not open socket')
                sys.exit()
            return server.accept()
        else:
            raise "Don't name to Attr"

if __name__ == '__main__':
    netting = NettingServer()
    netting.target = 'localhost'  # Atributo criado no ato da execucão
    netting.port = 9090  # Atributo críado no ato da execucão
    netting.sockparser()


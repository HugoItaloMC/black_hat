import socket


class Netting:
    def __init__(self):
        self.socket_by = socket
    def sockparser(self):
        raise NotImplementedError


class NettingServer(Netting):
    # The bind object from socket
    def __init__(self):
        super().__init__()
        self.target: str = str()  # The host to bind
        self.port: int = int()  # The port from host by bind away

    def sockparser(self):
        # Begin server bind in host from socket
        # Server create thread to client_socket

        server = self.socket_by.socket(self.socket_by.AF_INET, self.socket_by.SOCK_STREAM)
        server.setsockopt(self.socket_by.SOL_SOCKET, self.socket_by.SO_REUSEADDR, 1)
        server.bind((self.target, self.port))
        server.listen(5)
        print("[*] - Listening only %s:%d" % (self.target, self.port))
        return server.accept()


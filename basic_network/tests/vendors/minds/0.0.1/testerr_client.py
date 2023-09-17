import socket
import sys


class Netting:

    def __init__(self):
        self.sockopt = socket

    def __getattr__(self, item):
        value = item
        setattr(self, item, value)
        return value

    def sockparser(self):
        raise NotImplementedError


class NettingClient(Netting):
    # The sender object by socket
    def __init__(self):
        super().__init__()

    def __getattr__(self, item):
        return super().__getattr__(item)

    def sockparser(self, buffer):
        # Begin sender by client to host bind in socket
        client = None
        for res in socket.getaddrinfo(self.target, self.port,
                                      socket.AF_UNSPEC,
                                      socket.SOCK_STREAM,
                                      ):
            af, socktype, proto, canonname, sa = res
            try:
                client = socket.socket(af, socktype, proto)
            except OSError as err:
                client = None
                continue
            try:
                client.connect(sa)
            except OSError as err:
                client.close()
                continue
            break
        if client is None:
            print("Don't connected socket")
            sys.exit(1)

        with client:

            if len(buffer):
                client.sendall(buffer)
            while True:
                recv_len = 1
                response = b""
                while recv_len:
                    data = client.recv(4096)
                    recv_len = len(data)
                    response += data
                    if recv_len > 4096:
                        break
                response += data
                print(response,)

                buffer = input("Enter command: ")
                buffer += "\n"
                client.sendall(buffer.encode())


if __name__ == '__main__':
    client = NettingClient()
    client.target = 'localhost'
    client.port = 280
    buffer = b'Hello'
    client.sockparser(buffer)

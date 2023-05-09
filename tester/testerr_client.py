import socket



class Netting:

    def __init__(self):
        self.sockopt = socket
    def sockparser(self):
        raise NotImplementedError


class NettingClient(Netting):
    # The sender object by socket
    def __init__(self):
        super().__init__()
        self.target: str = str()  # Host bind to socket, again connection this client to send buffer
        self.port: int = int()  # Port by host from client

    def sockparser(self, buffer):
        # Begin sender by client to host bind socket
        client_socket = self.sockopt.socket(self.sockopt.AF_INET, self.sockopt.SOCK_STREAM)
        with client_socket:
            client_socket.connect((self.target, self.port))

            if len(buffer):
                client_socket.send(buffer.encode())
                while True:
                    response = b""
                    data = client_socket.recv(4096)

                    if not data:
                        break
                    response += data
                print(response,)

                buffer = input(b"Enter command: ")
                buffer += b"\n"
                client_socket.send(buffer)

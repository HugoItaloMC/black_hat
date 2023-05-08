import socket
from typing import Any


class Netting:

    def __init__(self):
        self.sockopt = socket
    def sockparser(self):
        raise NotImplementedError


class NettingClient(Netting):
    # The sender object by socket
    def __init__(self):
        super(__class__).__init__()
        self.target: str = str()  # Host bind to socket, again connection this client to send buffer
        self.port: int = int()  # Port by host from client

    def sockparser(self, buffer: Any):
        # Begin sender by client to host bind socket
        print("sockparser method implemented in `NettingClient`")



















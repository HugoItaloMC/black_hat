import socket
from test_parsers import Parser
from testerr_handler import ClientHandler


class Netting:
    def __init__(self):
        self.sockopt = socket
    def sockparser(self):
        raise NotImplementedError


class NettingServer(Netting):
    # The bind object from socket
    def __init__(self):
        super(__class__).__init__()
        self.target: str = str()  # The host to bind
        self.port: int = int()  # The port from host by bind away

    def sockparser(self):
        # Begin server bind in host from socket
        print("Is method sockparser implemented `NettingServer`")

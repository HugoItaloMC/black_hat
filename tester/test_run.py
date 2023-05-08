# know bahaviuor method `run`
import sys

from testerr_client import NettingClient
from testerr_server import NettingServer
from test_parsers import Parser

parser = Parser()


class Main:
    # The object to union
    def __init__(self):
        self.__server = NettingServer()
        self.__client = NettingClient()
        self.parser = parser.arg_parser()


    def _server(self):
        server = self.__server

        server.target = self.parser.targer
        server.port = int(self.parser.port)
        server.sockparser()

    def _client(self, buffer):
        client = self.__client
        client.target = self.parser.targer
        client.port = self.parser.port
        client.sockparser(buffer)

    def run(self):
        if self.parser.listen:
            return self._server()

        if not self.parser.listen and len(self.parser.targer) and int(self.parser.port) > 0:
            buffer = sys.stdin.read()
            return self._client(buffer)




if __name__ == '__main__':
    pycat = Main()
    pycat.run()  # Call server or/and client_sender

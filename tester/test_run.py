# know bahaviuor method `run`
import sys
import threading
from threading import Lock

from testerr_client import NettingClient
from testerr_server import NettingServer
from test_parsers import Parser
from testerr_handler import OptHandler
parser = Parser()
_handler = OptHandler()


class Main:
    # The object to union
    def __init__(self):
        self.__server = NettingServer()
        self.__client = NettingClient()
        self.parser = parser.arg_parser()
        self.lock = Lock()

    def _server(self):
        with self.lock:
            server = self.__server

            server.target = self.parser.targer
            server.port = int(self.parser.port)
            return server.sockparser()

    def _client(self, buffer):
        with self.lock:
            client = self.__client
            client.target = self.parser.targer
            client.port = int(self.parser.port)
            client.sockparser(buffer)

    def run(self):
        thread = []
        if self.parser.listen:
            server = self._server()
            while True:
                client_socker, addr = server[::1]
                print("[*] - Accepted connection from %s:%d" % (addr[0], addr[1]))
                threads = threading.Thread(target=_handler.client_handler, args=(client_socker,))
                threads.start()
                thread.append(threads)

        if not self.parser.listen and len(self.parser.targer) and int(self.parser.port) > 0:
            buffer = sys.stdin.read()
            threads = threading.Thread(target=self._client, args=(buffer,))
            threads.start()
            thread.append(threads)

        for line in thread:
            line.join()


if __name__ == '__main__':
    pycat = Main()
    pycat.run()  # Call server or/and client_sender

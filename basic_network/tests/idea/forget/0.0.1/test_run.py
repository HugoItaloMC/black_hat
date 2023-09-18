# know bahaviuor method `run`
import sys
import threading
from threading import Lock

from testerr_client import NettingClient, Netting
from testerr_server import NettingServer
from test_parsers import Parser
from testerr_handler import OptHandler


class Main(Netting):

    # The object to union

    def __init__(self):
        super().__init__()
        self.lock = Lock()
        self.__client = NettingClient()
        self.__server = NettingServer()
        self.__parser = Parser()

    def __getattr__(self, item):
        return super().__getattr__(item)

    def _server(self):
        with self.lock:
            server = self.__server
            parser = self.__parser.arg_parser()
            server.target = parser.targer
            server.port = int(parser.port)
            return server.sockparser()

    def _client(self, buffer):
        with self.lock:
            parser = Parser()
            parser = self.__parser.arg_parser()
            client = self.__client
            client.target = parser.targer
            client.port = int(parser.port)
            client.sockparser(buffer)

    def _handler(self):
        with self.lock:
            handler = OptHandler()
            parser = self.parser.arg_parser()
            handler.upload = parser.upload
            handler.execute = parser.execute
            handler.command = parser.command
            return handler

    def sockparser(self):
        thread = []
        parser = self.__parser.arg_parser()
        if parser.listen:
            server = self._server()
            client_socker, addr = server[::1]
            handler = self._handler()
            with client_socker:
                print("[*] - Accepted connection from %s:%d" % (addr[0], addr[1]))
                threads = threading.Thread(target=handler.client_handler, args=(client_socker,))
                threads.start()
                thread.append(threads)

        if not parser.listen and len(parser.targer) and int(parser.port) > 0:
            buffer = sys.stdin.read()
            threads = threading.Thread(target=self.client, args=(buffer,))
            threads.start()
            thread.append(threads)

        for line in thread:
            line.join()


if __name__ == '__main__':
    pycat = Main()
    pycat.sockparser()  # Call server or/and client_sender

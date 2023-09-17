import sys
from threading import Thread

from tests_parserargs import JoinParser
from tests_bind import socket_loop
from tests_handlers import test_client_handler, test_client_sender

args = JoinParser()


def manager():
    parser = args()

    if parser['listen']:
        threads = [Thread(target=socket_loop, args=(parser['target'], parser['port']))]
        [thread.start() for thread in threads]

    elif not parser['listen'] and len(parser['target']) and parser['port'] > 0:
        buffer = sys.stdin.read()
        threads = [(Thread(target=test_client_sender, args=(buffer.encode(),)))]
        [thread.start() for thread in threads]


if __name__ == '__main__':
    manager()

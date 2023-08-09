import threading
import sys
from tests_parserargs import JoinParser
from tests_bind import Netting

args = JoinParser()
bind = Netting


def test_port_target():
    print('..Running test method port target')


def test_command():
    print('..Running test method command')


def test_execute():
    print('..Running test method execute')


def test_upload():
    print('..Running test method upload')


def socket_bind():
    parser = args()
    bind.socket_loop(parser['target'], parser['port'])


def socket_connect():
    print('..Running test method socket connect')


def test_listen():
    print('..Running test method listen')
    socket_bind()


def test_client_handler():
    parser = args()
    print('..Running client handler')
    socket_connect()

    if parser['upload_destination']:
        test_upload()
        if parser['command']:
            test_command()

    elif parser['execute']:
        test_execute()

    elif parser['command']:
        test_command()


def test_client_sender(buffer):
    print('..Running test method client sender')


if __name__ == '__main__':
    def manager():
        parser = args()
        if parser['listen']:
            bind.socket_loop(parser['target'], parser['port'])
        elif not parser['listen'] and len(parser['target']) and parser['port'] > 0:
            buffer = sys.stdin.read()
            test_client_sender(buffer)

    manager()

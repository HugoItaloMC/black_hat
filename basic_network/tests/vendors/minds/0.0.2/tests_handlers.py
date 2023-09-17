import socket

from tests_parserargs import JoinParser
from tests_opt import test_upload_destination, test_execute, test_command

args = JoinParser()


def test_client_handler(client_socket):
    parser = args()

    if parser['upload_destination']:
        test_upload_destination()
        if parser['command']:
            print('In `test_client_handler` from opt`upload_destination` before `command` Operations')
            #test_command()

    elif parser['execute']:
        #test_execute()
        print('In `test_client_handler` from opt `execute`  Operations')

    elif parser['command']:
        test_command(client_socket)


def test_client_sender(buffer):
    client = None
    parser = args()
    for res in socket.getaddrinfo(parser['target'], parser['port'], socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
    else:
        try:

            client = socket.socket(af, socktype, proto)
            client.connect(sa)

            while True:
                client.settimeout(7)
                data = client.recv(4096)
                if not data:
                    break

                print(data.decode(), flush=True)

        except Exception as err:
            print("Error: Type Error %s" % type(err))

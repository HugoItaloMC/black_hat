from tests_parserargs import JoinParser

args = JoinParser()


def test_port_target():
    print('Running test method port target')


def test_command():
    print('Running test method command')


def test_execute():
    print('Running test method execute')


def test_upload():
    print('Running test method upload')


def socket_bind():
    print('Running test method socket bind')


def socket_connect():
    print('Running test method socket connect')


def test_listen():
    print('Running test method listen')
    socket_bind()


def test_client_handler():
    parser = args()
    print('Running client handler')
    socket_connect()

    if parser['upload_destination']:
        test_upload()
        if parser['command']:
            test_command()

    elif parser['execute']:
        test_execute()

    elif parser['command']:
        test_command()


if __name__ == '__main__':
    def manager():
        parser = args()
        if parser['listen']:
            test_listen()
        elif not parser['listen'] and len(parser['target']) and parser['port'] > 0:
            test_client_handler()

    manager()

from tests_abs import Allowers


class AllowedServer(Allowers):

    def _allowed(self, _socket, object_send, target, port):
        _socket.bind((target, port))
        _socket.listen(5)

        while True:
            client_socket, addr = _socket.accept()
            print("[*] - Allowed conn .")
            threads = [self._process(target=object_send.con, args=(client_socket,))]
            [thread.start() for thread in threads]
            while True:
                pipe = self.pipeline(client_socket.recv(1024))
                if not pipe: break
                with open('out_process.jsonl', 'a+') as filerr:
                    filerr.write(pipe.decode())
            [thread.join() for thread in threads]


class AllowedConn(Allowers):

    def __init__(self):
        super().__init__()

    def _allowed(self, _socket, object_send, target, port):
        _socket.connect((target, port))
        while object_send.loop():
            print("Connected in %s ." % target)
            object_send.con = _socket

            while object_send.loop():
                msg = _socket.recv(1024)
                if not msg: break
                print(str(msg, 'utf-8'))

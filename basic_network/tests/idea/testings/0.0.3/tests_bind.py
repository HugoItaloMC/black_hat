from threading import Thread

from tests_main import AllowedServer
from tests_abs import Sender


class SenderBind(Sender):

    def __init__(self):
        super().__init__()
        self._process = Thread

    def start_process(self, target, port):
        try:
            allow = AllowedServer()
            _socket, addr = self.conn_info(target, port)
            threads = [self._process(target=allow._allowed, args=(_socket, self, addr[0], addr[1]))]
            [thread.start() for thread in threads]
            print("***\tIniciando Servidor Aguardando Conexão\t***")
            msg = input()
            while True:
                self.put("Server: " + msg)
                msg = input()

            [thread.join() for thread in threads]
            print(threads.result)
            _socket.close()
            exit()

        except Exception as err:
            print("## Error\t:: %s" % err)


if __name__ == '__main__':
    _start = SenderBind()
    _start.start_process(target=input("::\tINPUT TARGET: "), port=int(input("::\tTARGET PORT FROM LOCAL: ")))

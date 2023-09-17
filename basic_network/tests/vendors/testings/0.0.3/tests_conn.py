from threading import Thread

from tests_main import AllowedConn
from tests_abs import Sender


class SenderConn(Sender):

    def __init__(self):
        super().__init__()
        self._process = Thread

    def start_process(self, target: str, port: int):
        try:
            _socket, addr = self.conn_info(target, port)
            _allower = AllowedConn()
            threads = [self._process(target=_allower._allowed, args=(_socket, self, addr[0], addr[1]))]
            [thread.start() for thread in threads]
            print("")
            msg = input()
            while True:
                self.put(msg)
                msg = input()

            [thread.join() for thread in threads]
            _socket.close()
            exit()

        except Exception as err:
            print("## Error\t:: %s" % err)


if __name__ == '__main__':
    _task = SenderConn()
    _task.start_process(target=input("::\tINPUT TARGET: "), port=int(input("::\tINPUT PORT FROM LOCAL: ")))

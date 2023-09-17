import subprocess
from threading import Thread
from abc import ABCMeta, abstractmethod
from socket import (socket, AF_UNSPEC,
                    SOCK_STREAM, AI_PASSIVE,
                    SO_REUSEADDR, SOL_SOCKET,
                    getaddrinfo, SocketType)


class Sender(metaclass=ABCMeta):

    @classmethod
    def conn_info(cls, *args) -> tuple or None:
        #
        for line in getaddrinfo(args[0],
                                args[1],
                                AF_UNSPEC, SOCK_STREAM, 0,
                                AI_PASSIVE):
            AF_, SOCKET_TYPE, PROTOCOL, CANONNAME, ADDR = line
        else:
            try:
                cls._socket = socket(AF_, SOCKET_TYPE, PROTOCOL)
                cls._socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                return cls._socket, ADDR,

            except Exception as err:
                print("##\t Error: %s" % err)

    def __init__(self):
        self.__msg: str = str()
        self.new: bool = True
        self.con = None
        self._socket: SocketType

    def put(self, msg: str):
        self.__msg = msg

        if self.con is not None:
            self.con.send(str.encode(self.__msg))

    def get(self):
        return self.__msg

    def loop(self):
        return self.new

    @abstractmethod
    def start_process(self):
        raise NotImplementedError


class Allowers(metaclass=ABCMeta):

    def __init__(self):
        self._process = Thread

    def pipeline(self, arg):
        COMMAND = arg.rstrip()
        proc = subprocess.check_output(COMMAND, stderr=subprocess.PIPE, shell=True)
        return proc

    @abstractmethod
    def _allowed(self):
        raise NotImplementedError

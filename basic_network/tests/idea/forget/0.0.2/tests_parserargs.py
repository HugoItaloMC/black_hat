import argparse
import sys


class JoinParser:
    # Controller args to engine

    def __getattr__(self, attr):
        # Lazy Attr
        valur = attr
        setattr(self, attr, valur)
        return valur

    def parser_args(self):
        args = self.window_args()
        # Join args from client for process the engine
        self.target = args.target
        self.port = int(args.port) if args.port is not None else None
        self.listen = args.listen
        self.command = args.command
        self.execute = args.execute
        self.upload_destination = args.upload

        return self.__dict__

    @staticmethod
    def window_args():
        # Inpout args from window client
        __parser = argparse.ArgumentParser(sys.argv[1:], description='NetCat With Python')
        __parser.add_argument('-l', '--listen', action='store_true', help='TODO: Running socket bind')
        __parser.add_argument('-e', '--execute', metavar='FILE', help='TODO: Send file in path using running command')
        __parser.add_argument('-c', '--command', action='store_true', help='TODO: To execute shell command')
        __parser.add_argument('-u', '--upload', metavar='DESTINATION', help='TODO: Upload output from to send path')
        __parser.add_argument('-t', '--target', metavar='HOST', help="TODO: Target to bind and connect socket")
        __parser.add_argument('-p', '--port', metavar='PORT', help='TODO: Port from target to connect and bind socket')
        return __parser.parse_args()

    def __call__(self, *args, **kwargs):
        return self.parser_args()


if __name__ == '__main__':
    parser = JoinParser()
    print(parser())


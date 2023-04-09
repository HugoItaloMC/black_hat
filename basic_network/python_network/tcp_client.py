import socket
import threading

# TCP CLIENT

target_host = "google.com.br"
target_port = 80

# Create a Socket Object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect client
client.connect((target_host, target_port))

# Send some data (enviar alguns dados)
client.send(b"GET / HTTP/1.1\r\nHost: google.com.br\r\n\r\n")

# Receive some data (recebendo alguns dados)
response = client.recv(4096)
print(response)
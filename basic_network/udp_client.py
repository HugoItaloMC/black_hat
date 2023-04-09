import socket

# UDP CLIENT
target_host = '127.0.0.1'
target_port = 80

# Create a Socket Object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send some Data
client.sendto(b"AAAABBBBCCCC", (target_host, target_port))

# Receive some data
data, addr = client.recvfrom(4096)
print(data)
import socket
import threading

bend_ip = "0.0.0.0"
bend_port = 9090

# Create Object Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.listen(5)  # Await Connection 5
print("[*] Listening on %s:%d" % (bend_ip, bend_port))

def handle_client(client_socket: socket) -> None:

    # Este e o tratamento da threading com handler-client`
    # Imprimir o que o cliente envia

    request = client_socket.recv(1024)
    print("[*] Received : %s" % request)

    # Enviar devolta um pacote
    client_socket.send("ACK!")

    client_socket.close()


while True:

    client, addr = server.accept()
    print("[*] Accept Connection %s:%d" % (addr[0], addr[1]))

    # Girar nosso threading do client para lidar com dados de entrada
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
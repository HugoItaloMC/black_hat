# The tool TCP PROXY

import sys
import socket
import threading


def server_loop(local_host, local_port_, remote_host, remote_port, receiv_first):

    # Create Server Socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Start bind`s server
    try:
        server.bind((local_host, local_port_))

    except Exception as err:
        print("[!!] Failed to listen server: %s:%a \n\n[!!] Check for other listening sockets or correct permissions" %
              (local_host, local_port_)
              )
    print("[!!] Listening on %s:%s" %
          (local_host, local_port_))


    # Start connection client
    while True:
        client_socket, addr = server.accept()

        # Print out the local connection information
        print("[==>] Received incoming connection from %s:%d" %
              (addr[0], addr[1])
              )

        # Start a Thread to talk to the remote host
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket,
                remote_host,
                remote_port,
                receiv_first)
        )
        proxy_thread.start()


def main():

    # Analisando linha de comando, exemplo de uso
    if len(sys.argv[1:]) != 5:
        print("Usage: ./toolnet_proxy.py [local_host] [local_port] [remote_host] [remote_port] [receive_first]"
              "\nExample: python -m toolnet_proxy 127.0.0.1 9090 10.12.132.1 9000 True")
        sys.exit()

    # Set local listening parameters
    local_host = sys.argv[1]
    local_port = sys.argv[2]

    # Set remote target
    remote_host = sys.argv[3]
    remote_port = sys.argv[4]

    # Dizendo para nosso proxy para enviar e receber dados, antes de enviar para o host remoto
    receiv_first = sys.argv[5]

    receiv_first = True if "True" in receiv_first else False

    # Start lintening socket
    server_loop(local_host, local_port, remote_host, remote_port, receiv_first)


def proxy_handler(client_socket, remote_host, remote_port, receiv_first):

    # Connect to the remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # Receive data from the remote end if necessary
    if receiv_first:

        remote_buffer = receiv_from(remote_socket)
        hexdump(remote_buffer)

        # Send it to our response handler
        remote_buffer = response_handler(remote_buffer)

        # If we have data to send to our local client, send it
        if len(remote_buffer):
            print("[<==] Sending %d bytes to localhost." % len(remote_buffer))
            client_socket.send(remote_buffer)

    # Agora vamos rodar ha leitura local
    # Algum para local, algum para remoto
    # Lavar, enxugar, repita

    while True:

        # Leitura local host
        local_buffer = receiv_from(client_socket)

        if len(local_buffer):
            print('[==>] Sending %d bytes to local host' % len(local_buffer))
            hexdump(local_buffer)

            # send it to our  request handler
            local_buffer = request_handler(local_buffer)

            # send off the data to the remote host
            remote_socket.send(local_buffer)
            print("[==>] Send to remote")

        # Receive back the response
        remote_buffer = receiv_from(remote_socket)

        if len(remote_buffer):

            print("[<==] Received %d bytes from remote " % remote_buffer)
            hexdump(remote_buffer)

            # Send to our response handler
            remote_buffer = response_handler(remote_buffer)

            # Send the response to the local socket
            client_socket.send(remote_buffer)

            print("[<==] Sent to local host")

        # if no more data on either side, close the connections
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()


def hexdump(src, lenght=16):
    result = []
    digits = 4 if isinstance(src, str) else 2

    for line in range(0, len(src), lenght):
        s = src[line:line+lenght]
        hexa = b"".join(["%0*X" % (digits, ord(x)) for x in s])
        text = b"".join([x if 0x20 <= ord(x) < 0x7F else b"." for x in s])
        result.append(b"%04X    %-*s    %s" % (line, lenght* (digits + 1), hexa, text
                                               )
                      )
    print(b"\n".join(result))


def receiv_from(connection):

    buffer = ""

    # We set a 5 second timeout buffer until
    # target, this may need to be adjusted
    connection.settimeout(5)

    try:
        # Keep reading into the buffer until
        # there`s no more data
    # Or we time out
        while True:
            data = connection.recv(4096)

            if not data:
                break
            buffer += data
    except Exception as err:
        pass
    return buffer


def response_handler():
    ...


def request_handler():
    ...


if __name__ == '__main__':
    main()

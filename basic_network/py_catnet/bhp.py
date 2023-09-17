import sys
import socket
import threading
import subprocess
import argparse
import logging

# some Globals Variables

listen: bool = False
command: bool = False
upload: bool = False
execute: str = ""
target: str = ""
upload_destination = '/tmp'
port: int


def usage():
    print("BHP NET TOOL"
          "\nUsage: bhp.py -t target_host -p port"
          "\n-l --listen \n:: Executar em [host]:[port] para conexoes de entrada"
          "\n-e --execute=file_to_run \n:: Receber arquivo fornecido em cima receber uma ligacao"
          "\n-c --comand \n:: Inicializa um Comando shell"
          "\n-u --upload=destination \n:: Ao receber conexao carregar um arquivo e gravar em [destination]"
          "\nEx:\n:: ~$bhp.py -t 192.168.0.1 -p 5555 -l -c"
          "\n\n~$bhp.py -t 192.168.0.1 -p 5555 -l -u=[path_to_saved]"
          "\n\n~$bhp.py -t 192.168.0.1 -p 5555 -l -e='cat /etc/passwd'"
          "\n\n~$echo 'AAAABBBCCCDDDEEEFFF' | ./bhp.py -t 192.168.0.1 -p 135"
          )
    sys.exit(0)


def main():
    global listen
    global command
    global upload
    global execute
    global target
    global upload_destination
    global port

    # Ler as Opcoes da linha de comando
    parser = argparse.ArgumentParser(prog="PY NETCAT", usage="%(prog)s")
    parser.add_argument('-l', '--listen', action='store_true', help='TODO: listar/instanciar servidor TCP')
    parser.add_argument('-e', '--execute', metavar='FILE', help='TODO: Executar comando externo')
    parser.add_argument('-c', '--command', action='store_true', help='TODO: Begin shell')
    parser.add_argument('-u', '--upload', metavar='DESTINATION', help='TODO: Upload logging from app to file back')
    parser.add_argument('-t', '--target', metavar='HOST', help='TODO: Host for server or client')
    parser.add_argument('-p', '--port', type=int, metavar='PORT', help='TODO: Port to server or client')

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_usage()
        sys.exit()

    listen = args.listen
    execute = args.execute
    command = args.command
    upload = bool(args.upload)
    upload_destination = upload_destination if args.upload else ''
    target = args.target
    port = args.port

    # TODO: args para instanciar variaveis globais
    if listen:
        server_loop()

    elif not listen and len(target) and port > 0:
        buffer = sys.stdin.read()
        client_sender(buffer)


# Send Client
def client_sender(buffer):
    """
    :param buffer: Comandos de entrada por parametros
    :return: non
    """

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conectando para host de destino
        with client_socket:
            client_socket.connect((target, port))

            if len(buffer):
                client_socket.sendall(buffer.encode())

            while True:
                # Esperar retorno de dados
                response = b""

                while True:
                    data = client_socket.recv(4096)

                    if not data:
                        break
                    response += data
                print(response, )
    except socket.timeout:
        print("Error: Connection Time out")
    except ConnectionRefusedError:
        print("Error: Connection Refused")
    except ConnectionResetError:
        print("Error: Connection Reseted")
    except OSError as err:
        print(f"Error: {type(err)}")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        # Esperar por alguma entrada

        buffer = input("Enter command: ")

        # Enviar
        client_socket.sendall(buffer.encode())
        client_socket.settimeout(10)


# Primary Server Loop


def server_loop():
    global target, port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Se nenhum trajeto for definido, sera listada diversas interdaces
        if not target:
            target = socket.gethostbyname('localhost')

        # Start TCP server with socket

        # Configurar para reutilizar a host e a porta
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server.bind((target, port))

        # Await Definitions
        server.listen(5)
        print(f"[*] - Listening on {target}:{port}")

        while True:
            client_socket, addr = server.accept()
            print(f"[*] - Accepted connection from {addr[0]}:{addr[1]}")

            # Visao de uma nova threading para nosso client
            client_thread = threading.Thread(target=client_handler, args=(client_socket,))
            client_thread.start()

    except Exception as err:
        print(f"Error : {err}")

    finally:
        server.close()


def run_command(command):
    command = command.rstrip()

    # Executar o comando e retornar uma saida
    try:
        output = subprocess.check_call(command,
                                       stderr=subprocess.STDOUT,
                                       shell=True)

    except:
        output = "Failed the execution command line\r\n"

    # Enviar a Saida de volta para o cliente
    return output.encode()


# Upload de arquivos, execucao de comandos e o shell

def client_handler(client_socket):
    global upload_destination
    global execute
    global command

    # Checando para Carregamento
    if len(upload_destination):
        # Lidos em todos os bytes e mandamos para nosso arquivo
        file_buffer = ""
        max_file_size = 1024 * 1024  # 1MB
        # Manter a leitura ate que nao esteja mais disponivel

        while True:
            data = client_socket.recv(1024)

            if not data:
                break

            file_buffer += data

            if len(file_buffer) > max_file_size:
                client_socket.sendall(b"O tamanho do arquivo excede o tamanho esperado")

            # Agora tomamos os bytes e tentamos escrever no arquivo de carregamento
            try:
                with open(f'{upload_destination}.txt', "wb") as arq:
                    arq.write(file_buffer.encode())
                    client_socket.sendall(f"Arquivo Salvo com Sucesso em {upload_destination}".encode())

            except Exception:
                client_socket.sendall(f"Falha ao salvar arquivo em {upload_destination}".encode())

            # Checando Comando Para execucao
            if execute:
                # Executando comando

                try:
                    output = subprocess.run(
                        execute.split(),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        check=True).stdout
                    client_socket.sendall(output.decode())

                except subprocess.CalledProcessError as err:
                    print(f"Erro ao executar o comando {err.output}".encode())

            # Agora vamos para outro ciclo se um comando shell for chamado
            if command:

                while True:
                    # Mostrar uma linha simples
                    client_socket.sendall(b"BHP.># ")

                    # Agora recebemos ate que haja um avanco na linha (tecla enter)
                    cmd_buffer = ""

                    while "\n" not in cmd_buffer:
                        # Alguma saida do comando
                        command = run_command(cmd_buffer)
                        # Alguma resposta de saida
                        client_socket.sendall(command)


if __name__ == '__main__':
    logging.basicConfig(filename='logging.txt',
                        filemode='wb',
                        level=logging.INFO,
                        format="%(asctime)s %(levelname) %(messege)s")
    main()

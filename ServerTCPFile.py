import socket
import os
import struct

TCP_IP = '192.168.0.14' # endereço IP do servidor 
TCP_PORTA = 42127      # porta disponibilizada pelo servidor
TAMANHO_BUFFER = 1024

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((TCP_IP, TCP_PORTA))
servidor.listen(1)

print("Servidor disponível na porta 42127 e escutando...\n")
print("Para acessar menu de imagens, digite '#menu'.\n")
conn, addr = servidor.accept()
print('Endereço conectado:', addr)

while True:
    data = conn.recv(TAMANHO_BUFFER)
    if not data:
        break  # Encerra a conexão se não houver mais dados

    mensagem = data.decode('utf-8')
    print("Cliente:", mensagem)

    if mensagem.upper() == "QUIT":
        print("Conexão encerrada pelo cliente.")
        conn.close()  # Fecha a conexão com o cliente
        break
    elif mensagem.upper() == "#MENU":
        lista = ""
        files = os.listdir("imagens")
        for i in files:
            if i.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                lista = lista + i + " ||| " 
        conn.send(lista.encode('utf-8'))
        data = conn.recv(TAMANHO_BUFFER)
        if not data:
            break  # Encerra a conexão se não houver mais dados
        mensagem = data.decode('utf-8')
        print("Cliente:", mensagem)
        imagem_solicitada = "imagens/" + mensagem
        image_size = os.path.getsize(imagem_solicitada)
        conn.send(struct.pack("!Q",image_size))
        with open(imagem_solicitada, "rb") as file:
            data = file.read(2048)
            while data:
                conn.send(data)
                data = file.read(2048)
            conn.send("Imagem enviada com sucesso".encode('utf-8'))
            file.close()
    else:
        resposta = input("Servidor: ")
        conn.send(resposta.encode('utf-8'))

servidor.close()  # Fecha o socket do servidor após a conexão ser encerrada

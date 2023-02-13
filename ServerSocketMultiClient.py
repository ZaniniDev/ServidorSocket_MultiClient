import threading
import socket

HOST = "localhost" #aqui você pode subistituir pelo IP de rede que você deseja fazer o socket
PORT = 7777 #aqui você pode colocar qualquer outra porta, o recomendado é ser uma porta maior que 1023, para evitar conflitos de padronização
CLIENTS_SOCKET = []

def messagesTreatment(client): 
    onBroadcast = True #deixe ativado caso queira que o servidor faça um broadcast entre os clients   
    while True:
        try:
            msg = client.recv(5000)
            ip = str(client.getsockname())
            msgDecodificada = msg.decode('utf-8').strip()
            print("RECEBIDO PACOTE DO IP - ("+str(ip)+") - MENSAGEM:"+str(msgDecodificada))
            if(client not in CLIENTS_SOCKET):
                """ Momento onde é adicionado o Client na lista de Clients que o servidor está em conexao"""
                CLIENTS_SOCKET.append(client)
                print("Novo Client adicionado! Total: "+str(len(CLIENTS_SOCKET)))                
            if(onBroadcast == True):
                broadcast(msg, client)
        except Exception as e:
            print(e)            
            deleteClient(client)
            break

def broadcast(msg, client):
    #função para enviar mensagens recebidas para todos os clientes
    clients = CLIENTS_SOCKET
    for clientItem in clients:
        """ Percorre todos os clients para enviar a mensagem recebida"""
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                deleteClient(clientItem)

def deleteClient(client):
    if(client in CLIENTS_SOCKET):
        CLIENTS_SOCKET.remove(client)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        server.listen()
        print("Iniciou o servidor")
    except:
        return print('\nNão foi possível iniciar o servidor!\n')
    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()


main()
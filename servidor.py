import socket
import threading

HOST = input("Host: ")
PORT = int(input("Port: "))

servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
servidor.bind((HOST,PORT))
servidor.listen()
print(f'O servidor está ativo e receptivo {HOST}:{PORT}')

clientes = []
usernames = []

def globalMessage(message):
    for cliente in clientes:
        cliente.send(message)

def handleMessages(cliente):
    while True:
        try:
            recebeMensagemDeCliente = cliente.recv(2048).decode('ascii')
            globalMessage(f'{usernames[clientes.index(cliente)]} :{recebeMensagemDeCliente}'.encode('ascii'))
        except:
            clientLeaved = clientes.index(cliente)
            client.close()
            clientes.remove(clientes[clientLeaved])
            clientLeavedUsername = usernames[clientLeaved]
            print(f'{clientLeavedUsername} has left the chat...')
            globalMessage(f'{clientLeavedUsername} has left us...'.encode('ascii'))
            usernames.remove(clientLeavedUsername)


def initialConnection():
    while True:
        try:
            cliente, address = servidor.accept()
            print(f"New Connetion: {str(address)}")
            clientes.append(cliente)
            cliente.send('getUser'.encode('ascii'))
            username = cliente.recv(2048).decode('ascii')
            usernames.append(username)
            globalMessage(f'{username} just joined the chat!'.encode('ascii'))
            user_thread = threading.Thread(target=handleMessages,args=(cliente,))
            user_thread.start()
        except:
            pass

initialConnection()
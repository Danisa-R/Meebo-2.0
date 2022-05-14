import socket
from ssl import CHANNEL_BINDING_TYPES
import threading

host = '127.0.0.1'
port = 9091

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port)) 
server.listen() # server starts listening for incoming connections

clients = []
nicknames = []

# broadcast message to clients connected to server
def broadcast(message):
    for client in clients:
        client.send(message)

# handle method for client connections
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            current_client = clients.index(client)
            print(f'{nicknames[current_client]}')
            broadcast(message)
        except:
            clients.remove(client)
            client.close()
            nickname = nicknames[clients.index(client)]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.pop(nickname)
            break

# main method
def receive():
    while True:
        client, address = server.accept() # client socket & address socket accepts
        print(f'Connected with {str(address)}') 

        client.send('NICK'.encode('ascii')) 
        nickname = client.recv(1024).decode('ascii') 
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of client is: {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('ascii')) # every client knows about the new client
        client.send('Connected to the server'.encode('ascii'))

        #run one thread for each client connected
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
print("~~ Server is listening ~~~")
receive()
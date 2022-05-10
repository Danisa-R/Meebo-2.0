import socket
from ssl import CHANNEL_BINDING_TYPES
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port)) # server is bind or bound to localhost on port 55555 
server.listen() # server starts listening for incoming connections


clients = []
nicknames = []

#broadcast message to clients connected to server
def broadcast(message):
    for client in clients:
        client.send(message)

#handle method for client connections
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client) # need index to remove client from list
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

#main method
def receive():
    while True:
        client, address = server.accept() 
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

receive()
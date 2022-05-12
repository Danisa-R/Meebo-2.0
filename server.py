import socket
from ssl import CHANNEL_BINDING_TYPES
import threading

host = '127.0.0.1'
port = 55557

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port)) 
server.listen() # server starts listening for incoming connections

clients = []
usernames = []

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
            print(f'{usernames[current_client]}')
            broadcast(message)
        except:
            clients.remove(client)
            client.close()
            username = usernames[clients.index(client)]
            broadcast(f'{username} left the chat!'.encode('ascii'))
            usernames.pop(username)
            break

# main method
def receive():
    while True:
        client, address = server.accept() # client socket & address socket accepts
        print(f'Connected with {str(address)}') 

        client.send('USER'.encode('utf-8')) 
        username = client.recv(1024).decode('ascii') 
        usernames.append(username)
        clients.append(client)

        print(f'Username of client is: {username}')
        broadcast(f'{username} joined the chat!'.encode('ascii')) # every client knows about the new client
        client.send('Connected to the server'.encode('ascii'))

        #run one thread for each client connected
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
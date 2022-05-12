import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

host = '127.0.0.1' 
port = 55557

username = input('What is your name: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1, 55557'))

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        message = tkinter.Tk() # window where we'll have file dialog

        message.withdraw()
        self.username = simpledialog.askstring("Username", 
        "Please choose a Username", parent=message)

        self.gui_done = False
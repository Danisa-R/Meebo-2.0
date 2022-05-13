from re import A
import socket
from struct import pack
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

host = '127.0.0.1' # if server is online provide public IP address
port = 55557

nickname = input('What is your name: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1, 55557'))

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        message = tkinter.Tk() # window where we'll have file dialog

        message.withdraw()
        self.nickname = simpledialog.askstring("Nickname", 
        "Please choose a Nickname", parent=message)

        self.gui_done = False 
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win == tkinter.Tk()
        self.win.configure(bg="lightblue")

        self.chat_label = tkinter.Label(self.win, text="Chat", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.message_label = tkinter.Label(self.win, text="Chat", bg="lightgray")
        self.message_label.configure(font=("Arial", 12))
        self.message_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Sent", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop) # window eventhandler , program terminate
        self.win.mainloop()

    def write(self):
        message = f'{self.nickname}: {self.input_area.get('1.0', 'end')}'
        self.sock.send(message.encode('ascii'))
        self.input_area.delete('1,0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('ascii'))
                else:


            except:
                pass
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import tkinter as tkt

class ClientManager:
    def __init__(self, bufsiz, host, port):
        self.bufsiz = bufsiz
        self.is_running = False

        self.host = host
        self.port = port

    # launch the execution of a client and the creation of socket and graphical interface
    # manage possible connection errors
    def launch_client(self):
        self.draw_client_interface()
        self.is_running = True
        if not self.port:
            self.port = 53000
        else:
            self.port = int(self.port)
        self.addr = (self.host, self.port)
        try:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.addr)
            print("Connection enstablished")
        except socket.error as e:
            print("Connection error: ", e)

        receive_thread = Thread(target=self.receive)
        receive_thread.start()

        tkt.mainloop()        

    # manage the receival of messages from the socket
    def receive(self):
        while self.is_running:
            try:
                msg = self.client_socket.recv(self.bufsiz).decode("utf8")
                self.msg_list.insert(tkt.END, msg)
            except OSError:
                print("The client has been disconnected from the server.")

    # send a message
    def send(self, event = None):
        msg = self.my_msg.get()
        self.my_msg.set("")
        self.client_socket.send(bytes(msg, "utf8"))

    # close the socket if the graphical interface is closed
    def on_closing_view(self, event=None):
        self.client_socket.close()
        self.is_running = False
        self.window.destroy()

    # graphical interface creation method
    def draw_client_interface(self):
        self.window = tkt.Tk()
        self.window.title("Chatroom")

        self.messages_frame = tkt.Frame(self.window)
        self.my_msg = tkt.StringVar()
        self.my_msg.set("Write here your text.")
        self.scrollbar = tkt.Scrollbar(self.messages_frame)
        
        self.msg_list = tkt.Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
        self.msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
        self.msg_list.pack()
        self.messages_frame.pack()

        entry_field = tkt.Entry(self.window, textvariable=self.my_msg)
        entry_field.bind("<Return>", self.send)
        entry_field.pack()
        send_button = tkt.Button(self.window, text="Enter", command=self.send)
        send_button.pack()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing_view)

if __name__ == "__main__":
    BUFSIZ = 1024
    HOST = '127.0.0.1'
    PORT = 53000

    client_manager = ClientManager(BUFSIZ, HOST, PORT)
    client_manager.launch_client()
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

class ServerManager:
    def __init__(self, host, port, bufsiz):
        addr = (host, port)
        self.bufsiz = bufsiz
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind(addr)

        self.clients = {}
        self.addresses = {}

        self.is_running = False

    # launch server execution
    def launch_server(self):
        self.is_running = True
        self.server.listen(5)
        print("Waiting connections...")
        ACCEPT_THREAD = Thread(target=self.handle_incoming_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        self.server.close()

    # once the server has been launched continue to listen for incoming connections and
    # manage possible exceptions
    def handle_incoming_connections(self):
        while self.is_running:
            try:
                client, client_address = self.server.accept()
                print("%s:%s joined the chat." % client_address)
                client.send(bytes("Welcome! Write your nickname and press Enter!", "utf8"))
                try:
                     username = client.recv(self.bufsiz).decode("utf8")
                     self.addresses[client] = client_address
                     self.clients[client] = username
                     self.broadcast(bytes("%s joined the chat!" % username, "utf8"))
                     Thread(target=self.handle_client, args=(client, username)).start()
                except:
                    print("Client disconnected")
            except Exception as e:
                print('Error: unable to accept clients', e)

    # broadcast messages received from clients and manage possible disconnection exceptions
    def handle_client(self, client, username):
        while self.is_running:
            try:
                msg = client.recv(self.bufsiz)
                self.broadcast(msg, username + ": ")
            except ConnectionResetError:
                self.disconnect_client(client, username, True)
                print("Connection reset by %s." % username)
                break
            except Exception as e:
                self.disconnect_client(client, username, True)
                print("An error occurred with %s: %s" % (username, e))
                break

    # remove a client from clients dictionary: can be used both
    # if the disconnection is intentional or originated by some connecion errors
    def disconnect_client(self, client, username, dropped = False):
        print("Client disconnected")
        del self.clients[client]
        if dropped:
            msg = "%s lost connection." % username
        else:
            msg = "%s left the chat." % username
        self.broadcast(bytes(msg, "utf8"))
        client.close()

    # broadcast a message to all the clients registered to the server
    def broadcast(self, msg, prefix=""):
        for user in self.clients:
            user.send(bytes(prefix, "utf8") + msg)

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 53000
    BUFSIZ = 1024

    server_manager = ServerManager(HOST, PORT, BUFSIZ)
    server_manager.launch_server()


                


        
        


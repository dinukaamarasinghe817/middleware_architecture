import socket
import sys
import threading

isActive = threading.Event()
isActive.set()

clients = []

class ClientThread(threading.Thread):
    def __init__(self, client_socket, addr, mode):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.addr = addr
        # self.clients = clients
        self.mode = mode

    def run(self):
        print("Client connected: {}".format(self.addr))

        if self.mode == "PUBLISHER":
            self.handle_publisher()
        elif self.mode == "SUBSCRIBER":
            self.handle_subscriber()

        self.client_socket.close()
        clients.remove(self.client_socket)
        print("Client disconnected: {}".format(self.addr))

    def handle_publisher(self):
        global clients
        while True:
            data = self.client_socket.recv(1024).decode()
            if not data:
                break

            # Send the message to all subscriber clients
            for client in clients:
                if client.mode == "SUBSCRIBER":
                    client.client_socket.send(data.encode())

    def handle_subscriber(self):
        while True:
            data = self.client_socket.recv(1024).decode()
            if not data:
                break

            # Display the message from the publisher
            print("Received from publisher {}: {}".format(self.addr, data))

def run_server(port):
    global clients # to keep track all clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    server_socket.bind((host, port))

    # Listen for 10 connections
    server_socket.listen(10)

    print("Server listening on {}:{}".format(host, port))

    def input_thread():
        while True:
            user_input = input()
            if user_input.lower() == 'terminate':
                print("Goodbye! Exiting program\n")
                isActive.clear()
                break

    input_thread = threading.Thread(target=input_thread)
    input_thread.start()

    while isActive.is_set():
        client_socket, addr = server_socket.accept()
        mode = client_socket.recv(1024).decode()
        client_thread = ClientThread(client_socket, addr, mode)
        client_thread.mode = mode
        clients.append(client_thread)
        client_thread.start()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    run_server(port)

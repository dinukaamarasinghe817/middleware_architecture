import socket
import sys
import threading
import select

# to track termination
isActive = threading.Event()
isActive.set()

clients = []

class ClientThread(threading.Thread):
    client_count_lock = threading.Lock()
    client_count = 1

    def __init__(self, client_socket, addr):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.addr = addr
        with ClientThread.client_count_lock:
            self.id = ClientThread.client_count
            ClientThread.client_count += 1

    # handle client connections
    def run(self):
        print("Client{} connected from : {}".format(self.id, self.addr))
        self.handle_client()
        self.client_socket.close()
        self.remove_client()
        print("Client{} disconnected : {}".format(self.id, self.addr))

    # handle publisher
    def handle_client(self):
        global clients
        while True:
            data = self.client_socket.recv(1024).decode()
            if not data or data == "terminate":
                break
            print("Client{} : {}".format(self.id, data))
    
    # once client got disconnected, remove
    def remove_client(self):
        global clients
        for thread in clients:
            if thread.client_socket == self.client_socket:
                clients.remove(thread)
                break

# to obtain IP automatically
def get_local_ip():
    try:
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80))
        local_ip = temp_socket.getsockname()[0]
        temp_socket.close()
        return local_ip
    except socket.error:
        return None

def run(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = get_local_ip()
    if(host == None):
        print("Unable to obtain local IP address!")
    server_socket.bind((host, port))
    server_socket.listen(0)
    print("Listening on {} : {}".format(host, port))

    def input_thread():
        while isActive.is_set():
            user_input = input()
            if user_input.lower() == 'terminate':
                if threading.active_count() - 2 > 0:
                    print("Can't terminate, there are active clients")
                else:
                    print("Goodbye!\n")
                    isActive.clear()
                    break

    input_thread = threading.Thread(target=input_thread)
    input_thread.start()

    while isActive.is_set():
        rlist, _, _ = select.select([server_socket], [], [], 1)
        if server_socket in rlist:
            client_socket, addr = server_socket.accept()
            client_thread = ClientThread(client_socket, addr)
            clients.append(client_thread)
            client_thread.start()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])
    run(port)
import sys
import socket

def run(port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    server_sock.bind((host, port))
    server_sock.listen(1)
    print("Listening on host {} : {}".format(host, port))
    client_sock, address = server_sock.accept()

    while True:
        data = client_sock.recv(1024).decode()
        if not data:
            break
        print("{}".format(data))
    
    client_sock.close()
    server_sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])
    run(port)
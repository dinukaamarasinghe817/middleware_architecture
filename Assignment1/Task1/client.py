import sys
import socket

def run(host,port):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((host,port))

    while True:
        data = input("client :> ")
        if data != "terminate":
            client_sock.send(data.encode())
        else:
            break
    
    client_sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <server> <port>")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    run(host,port)
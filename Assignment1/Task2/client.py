import sys
import socket
import threading


def run(host,port,mode):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((host,port))
    client_sock.send(mode.encode())

    if(mode == "PUBLISHER"):
        while True:
            data = input("client :> ")
            if data.lower() != "terminate":
                client_sock.send(data.encode())
            else:
                break
        
        client_sock.close()
    else:
        while True:
            data = client_sock.recv(1024).decode()
            if data != "":
                print(data)
            else:
                break
        
        client_sock.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <server> <port> <mode>")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    mode = sys.argv[3]
    run(host,port,mode)
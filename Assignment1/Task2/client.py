import sys
import socket
import threading
import select

isActive = threading.Event()
isActive.set()


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
                print("Goodbye!\n")
                break
        
        client_sock.close()
    else:
        def input_thread():
            while isActive.is_set():
                user_input = input()
                if user_input.lower() == 'terminate':
                    print("Goodbye!\n")
                    isActive.clear()
                    break

        input_thread = threading.Thread(target=input_thread)
        input_thread.start()

        def subscribe_thread():
            while isActive.is_set():
                rlist, _, _ = select.select([client_sock], [], [], 1)
                if client_sock in rlist:
                    data = client_sock.recv(1024).decode()
                    if not data:
                        break
                    print(data)
            
            client_sock.close()
        
        subscribe_thread = threading.Thread(target=subscribe_thread)
        subscribe_thread.start()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <server> <port> <mode>")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    mode = sys.argv[3]
    run(host,port,mode)
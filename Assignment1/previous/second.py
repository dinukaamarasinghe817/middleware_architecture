import sys
import socket
import threading
import select

isActive = threading.Event()
isActive.set()
active_threads = []

def publish():
    
    publisher_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    publisher_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    publisher_socket.bind(("localhost", 5555))
    publisher_socket.listen()

    print("\n\t\t--- Type the message and hit ENTER ---\n\t\t--- To quit, type 'exit' ---\n")

    connection, _ = publisher_socket.accept()

    while True:
        message = input()
        if message == "exit":
            print("exited successfully")
            break
        connection.sendall(message.encode())
    
    for thread in active_threads:
        thread.join()

    connection.close()
    publisher_socket.close()

def subscribe():
    subscriber_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    subscriber_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    subscriber_socket.connect(("localhost", 5555))
    subscriber_socket.setblocking(0)

    print("\n\t\t--- To quit, type 'exit' ---\n")

    def input_thread():
        while True:
            user_input = input()
            if user_input.lower() == 'exit':
                print("exited successfully")
                isActive.clear()
                break

    input_thread = threading.Thread(target=input_thread)
    active_threads.append(input_thread)
    input_thread.start()

    while isActive.is_set():
        ready_sockets, _, _ = select.select([subscriber_socket], [], [], 1)

        if subscriber_socket in ready_sockets:
            try:
                message = subscriber_socket.recv(1024).decode()
                if(message != ""):
                    print("Received:", message)
            except socket.error:
                # Handle disconnection when recv fails
                print("Publisher disconnected")
                break

    subscriber_socket.close()

def main(arg1):
    if arg1 == "publisher":
        publish()
    elif arg1 == "subscriber":
        subscribe_thread = threading.Thread(target=subscribe)
        subscribe_thread.start()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <user>")
    else:
        arg1 = sys.argv[1]
        main(arg1)

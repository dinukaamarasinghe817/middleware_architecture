
# type the these commands in terminal to run
# 'python pubsub.py pub' to access publisher interface
# 'python pubsub.py sub' to access subscriber interface

import sys
import zmq
import threading

isActive = threading.Event()
isActive.set()

def publish():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    print("\n\t\t+----------------------------------+")
    print("\t\t+-       Welcome Publisher!       -+")
    print("\t\t+- Type the message and hit ENTER -+")
    print("\t\t+-      To quit, type 'exit'      -+")
    print("\t\t+----------------------------------+\n")

    while True:
        message = input()
        if message == "exit":
            print("Goodbye! Exiting program\n")
            break
        socket.send_string(message)

    socket.close()
    context.term()

def subscribe():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    print("\n\t\t+----------------------------------+")
    print("\t\t+-       Welcome Subscriber!      -+")
    print("\t\t+-      To quit, type 'exit'      -+")
    print("\t\t+----------------------------------+\n")

    def input_thread():
        while True:
            user_input = input()
            if user_input.lower() == 'exit':
                print("Goodbye! Exiting program\n")
                isActive.clear()
                break

    input_thread = threading.Thread(target=input_thread)
    input_thread.start()

    while isActive.is_set():
        if socket.poll(timeout=0):
            message = socket.recv_string()
            print("Received:", message)
    
    socket.close()
    context.term()

def main(arg1):
    if arg1 == "pub":
        publish()
    elif arg1 == "sub":
        subscribe_thread = threading.Thread(target=subscribe)
        subscribe_thread.start()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <user>")
    else:
        arg1 = sys.argv[1]
        main(arg1)

# Instructions to run the application
    i.    Open the terminal or command prompt and naviget to the folder 'Task2'

    ii.   Type 'python server.py <port>' in the terminal and hit enter (eg. port = 5000)

    iii.  Ther server should start and copy the host address

    iv.   Open another instance of the terminal and navigate to the folder 'Task2'

    v.    Type 'python client.py <host_address> <port> <client_type>
            - Replace <host_address> with the address you copied
            - For a publisher, <client_type> = PUBLISHER
            - For a subscriber, <client_type> = SUBSCRIBER

    vi.   As a publisher you can Type any message and hit enter

    vii.  The message will appear in the subscriber terminal

    viii. Repeat stpes (iv, v, vi) To connect multiple publishers and subscribers
    
    viii. To disconnect from client side, type 'terminate' and hit enter

# Constraints

Note : The server could only be terminate when there are no more clients connected to the server.

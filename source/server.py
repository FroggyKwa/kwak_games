from source.web import connect_InSocket, connect_OutSocket, read_sock, sock_send, close_sock


sockIn = connect_InSocket()
running = True

clients = dict()
while running:
    data, address = read_sock(sockIn)
    print(data, type(data))
    print(address)
    if data == '1':
        if address in clients.keys():
            sock_send(clients[address], '2')
            print('request denied: 2')
        elif len(clients.values()) >= 4:
            sock = connect_OutSocket(address=address[0], port=5556)
            sock_send(sock, '3')
            sock.close()
            print('request denied: 3')
        else:
            clients[address] = connect_OutSocket(address=address[0], port=5556)
            sock_send(clients[address], '1')
            print('request accepted')
        print(clients)
    if data == '0':
        sock = clients.pop(address)
        sock_send(sock, '0')
        print('client is disconnected')
        close_sock(sock)
        if len(clients.values()) == 0:
            running = False
        print(clients)


close_sock(sockIn)

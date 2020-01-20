from source.network import connect_InSocket, connect_OutSocket, read_sock, sock_send, close_sock
from source.player import Player
import time


sockIn = connect_InSocket()
running = True

clients = dict()
players = dict()
bullets = list()
cur_time = time.time()
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
            players[address] = Player(100, 100, clients[address])
            sock_send(clients[address], '1')
            print('request accepted')
        print(clients)
    elif data == '0':
        sock = clients.pop(address)
        sock_send(sock, '0')
        print('client is disconnected')
        close_sock(sock)
        if len(clients.values()) == 0:  # сомнительное решение ._.
            running = False
        print(clients)
    elif data.startswith('2'):
        # test our server
        from random import randint
        points = list()
        if time.time() - cur_time >= 5:
            points.append((randint(700, 1000), randint(700, 1000)))
            cur_time = time.time()
        reply = f'Hello, {address[0]}'
        sock_send(clients[address], reply.encode())
        player = players[address]
        keys = tuple(data.split()[1])
        print(keys)
        if keys[119] or keys[32]:
            player.move(direction='up')
        if keys[97]:
            player.move(direction='left')
            player.direction = 'left'
        if keys[100]:
            player.move(direction='right')
            player.direction = 'right'
        if keys[275]:
            player.direction = 'right'
            bullets.append([player.x + 2, player.y + 2, 'right'])
        if keys[276]:
            player.direction = 'left'
            bullets.append([player.x + 2, player.y + 2, 'left'])
close_sock(sockIn)

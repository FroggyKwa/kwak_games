from source.network import connect_InSocket, connect_OutSocket, read_sock, sock_send, close_sock
from source.player import Player
import time


sockIn = connect_InSocket(address='0.0.0.0')
running = True
print(sockIn.getsockname())

clients = dict()
players = dict()
bullets = list()
cur_time = time.time()
points = list()
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
        #from random import randint
        #if time.time() - cur_time >= 2:
        #    points.append((randint(10, 1500), randint(10, 700)))
        #    cur_time = time.time()
        #reply = ' '.join([f'{a}_{b}' for a, b in points])
        #print(reply)
        #sock_send(clients[address], reply)
        player = players[address]
        keys = tuple(map(int, list(data.split()[1])))
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
    for addr in players.keys():
        p = players
        x, y, hp, d = p[addr].x, p[addr].y, p[addr].hp, p[addr].direction
        bullets_str = str(len(bullets)) + ' ' + \
                      ' '.join([str(i[0]) + ' ' + str(i[1]) for i in bullets])
        players_str = str(len(p) - 1) + ' ' + \
                      ' '.join([str(i.x) + ' ' + str(i.y) + ' ' + i.direction
                                for i in p.values() if i != p[addr]])
        reply = f'{x} {y} {hp} {d} {bullets_str} {players_str}'
        sock_send(clients[addr], reply)


close_sock(sockIn)

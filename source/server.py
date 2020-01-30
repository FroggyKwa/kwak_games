from source.network import connect_InSocket, connect_OutSocket, read_sock, sock_send, close_sock
from source.player import Player
import time

sockIn = connect_InSocket(address='0.0.0.0')
running = True
print(sockIn.getsockname())
cur_time = time.time()
clients = dict()
players = dict()
bullets = list()
points = list()
while running:
    data, address = read_sock(sockIn)
    print(data, type(data))
    print(address)
    if data == '1':
        if address in clients.keys():
            sock_send(clients[address], '2')
            print('request de`nied: 2')
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
        player = players[address]
        keys = tuple(map(int, list(data.split()[1])))
        print(keys)
        if keys[119] or keys[32]:
            player.change_velocity(direction='up')
        if keys[97]:
            player.change_velocity(direction='left')
            player.direction = 'left'
        if keys[100]:
            player.change_velocity(direction='right')
            player.direction = 'right'
        if not (keys[119] or keys[32] or keys[97] or keys[100]):
            player.change_velocity()
        if keys[275]:
            player.direction = 'right'
            if not player.cur_shoot_time:
                bullets.append([player.x + 2, player.y + 2, 'right', 180])
                player.cur_shoot_time = 30
        if keys[276]:
            player.direction = 'left'
            if not player.cur_shoot_time:
                bullets.append([player.x + 2, player.y + 2, 'left', 180])
                player.cur_shoot_time = 30
    for i in players.values():
        print(i, players)
        if i.cur_shoot_time:
            i.cur_shoot_time -= 1
    for i in bullets:  # уменьшается жизнь пуль
        print(i)
        i[3] -= 1
        if not i[3]:
            bullets.remove(i)
    for addr in players.keys():
        p = players
        x, y, hp, d = p[addr].x, p[addr].y, p[addr].hp, p[addr].direction
        bullets_str = str(len(bullets)) + ' ' + \
                      ' '.join([str(i[0]) + ' ' + str(i[1]) for i in bullets])
        players_str = str(len(p) - 1) + ' ' + \
                      ' '.join([str(i.x) + ' ' + str(i.y) + ' ' + i.direction
                                for i in p.values() if i != p[addr]])
        reply = f'{x} {y} {hp} {d} {bullets_str} {players_str}'
        if time.time() - cur_time >= 0.001:
            try:
                sock_send(clients[addr], reply)
            except KeyError:
                pass
        print(list([(p.x, p.y, p.x_velocity, p.y_velocity) for p in players.values()]))
        if time.time() - cur_time >= 0.1:
            # пульки движутся со скоростью 200 пикселей в секунду
            b = list()
            for i in bullets:
                v = 20 if i[2] == 'right' else -20
                b.append([i[0] + v, i[1], i[2], i[3]])
            bullets = b
            # bullets = list(map(lambda b: [b[0] + 20, b[1], b[2], b[3]], bullets))
        if time.time() - cur_time >= 0.001:
            for p in players.values():
                p.move()

close_sock(sockIn)

from source.network import connect_InSocket, connect_OutSocket, read_sock, sock_send, close_sock
from source.player import Player
from socket import gethostname, gethostbyname
from source.instances import *
import time, pygame
from source.get_platforms import *

sockIn = connect_InSocket(address='0.0.0.0')
running = True
print('IP:\n' + gethostbyname(gethostname()) + ':5555')
pygame.init()
size = WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode(size)
cur_time = time.time()
clients = dict()
players = dict()
bullets = pygame.sprite.Group()
platforms = list()
get_platforms(screen, platforms)
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
            players[address] = Player(100, 100, socket=clients[address])
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
            player.state = 'jump'
        if keys[97]:
            player.change_velocity(direction='left')
            player.direction = 'left'
            if not player.state == 'jump':
                player.state = 'run'
        if keys[100]:
            player.change_velocity(direction='right')
            player.direction = 'right'
            if not player.state == 'jump':
                player.state = 'run'
        if keys[275]:
            player.direction = 'right'
            player.shooting = True
            if player.state == 'run':
                player.state = 'run-shoot'
            else:
                player.state = 'shoot'
            if not player.cur_shoot_time:
                bullets.add(Bullet(screen, player.x + 2, player.y + 2, 'right'))
                player.cur_shoot_time = 30
        if keys[276]:
            player.direction = 'left'
            player.shooting = True
            if player.state == 'run':
                player.state = 'run-shoot'
            else:
                player.state = 'shoot'
            if not player.cur_shoot_time:
                bullets.add(Bullet(screen, player.x + 2, player.y + 2, 'left'))
                player.cur_shoot_time = 30
        if not (keys[119] or keys[32] or keys[97] or keys[100]):
            player.change_velocity()
            if player.onGround:
                player.state = 'idle'
    for i in players.values():
        print(i, players)
        if i.cur_shoot_time:
            i.cur_shoot_time -= 1
    for addr in players.keys():
        p = players
        x, y, hp, d, state = p[addr].x, p[addr].y, p[addr].hp, p[addr].direction, p[addr].state
        bullets_str = str(len(bullets)) + ' ' + \
                      ' '.join([str(i.rect.x) + ' ' + str(i.rect.y) for i in bullets])
        players_str = str(len(p) - 1) + ' ' + \
                      ' '.join([str(i.x) + ' ' + str(i.y) + ' ' + i.direction
                                for i in p.values() if i != p[addr]])
        reply = f'{x} {y} {hp} {d} {state} {bullets_str} {players_str}'
        if time.time() - cur_time >= 0.001:
            try:
                sock_send(clients[addr], reply)
            except KeyError:
                pass
        if time.time() - cur_time >= 0.1:
            # пульки движутся со скоростью 200 пикселей в секунду
            for i in bullets:
                i.move()
            # bullets = list(map(lambda b: [b[0] + 20, b[1], b[2], b[3]], bullets))
        if time.time() - cur_time >= 0.001:
            for p in players.values():
                p.move(platforms)

close_sock(sockIn)

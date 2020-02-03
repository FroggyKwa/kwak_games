import time
import pygame
from source.network import connect_InSocket, connect_OutSocket, read_sock, sock_send, close_sock
from source.player import Player
from socket import gethostname, gethostbyname
from source.instances import *
from source.get_platforms import *

sockIn = connect_InSocket(address='0.0.0.0')
running = True
print('IP:\n' + gethostbyname(gethostname()) + ':5555')
pygame.init()
cl = pygame.time.Clock()
size = WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode(size)
cur_time = time.time()
clients = dict()
players = dict()
bullets = pygame.sprite.Group()
platforms = pygame.sprite.Group()
get_platforms(screen, platforms)
players['111'] = Player(300, 100)
players['222'] = Player(500, 100)
while running:
    data, address = read_sock(sockIn)
    if data == '1':
        if address in clients.keys():
            sock_send(clients[address], '2')
        elif len(clients.values()) >= 4:
            sock = connect_OutSocket(address=address[0], port=5556)
            sock_send(sock, '3')
            sock.close()
        else:
            print(address, 'подключился')
            clients[address] = connect_OutSocket(address=address[0], port=5556)
            players[address] = Player(100, 100, socket=clients[address])
            sock_send(clients[address], '1')
            # print(clients)
    elif data == '0':
        sock = clients.pop(address)
        sock_send(sock, '0')
        close_sock(sock)
        if len(clients.values()) == 0:  # сомнительное решение ._.
            running = False
    elif data.startswith('2'):
        # print(players)
        player = players[address]
        keys = tuple(map(int, list(data.split()[1])))
        if not (keys[119] or keys[32] or keys[97] or keys[100]):
            player.change_velocity()
            if player.onGround:
                player.state = 'idle'
            player.shooting = False
        if keys[119] or keys[32]:
            player.change_velocity(direction='up')
            player.state = 'jump'
            player.shooting = False
        if keys[275]:  # стрелять вправо
            player.direction = 'right'
            player.shooting = True
            if player.onGround:
                player.state = 'shoot'
            if not player.cur_shoot_time:
                bullets.add(Bullet(screen, player.x + 10, player.y + 23, direction='right', owner=player))
                player.cur_shoot_time = 30
        if keys[276]:  # стрелять влево
            player.direction = 'left'
            player.shooting = True
            if player.onGround:
                player.state = 'shoot'
            if not player.cur_shoot_time:
                bullets.add(Bullet(screen, player.x + 10, player.y + 23, direction='left', owner=player))
                player.cur_shoot_time = 30
        if keys[97]:  # идти влево
            player.change_velocity(direction='left')
            player.direction = 'left'
            if not player.state == 'jump':
                if not player.shooting:
                    player.state = 'run'
                else:
                    player.state = 'run-shoot'
        if keys[100]:  # идти вправо
            player.change_velocity(direction='right')
            player.direction = 'right'
            if not player.state == 'jump':
                if not player.shooting:
                    player.state = 'run'
                else:
                    player.state = 'run-shoot'
        if keys[275]:
            player.direction = 'right'
        elif keys[276]:
            player.direction = 'left'
    for i in players.values():
        if i.cur_shoot_time:
            i.cur_shoot_time -= 1
    for addr in players.keys():
        p = players
        x, y, hp, d, state = p[addr].x, p[addr].y, p[addr].hp, p[addr].direction, p[addr].state
        bullets_str = str(len(bullets)) + ' ' + \
                      ' '.join([str(i.rect.x) + ' ' + str(i.rect.y) for i in bullets])
        players_str = str(len(p) - 1) + ' ' + \
                      ' '.join([str(i.rect.x) + ' ' + str(i.rect.y) + ' ' + i.direction + ' ' + i.state
                                for i in p.values() if i != p[addr]])
        reply = f'{x} {y} {hp} {d} {state} {bullets_str} {players_str}'
        try:
            sock_send(clients[addr], reply)
        except KeyError:
            pass
        for p in players.values():
            p.move(platforms)
        for i in bullets:
            if time.time() - cur_time >= 0.001:
                i.move()
                for p in players.values():
                    if pygame.sprite.collide_mask(i, p) and i.owner != p:
                        i.kill()
                        p.get_damage(20)
        print(*[f'{i.x}, {i.y}; ' for i in players.values()])
        for i in players.values():
            i.change_velocity()
    cl.tick(60)
close_sock(sockIn)

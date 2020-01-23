import pygame
from source.network import *
from source.get_map import *
from source.camera import *
from threading import Thread
import traceback  # todo: убрать эту штуку после дебага
pygame.init()
size = width, height = 1280, 800
screen = pygame.display.set_mode(size)
running = True
FPS = 60
cl = pygame.time.Clock()
ip = ''
msg_text = ''
sockIn = connect_InSocket(address='0.0.0.0', port=5556)
state = 2
messages = list()
camera = Camera(800, 800, (1280, 800))
x, y, hp, d = 0, 0, 100, 'right'  # todo:мусор
while running:
    if state == 1:  # Меню
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 0, 0))

    if state == 2:  # Подключение
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # print(event.unicode, event.key, end='* ')
                if event.key == 8:  # backspace
                    ip = ip[:-1]
                    continue
                if event.key == 27:  # escape
                    state = 1
                    continue
                if event.key == 13:  # enter
                    try:
                        sockOut = connect_OutSocket(address=ip.split(':')[0], port=int(ip.split(':')[1]))
                    except socket.gaierror:
                        msg_text = 'Сервер отключен или не сущесвует'
                        print(traceback.format_exc())
                        continue
                    except (IndexError, ValueError):
                        msg_text = 'IP указан неккоректно'
                        print(traceback.format_exc())
                        continue
                        '''except OSError as e:
                        if e.errno == 10048:
                            msg_text = 'Вы уже подключенны к серверу'
                            print(traceback.format_exc())
                            continue'''
                    else:
                        sock_send(sockOut, '1')
                        data, address = read_sock(sockIn)  # todo: если сервер не включен то виснет, исправить
                        if data == '1':
                            msg_text = 'Подключение прошло успешно!'
                            t1 = Thread(target=read_server_sock, args=(sockIn, messages, running))
                            t1.start()
                            game_background = get_map()
                            print('Поток запущен')
                            print(msg_text)
                            state = 3
                        elif data == '2':
                            msg_text = 'Вы уже подключены к данному серверу'
                        elif data == '3':
                            msg_text = 'Сервер уже заполнен!'
                        print(data)
                ip = ip + event.unicode if event.unicode.isprintable() else ip
                print(event.unicode, event.key, event.mod)
                print(ip)
        font = pygame.font.Font(None, 70)

        phr = font.render(ip, 0, (100, 255, 100))
        phr_w = phr.get_width() if phr.get_width() > 600 else 600
        phr_h = phr.get_height()
        phr_x = width // 2 - phr_w // 2
        phr_y = height // 2 - phr_h // 2

        text = font.render("Введите IP сервера (x.x.x.x:y):", 0, (100, 255, 100))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2 - phr.get_height() - 30

        msg = font.render(msg_text, 0, (100, 255, 100))
        msg_x = width // 2 - msg.get_width() // 2
        msg_y = height // 2 - msg.get_height() // 2 + phr.get_height() + 30

        screen.fill((0, 0, 0))
        screen.blit(text, (text_x, text_y))
        screen.blit(phr, (phr_x, phr_y))
        screen.blit(msg, (msg_x, msg_y))
        pygame.draw.rect(screen, (0, 255, 0), (phr_x - 10, phr_y - 10,
                                               phr_w + 20, phr_h + 20), 1)

    if state == 3:  # Игра
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sock_send(sockOut, '0')
                break
        keys = pygame.key.get_pressed()
        # print(keys if any(keys) else '')
        #coords = list()
        bullets = list()  # todo:мусор
        enemies = list()  # todo:мусор
        if messages:
            print(messages)
            print(messages[0][0])
            #coords = [tuple(map(int, coord.split('_'))) for coord in messages[0][0].split()]
            data = messages[0][0].split()
            print(data)
            x, y, hp, d = int(float(data.pop(0))), int(float(data.pop(0))), int(data.pop(0)), data.pop(0)  # todo:мусор
            for i in range(int(data.pop(0))):  # todo:мусор
                bullets.append((int(float(data.pop(0))), int(float(data.pop(0)))))
            for i in range(int(data.pop(0))):  # todo:мусор
                enemies.append((int(data.pop(0)), int(data.pop(0)), data.pop(0)))
            messages.clear()
        sock_send(sockOut, '2 ' + ''.join(map(str, keys)))
        screen.blit(game_background, (0, 0))
        player = pygame.Surface((30, 50))
        player.fill((0, 0, 255))
        screen.blit(player, (x, y))  # todo:мусор
        for i in bullets:  # todo:мусор
            bullet = pygame.Surface((10, 5))
            bullet.fill((100, 100, 100))
            screen.blit(bullet, (i[0], i[1]))
        for i in enemies:  # todo:мусор
            enemy = pygame.Surface((30, 50))
            enemy.fill((255, 0, 0))
            screen.blit((i[0], i[1]), enemy)
    pygame.display.flip()
    cl.tick(FPS)

t1.join()
close_sock(sockIn)
close_sock(sockOut)
pygame.quit()

import pygame
from source.web import *
pygame.init()
size = width, height = 1280, 800
screen = pygame.display.set_mode(size)
running = True
FPS = 60
cl = pygame.time.Clock()

ip = ''
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 8:  # backspace
                ip = ip[:-1]
                continue
            if event.key == 13:  # enter
                try:
                    sockOut = connect_OutSocket(address=ip.split(':')[0], port=int(ip.split(':')[1]))
                    sockIn = connect_InSocket(port=5556)
                    continue

                except socket.gaierror:  # todo: написать вывод сообщений об ошибке
                    continue
                except (IndexError, ValueError):
                    continue
                except OSError as e:
                    if e.errno == 10048:
                        print('вы уже подключенны к серверу')
            ip = ip + event.unicode
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

    screen.fill((0, 0, 0))
    screen.blit(text, (text_x, text_y))
    screen.blit(phr, (phr_x, phr_y))
    pygame.draw.rect(screen, (0, 255, 0), (phr_x - 10, phr_y - 10,
                                           phr_w + 20, phr_h + 20), 1)
    pygame.display.flip()
    cl.tick(FPS)





while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        sock_send(sockOut, event)
    print(read_sock(sockIn))
    screen.fill((0, 0, 0))
    pygame.display.flip()
    cl.tick(FPS)


close_sock(sockOut)
close_sock(sockIn)
pygame.quit()




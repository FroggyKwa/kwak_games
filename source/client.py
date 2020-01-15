import pygame
from source.web import connect_InSocket, connect_OutSocket, read_sock, sock_send, close_sock

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
running = True
fps = 60
sockOut = connect_OutSocket()
sockIn = connect_InSocket(port=5556)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        sock_send(sockOut, event)
    print(read_sock(sockIn))
    screen.fill((0, 0, 0))
    pygame.display.flip()
close_sock(sockOut)
close_sock(sockIn)
pygame.quit()


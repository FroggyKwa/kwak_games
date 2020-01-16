import json
import socket

import pygame
import uuid


JUMP_POWER = 10
GRAVITY = 0.35
MOVE_SPEED = 7


class Player(pygame.sprite.Sprite):
    def __init__(self, x0, y0, addr, udp_port):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(pygame.color.Color('Red'))
        self.rect = self.image.get_rect()
        self.x_velocity = 0
        self.y_velocity = 0
        self.id = str(uuid.uuid4())
        self.udp_addr = (addr[0], int(udp_port))
        self.hp = 100
        self.onGround = False
        self.update(x0, y0)

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def move(self, direction=None):
        if not direction:
            self.x_velocity = 0
        if direction == 'up':
            if self.onGround:
                self.y_velocity = -JUMP_POWER
                self.onGround = True
            if not self.onGround:
                self.y_velocity += GRAVITY
        if direction == 'left':
            self.x_velocity = -MOVE_SPEED
        if direction == 'right':
            self.x_velocity = MOVE_SPEED

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def get_damage(self, dmg):
        self.hp -= dmg if self.hp >= dmg else self.hp

    def send_udp(self, player_identifier, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps({player_identifier: message}), self.udp_addr)

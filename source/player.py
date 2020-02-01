import pygame
from source import *

JUMP_POWER = 20
GRAVITY = 0.5
MOVE_SPEED = 5
IMAGE_PATH = '../resources/player/'


class Player(pygame.sprite.Sprite):
    def __init__(self, x0, y0, socket=None, screen=None, *groups):
        super().__init__(*groups)
        self.screen = screen
        self.cnt = 1
        self.direction = 'right'
        self.state = 'idle'  # состояние героя, изменяется на сервере
        self.cur_image = 0
        self.image = self.change_image() if self.screen else None
        self.rect = self.image.get_rect() if self.image else pygame.Surface((20, 30)).get_rect()
        self.update(x0, y0)
        self.x_velocity = 0
        self.y_velocity = 0
        self.ip = None
        self.sock = socket
        self.hp = 100
        self.onGround = True
        self.shooting = False
        self.cur_shoot_time = 0

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

    def change_image(self):
        self.cur_image %= count_sprites[self.state]
        self.cur_image += 1
        image = pygame.image.load(IMAGE_PATH + f'{self.state}/{self.state}-{self.cur_image}.png').convert_alpha(
            self.screen)
        if self.direction == 'left':
            image = pygame.transform.flip(image, True, False)
        return image

    def change_velocity(self, direction=None):
        if not direction:
            self.x_velocity = 0
        if direction == 'up':
            if self.onGround:
                self.y_velocity = -JUMP_POWER
                self.onGround = False
        if direction == 'left':
            self.x_velocity = -MOVE_SPEED
        if direction == 'right':
            self.x_velocity = MOVE_SPEED
        if not self.onGround:
            self.y_velocity += GRAVITY if self.y_velocity <= 5 else 0

    def move(self):
        self.y = self.y + self.y_velocity
        self.x = self.x + self.x_velocity

    def get_damage(self, dmg):
        self.hp -= dmg if self.hp >= dmg else self.hp

import pygame
from source import *

JUMP_POWER = 15
GRAVITY = 0.3
MOVE_SPEED = 3
IMAGE_PATH = '../resources/player/'


class Player(pygame.sprite.Sprite):
    def __init__(self, x0, y0, socket=None, state='idle', direction='right', *groups):
        super().__init__(*groups)
        self.cnt = 1
        self.direction = direction
        self.state = state  # состояние героя, изменяется на сервере
        self.x = x0
        self.y = y0
        self.cur_image = 0
        self.change_image()
        self.rect = self.image.get_rect() if self.image else pygame.Surface((20, 30)).get_rect()
        self.update(x0, y0)
        self.x_velocity = 0
        self.y_velocity = 0
        self.ip = None
        self.sock = socket
        self.hp = 100
        self.onGround = False
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
        image = pygame.image.load(IMAGE_PATH + f'{self.state}/{self.state}-{self.cur_image}.png').convert_alpha()
        if self.direction == 'left':
            image = pygame.transform.flip(image, True, False)
        self.image = image
        self.rect = self.image.get_rect()
        self.update(self.x, self.y)

    def change_velocity(self, direction=None):
        if not direction:
            self.x_velocity = 0
        if direction == 'up':
            if self.onGround:
                self.y_velocity = -JUMP_POWER
                self.onGround = False
        if direction == 'left':
            self.x_velocity = -MOVE_SPEED
            self.image = pygame.transform.flip(self.image, True, False)
        if direction == 'right':
            self.x_velocity = MOVE_SPEED
        if not self.onGround:
            self.y_velocity += GRAVITY if self.y_velocity <= 3 else 0
        else:
            self.y_velocity = 0

    def move(self, group):
        self.y = self.y + self.y_velocity
        self.update(self.x, self.y)
        spr = None
        for i in group:
            if pygame.sprite.collide_mask(self, i):
                spr = i
                break
        if spr is not None:
            self.y = spr.rect.y - self.rect.height + 3
            self.onGround = True
        else:
            self.onGround = False
        self.update(self.x, self.y)
        self.x = self.x + self.x_velocity

    def get_damage(self, dmg):
        self.hp -= dmg if self.hp >= dmg else self.hp

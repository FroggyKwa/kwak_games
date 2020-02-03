import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, screen, *groups):
        super().__init__(groups)
        self.screen = screen
        self.image = None


class Platform(Entity):
    def __init__(self, screen, x, y, filename, *groups):
        super().__init__(screen, groups)
        self.cnt = 1
        self.image = filename if filename is not str \
            else pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Bullet(Entity):
    def __init__(self, screen, x, y, direction='right', owner=None):
        super().__init__(screen)
        self.cnt = 1
        self.owner = owner
        self.image = pygame.image.load(
            '../resources/misc/shot/shot-1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.lifespan = 180
        self.direction = direction

    def move(self):
        self.rect.x += 5 if self.direction == 'right' else -5
        self.lifespan -= 1
        self.image = pygame.image.load(
            f'../resources/misc/shot/shot-{(self.cnt % 3) + 1}.png').convert_alpha()
        self.screen.blit(self.image, self.rect)
        self.cnt += 1
        if not self.lifespan:
            self.kill()

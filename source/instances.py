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
        self.image = filename if filename is not str\
            else pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        print(self.rect)


class Bullet(Entity):
    def __init__(self, screen, x, y, dir):
        super().__init__(screen)
        self.cnt = 1
        self.image = pygame.image.load('../source/resources/warped city files/SPRITES/misc/shot/shot-1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.lifespan = 180
        self.direction = dir

    def move(self):
        self.rect.x += 20 if self.direction == 'right' else -20
        self.lifespan -= 1
        self.image = pygame.image.load(
            f'../source/resources/warped city files/SPRITES/misc/shot/shot-{(self.cnt % 3) + 1}.png').convert_alpha()
        self.screen.blit(self.image, self.rect)
        if not self.lifespan:
            self.kill()
#b = Bullet(pygame.display.set_mode((1280, 800)), 0, 0, 'тебе ли не пофиг куда ты смотришь')

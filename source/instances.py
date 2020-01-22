import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.image = None
        self.rect = self.image.get_rect() if self.image else None


class Player(Entity):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen
        self.cnt = 1
        self.image = pygame.image.load('../resources/warped city files/SPRITES/player/walk/walk-1.png').convert_alpha()

    def update(self, x, y):
        self.rect.x, self.rect.y = x, y
        self.cnt += 1
        self.image = pygame.image.load(
            f'../resources/warped city files/SPRITES/player/walk/walk-{(self.cnt % 9) + 1}.png').convert_alpha()
        self.screen.blit(self.image, self.rect)


class Bullet(Entity):
    def __init__(self, screen):
        super().__init__(screen)
        self.cnt = 1
        self.image = pygame.image.load('../resources/warped city files/SPRITES/misc/shot/shot-1.png').convert_alpha()

    def update(self, x, y):
        self.rect.x, self.rect.y = x, y
        self.cnt += 1
        self.image = pygame.image.load(
            f'../resources/warped city files/SPRITES/misc/shot/shot-{(self.cnt % 3) + 1}.png').convert_alpha()
        self.screen.blit(self.image, self.rect)



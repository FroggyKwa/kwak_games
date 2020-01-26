import pygame


class Camera:
    def __init__(self, width, height, size):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.size_width = size[0]
        self.size_height = size[1]

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(self.size_width / 2)
        y = -target.rect.y + int(self.size_height / 2)

        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - self.size_width), x)  # right
        y = max(-(self.height - self.size_height), y)  # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)

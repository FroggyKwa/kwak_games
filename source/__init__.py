import pygame
import os

pygame.mixer.init()


def resolve_route(route_relative=''):
    return os.path.join(os.path.abspath("."), route_relative)


count_sprites = {
    "hurt": 1,
    "shoot": 1,
    "idle": 4,
    "jump": 4,
    "run": 8,
    "run-shoot": 8,
    "walk": 16

}

images = {
    "background": pygame.image.load(resolve_route("../resources\\background.png")),
    "bg_menu": pygame.image.load("../resources\\bg_for_menu.png")
}

sounds = {}

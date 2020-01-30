import pygame
import os

pygame.mixer.init()


def resolve_route(route_relative=''):
    return os.path.join(os.path.abspath("."), route_relative)


images = {
    "background": pygame.image.load(resolve_route("../resources\\background.png")),
    "player": pygame.image.load(resolve_route("../resources\\player\\walk\\walk-1.png")),
    "bg_menu": pygame.image.load("../resources\\bg_for_menu.png")
}

sounds = {}

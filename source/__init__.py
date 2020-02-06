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
    "background": pygame.image.load(resolve_route("../resources/background.png")),
    "bg_menu": pygame.image.load("../resources/bg_for_menu.png"),
    "training_image": pygame.image.load("../resources/training.png")
}
sounds = {"music_in_game": [pygame.mixer.Sound(resolve_route('../resources/music/game_music.wav'))],
          "music_in_menu": [pygame.mixer.Sound(resolve_route('../resources/music/menu_music.wav'))],
          "typing_sound": pygame.mixer.Sound(resolve_route('../resources/music/typing.wav')),
          }

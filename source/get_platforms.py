import pytmx
import pygame
from source.instances import *


def get_platforms_surface(name_of_map="../resources/maps/map.tmx"):
    surface = pygame.Surface((1280, 800), pygame.SRCALPHA, 32)
    gameMap = pytmx.load_pygame(name_of_map)
    for layer in gameMap.visible_layers:
        for x, y, gid, in layer:
            tile = gameMap.get_tile_image_by_gid(gid)
            try:
                surface.blit(tile, (x * gameMap.tilewidth,
                                    y * gameMap.tileheight))
            except:
                continue
    return surface.convert_alpha(surface)


def get_platforms(screen, group, name_of_map="../resources/maps/map.tmx"):
    surface = pygame.Surface((1280, 800), pygame.SRCALPHA, 32)
    gameMap = pytmx.load_pygame(name_of_map)
    for layer in gameMap.visible_layers:
        for x, y, gid, in layer:
            img = gameMap.get_tile_image_by_gid(gid)
            try:
                group.append(Platform(screen, x * gameMap.tilewidth, y * gameMap.tileheight, img))
            except:
                continue
    return surface

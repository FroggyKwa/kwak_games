import pytmx
import pygame


def get_platforms(name_of_map="../source/resources/maps/map.tmx"):
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

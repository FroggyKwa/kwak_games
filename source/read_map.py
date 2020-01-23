import pygame
import pytmx


def draw_map(surface, name_of_map="map.tmx"):
    gameMap = pytmx.load_pygame(name_of_map)
    for layer in gameMap.visible_layers:
        for x, y, gid, in layer:
            tile = gameMap.get_tile_image_by_gid(gid)
            try:
                surface.blit(tile, (x * gameMap.tilewidth,
                                    y * gameMap.tileheight))
            except:
                continue

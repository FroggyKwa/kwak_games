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


def read_map(name_of_map="map.tmx"):
    table_of_map = [[0 for _ in range(64)] for _ in range(40)]
    gameMap = pytmx.load_pygame(name_of_map)
    no_first = False
    for i in gameMap.visible_layers:
        if no_first:
            for x, y, gid in i:
                tile = gameMap.get_tile_image_by_gid(gid)
                if tile:
                    table_of_map[y][x] = 1
        else:
            no_first = True
    return table_of_map

import pytmx


def read_map(name_of_map="../source/resources/maps/map.tmx"):
    table_of_map = [[0 for _ in range(64)] for _ in range(40)]
    gameMap = pytmx.TiledMap(name_of_map)
    for i in gameMap.visible_layers:
        for x, y, gid in i:
            tile = gameMap.get_tile_image_by_gid(gid)
            if tile:
                table_of_map[y][x] = 1
    return table_of_map


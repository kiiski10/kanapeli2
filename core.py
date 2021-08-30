import math

def screenPosToTilePos(kana, tileMap, pos):
    return(
        (pos[0] + kana.location[0] + tileMap.tilewidth) // tileMap.tileheight,
        (pos[1] + kana.location[1] + tileMap.tilewidth) // tileMap.tileheight,
    )

def tilePosToScreenPos(kana, tileMap, pos):
    x = pos[0] * tileMap.tilewidth - kana.location[0] - tileMap.tileheight
    y = pos[1] * tileMap.tileheight- kana.location[1] - tileMap.tileheight
    return(x, y)

def distance(start, end):
    return math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)
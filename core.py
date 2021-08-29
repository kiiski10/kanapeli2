
def screenPosToTilePos(kana, tileMap, pos):
    return(
        (pos[0] + kana.location[0] + tileMap.tilewidth / 2) // tileMap.tilewidth,
        (pos[1] + kana.location[1] + tileMap.tilewidth / 2) // tileMap.tileheight
    )

def tilePosToScreenPos(kana, tileMap, pos):
    x = pos[0] * tileMap.tilewidth - kana.location[0]
    y = pos[1] * tileMap.tileheight - kana.location[1]
    #print("TILE POS -> SCREEN POS:", pos, "->", x,y)
    return(x, y)

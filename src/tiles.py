import pygame

class Tile(pygame.sprite.DirtySprite):
    
    def __init__(self, type, x, y, visible = 1):
        # initalize
        pygame.sprite.DirtySprite.__init__(self)
        
        self.type = type
        self.x = x
        self.y = y
        self.visible = visible
        
    def __str__(self):
        return "{type} tile at x {x} y {y}".format(type=self.type, x=self.x, y=self.y)
    
    def __eq__(self, other):
        return self.type == other.type
    
    def __ne__(self, other):
        return sefl.type != other.type

class TileGroup(pygame.sprite.Group):
    
    def add(self, *sprites):
        for sprite in sprites:
            # check if the added sprites are Tiles.
            if isinstance(sprite, Tile):
                super.add(sprites)
            else:
                raise NotTile("The added sprite wasn't a Tile.") 
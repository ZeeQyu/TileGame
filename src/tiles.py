''' Module /src/tiles.py
    TileGame by ZeeQyu
    https://github.com/ZeeQyu/TileGame
    
    Module containing the tile class.
    Tiles are the main building block of the game world.
    They have a texture associated, the type attribute 
    corresponds to the constants.py IMAGES dictionary paths.
'''

import pygame

class Tile(object):
    ''' Tile object containing the type and location of the tile.
    '''
    
    def __init__(self, type, x, y):
        ''' Simple initalizer.
            "type" should be a string from the list of keys in the constants.py IMAGES dictionary.
            "x" and "y" should be ints and can be used for finding out where a tile belongs if
            you copy the tile away from the map array in main.py. They are not normally used.
        '''
        
        self.type = type
        self.x = x
        self.y = y
        
    def __str__(self):
        ''' Returns tile type and location (all attributes)
        '''
        return "{type} tile at x {x} y {y}".format(type=self.type, x=self.x, y=self.y)
    
    def __eq__(self, other):
        ''' Compares the type attribute
        '''
        return self.type == other.type
    
    def __ne__(self, other):
        ''' Compares the type attribute
        '''
        return self.type != other.type
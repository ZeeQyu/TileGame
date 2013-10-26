#!/usr/bin/env python
# coding=utf-8
''' Module /src/tiles.py
    TileGame by ZeeQyu
    https://github.com/ZeeQyu/TileGame
    
    Module containing the tile class.
    Tiles are the main building block of the game world.
    They have a texture associated, the type attribute 
    corresponds to the constants.py IMAGES dictionary paths.
'''

from random import choice
import pygame
from constants import *

class Tile(object):
    ''' Tile object containing the type and location of the tile.
    '''
    
    def __init__(self, type, x, y):
        ''' Simple initalizer.
            "type" should be a string from the list of keys in the constants.py IMAGES dictionary.
            "x" and "y" should be ints and can be used for finding out where a tile belongs if
            you copy the tile away from the map array in main.py. They are not normally used.
        '''
        # Type of tile, for identification purposes.
        # Can be accessed directly, but not for image getting purposes
        # get_image() should be used instead
        self.type = type
        self.x = x
        self.y = y
        
    def rect(self):
        ''' Returns a pygame.Rect object with the same dimensions and location as the tile
        '''
        return pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    
    def get_image(self):
        ''' Returns the image string which relates to the globals.images dictionary.
            Should be used when determining what image should be used.
            Only exists to be overwritten by subclasses
        '''
        return self.type
        
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
    
class RandomTile(Tile):
    ''' Subclass of Tile with code for random texture selection and preserving
    ''' 
    def __init__(self, type, x, y):
        ''' Initializes a tile with a random texture from the globals.images dict
        ''' 
        self.type = type
        self.x = x
        self.y = y
        
        # Randomly choose one of the textures with this name
        image_keys = []
        for key in IMAGES.keys():
            if key.find(type) != -1:
                image_keys.append(key)
        self.image = choice(image_keys)

    def get_image(self):
        ''' Returns the random texture string.
        ''' 
        return self.image
    
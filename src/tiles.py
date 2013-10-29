#!/usr/bin/env python
# coding=utf-8
''' Module /src/tiles.py
    TileGame
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Module containing the tile class.
    Tiles are the main building block of the game world.
    They have a texture associated, the type attribute 
    corresponds to the constants.py IMAGES dictionary paths.
'''

from random import choice, randint

import pygame

import constants, globals

class Tile(object):
    ''' Tile object containing the type and location of the tile.
    '''
    
    def __init__(self, type, x, y, timer=0):
        ''' Simple initalizer.
            "type" should be a string from the list of keys in the constants.py IMAGES dictionary.
            "x" and "y" should be ints and can be used for finding out where a tile belongs if
                you copy the tile away from the map array in main.py. They are not normally used.
            "timer" should be the time until time_up() is called. If this is the base class
        '''
        # Type of tile, for identification purposes.
        # Can be accessed directly, but not for image getting purposes
        # get_image() should be used instead
        self.type = type
        self.x = x
        self.y = y
        # Timer until some tiles "evolve"
        self.timer = timer
        
    def tick(self):
        ''' Method for counting down the block replacement timer.
            Should only be called if the tile is a transforming tile (for example, sapling)
        '''
        if self.timer < 0:
            self.time_up()
        self.timer -= 1
    
    def rect(self):
        ''' Returns a pygame.Rect object with the same dimensions and location as the tile
        '''
        return pygame.Rect(self.x * constants.TILE_SIZE, self.y * constants.TILE_SIZE,
                           constants.TILE_SIZE, constants.TILE_SIZE)
    
    def get_image(self):
        ''' Returns the image string which relates to the globals.images dictionary.
            Should be used when determining what image should be used.
            Only exists to be overwritten by subclasses like RandomTile.
        '''
        return self.type
    
    def time_up(self):
        ''' The function that should be called when self.timer has reached 0
            Exchanges this tile for the appropriate tile specified in the constants.IMAGES variable
        '''
        entity_tiles = []
        if constants.IMAGES[self.type].collides:
            for entity in globals.entity_list:
                entity_tiles.append(entity.get_tile())
        if (self.x, self.y) not in entity_tiles:
            if constants.IMAGES[self.type].evolve != None:
                globals.map[self.x][self.y] = make_tile(constants.IMAGES[self.type].evolve[2], self.x, self.y)
            globals.tick_tiles.remove([self.x, self.y])
            globals.update_map = True
        
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
    def __init__(self, type, x, y, timer=0):
        ''' Initializes a tile with one of the textures containing the type,
            for more varied visual impression.
        ''' 
        super(RandomTile, self).__init__(type, x, y, timer)
        
        # Randomly choose one of the textures with this name
        image_keys = []
        for key in constants.IMAGES.keys():
            if key.find(type) != -1:
                image_keys.append(key)
        self.image = choice(image_keys)

    def get_image(self):
        ''' Returns the random texture string.
        ''' 
        return self.image
    
def make_tile(type, x, y):
    ''' Function to create a tile of the appropriate type (Standard, Random and, later, multi-tile)
        Should be used instead of directly creating a specific tile unless it is certain which type
        is needed.
        
        "type" should be a string identifier from IMAGES.
        If it is a random tile, it should be the simplest form of the identifier
        (for example, "tree" and not "tree1"
        "x" and "y" are the indices of the tile in the "globals.map" array
    '''
    timer = 0
    # If the tile evolves, get a random timer for that and a replace_tile
    if constants.IMAGES[type].evolve != None:
        coordinates = [x, y]
        globals.tick_tiles.append(coordinates)
        timer = randint(*constants.IMAGES[type].evolve[:2])
        replace_tile = constants.IMAGES[type].evolve[2]
    # Random tiles
    if not constants.DEACTIVATE_RANDOM_TEXTURES:
        if constants.IMAGES[type].random:
            return RandomTile(type, x, y, timer)
        else:
            return Tile(type, x, y, timer)
    else:
        return Tile(type, x, y, timer)
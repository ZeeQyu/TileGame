#!/usr/bin/env python
# coding=utf-8
""" Module /src/tiles.py
    TileGame for Python 3
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Module containing the tile class.
    Tiles are the main building block of the game world.
    They have a texture associated, the type attribute 
    corresponds to the c.py IMAGES dictionary paths.
"""
import os, sys
from random import choice, randint

import pygame

sys.path.append(os.path.join(os.getcwd(), "sys"))
import entities, units
import globals as g
import constants as c
class AreaNotFreeException(Exception):
    """ Is thrown if a multitile is placed in a non-free spot. The spot should always be checked before
        make_tile() is called.
    """
    pass

class Tile(object):
    """ Tile object containing the type and location of the tile.
    """
    
    def __init__(self, type, x, y):
        """ Simple initalizer.
            "type" should be a string from the list of keys in the c.py IMAGES dictionary.
            "x" and "y" should be ints and can be used for finding out where a tile belongs if
                you copy the tile away from the map array in main.py. They are not normally used.
            "timer" should be the time until time_up() is called. If this is the base class
        """
        # Type of tile, for identification purposes.
        # Can be accessed directly, but not for image getting purposes
        # get_image() should be used instead
        self.type = type
        self.x = x
        self.y = y
        # If the tile evolves, get a random timer for that
        if c.IMAGES[type].evolve != None:
            g.tick_tiles.append([x, y])
            self.timer = randint(*c.IMAGES[type].evolve[:2])
        else:
            self.timer = 0          

        if c.IMAGES[type].random:
            image_keys = []
            for image in list(c.IMAGES.keys()):
                if image.startswith(type) and (image[len(type):].isdigit() or len(image) == len(type)):
                    image_keys.append(image)
            self.image = choice(image_keys)
        else:
            self.image = self.type 
        
    def tick(self):
        """ Method for counting down the block replacement timer.
            Should only be called if the tile is a transforming tile (for example, sapling)
        """
        if self.timer < 0:
            self.time_up()
        else:
            self.timer -= 1
    
    def rect(self):
        """ Returns a pygame.Rect object with the same dimensions and location as the tile
        """
        return pygame.Rect(self.x * c.TILE_SIZE, self.y * c.TILE_SIZE,
                           c.TILE_SIZE, c.TILE_SIZE)
    
    def get_image(self):
        """ Returns the random texture string or just the image
        """ 
        return self.image

    
    def time_up(self):
        """ The function that should be called when self.timer has reached 0
            Exchanges this tile for the appropriate tile specified in the c.IMAGES variable
        """
        # Check if the entity evolves
        if c.IMAGES[self.type].evolve != None:
            has_entities = False
            # Check if any entity is on that tile
            if c.IMAGES[c.IMAGES[self.type].evolve[2]].collides:
                has_entities = not entities.free_of_entities(self)
            if not has_entities:
                make_tile(c.IMAGES[self.type].evolve[2], self.x, self.y)
                g.tick_tiles.remove([self.x, self.y])
                return
        else:
            g.tick_tiles.remove([self.x, self.y])
        
    def __str__(self):
        """ Returns tile type and location (all attributes)
        """
        template = "{id} tile of type {type} at x {x} y {y} with evolve timer {timer}"
        return template.format(id=self.type, x=self.x, y=self.y,
                               type=type(self), timer=self.timer)
    
    def __eq__(self, other):
        """ Compares the type attribute
        """
        return self.type == other.type
    
    def __ne__(self, other):
        """ Compares the type attribute
        """
        return self.type != other.type

class MultiTileHead(Tile):
    """ The top-left tile of any multi-tile. Paints the actual image
    """
    def __init__(self, type, x, y, width, height):
        super(MultiTileHead, self).__init__(type, x, y)
        self.width = width
        self.height = height
    
class MultiTilePointer(Tile):
    """ The other tiles that aren't the head in a multi-tile. Paints a single, empty pixel.
    """
    def __init__(self, type, x, y, head_x, head_y):
        super(MultiTilePointer, self).__init__(type, x, y)
        self.target = head_x, head_y
        
    def __str__(self):
        """ Returns the normal values and the coordinates of the head.
        """
        template = "{id} tile of type {type} at x {x} y {y} pointing at {target}"
        return template.format(id=self.type, x=self.x, y=self.y,
                               type=type(self), target=self.target)
        
def area_is_free(x, y, width, height):
    """ Checks an area for if a multitile can be placed there
        "x" and "y" is the top left corner tile in the area.
        "width" and "height" is the width and height of the area 
            to be checked. 
    """
    is_free = True
#     for key in g.special_entity_list.keys():
#         if "areapackage" in key:
#             del g.special_entity_list[key]
    for i in range(x, x+width):
        for j in range(y, y+height):
            # If any of the tiles aren't placeable, it isn't free.
            if c.IMAGES[g.map[i][j].type].placeable == False:
                is_free = False
            else:
#                 units.Package(i * c.TILE_SIZE, j * c.TILE_SIZE, custom_name="areapackage" + str(i) + "." + str(j))
                pass
            if not entities.free_of_entities(g.map[i][j]):
                is_free = False
    return is_free
    
def make_tile(type, x, y, target=None):
    """ Function to create a tile of the appropriate type (Standard, Random and multi-tile)
        Should be used instead of directly creating a specific tile unless it is certain which type
        is needed.
        
        "type" should be a string identifier from IMAGES.
            If it is a random tile, it should be the base form of the identifier
            (for example, "tree" and not "tree1"
        "x" and "y" are the indices of the tile in the "g.map" array
        "target" should be a tuple of coordinates in the tile array if the tile being created is
            a pointer. It should be left empty if the tile isn't a multi-tile pointer.
    """
  
    # Check if where you're placing the tile is subject to a special tile.
    if g.map[x][y]:
        if c.SPECIAL_PLACE_TILES.__contains__(type + "+" + str(g.map[x][y].type)):
            return make_tile(c.SPECIAL_PLACE_TILES[type + "+" + str(g.map[x][y].type)], x, y)

    # If it is a multi-tile
    if c.IMAGES[type].multi_tile != None:
        width, height = c.IMAGES[type].multi_tile
        if not area_is_free(x, y, width, height):
            raise AreaNotFreeException("The area at x " + x + ", y " + y +
                                       ", with the width " + width + " and the height " +
                                       height + " was not placeable. Please check the area " +
                                       "before attempting to create a multi-tile.")
        # Create pointers
        for i in range(x, x + width):
            for j in range(y, y + height):
                # If it's the top-left tile, skip it
                if x == i and y == j:
                    continue
                # On all others, make pointers
                if c.IMAGES[type].collides:
                    make_tile("collide_pointer", i, j, (x, y))
                else:
                    make_tile("pointer", i, j, (x, y))
        
        tile = MultiTileHead(type, x, y, width, height)
    else:
        timer = 0
        # Check if target was specified. If so, this tile is a pointer.
        if target != None:
            tile = MultiTilePointer(type, x, y, *target)
        else:
            tile = Tile(type, x, y)
    # Change and update the map
    g.map[x][y] = tile
    g.update_map = True
    return tile 
    
def destroy_tile(x, y):
    # If the old tile was a multitile head or pointer
    if (g.map[x][y] and (type(g.map[x][y]) == MultiTileHead or
            type(g.map[x][y]) == MultiTilePointer)):
        # Get the destroy value
        if type(g.map[x][y]) == MultiTileHead:
            destroy_value = c.IMAGES[g.map[x][y].type].destroy
            multi_tile = {"x": x, "y": y,
                          "width": g.map[x][y].width,
                          "height": g.map[x][y].height} 
        else:
            target_x, target_y = g.map[x][y].target
            destroy_value = c.IMAGES[g.map[target_x][target_y].type].destroy
            try:
                multi_tile = {"x": target_x, "y": target_y,
                              "width": g.map[target_x][target_y].width,
                              "height": g.map[target_x][target_y].height}
            except:
                 import pdb, sys
                 e, m, tb = sys.exc_info()
                 pdb.post_mortem(tb)
        for i in range(multi_tile["x"], multi_tile["x"] + multi_tile["width"]):
            for j in range(multi_tile["y"], multi_tile["y"] + multi_tile["height"]):
                if i == x and j == y:
                    continue
                if len(destroy_value) > 2:
                    make_tile(destroy_value[2], i, j)
                else:
                    make_tile(destroy_value[1], i, j)
        make_tile(destroy_value[1], x, y)
    else:
        make_tile(c.IMAGES[g.map[x][y].type].destroy[1], x, y)
        
#!/usr/bin/env python
# coding=utf-8
''' Module /src/maps.py
    TileGame
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Module for handling loading and painting of the map.
    The map is the multidimensional array of tiles 
    which is used for painting the game world on the screen.
    It can be edited easily by replacing an index with a new tile instance.
'''
import pygame

import constants
import tiles
import globals

def generate_map():
    ''' Function that loads a PIL image and reads it, pixel by pixel, to decode it into a tile map. 
        
        Gets the map from the constants.IMAGES["map"] object.
        Sets a map (two-dimensional list of Tiles), the width and height of the image loaded 
        and the player starting point, x and y, from the file as variables in the globals module.
        (5 items) If no starting point is found, return 0, 0 as the starting point. 
    '''
    # Load the image
    map_image = pygame.image.load("res\\" + constants.IMAGES["map"].png)
    globals.map = []
    # Variable for holding multi_tiles until after the primary generation, because 
    multi_tiles = []
    width, height = map_image.get_size()
    player_start_x = 0
    player_start_y = 0
    
    for x in range(width):
        # Create a new vertical column for every pixel the image is wide.
        globals.map.append([])
        for y in range(height):
            # The pixel variable is the pixel we're currently checking.
            pixel = map_image.get_at((x, y))[:3]
            type = pixel_type(pixel, x, y)
            # If the pixel is the player start tile, save the location of that pixel.
            if type == "start_tile":
                player_start_x = x * constants.TILE_SIZE
                player_start_y = y * constants.TILE_SIZE
                type = constants.DEFAULT_TILE
            # Check to see if it's a multi-tile and, if so, store that in a variable to be done last
            globals.map[x].append(None)
            if constants.IMAGES[type].multi_tile:
                multi_tiles.append([type, x, y])
                tiles.make_tile(constants.DEFAULT_TILE, x, y)
            else:
                # Make a new tile and add it to the map
                tiles.make_tile(type, x, y)
            
    # Sets the values to the global values
    globals.width = width
    globals.height = height
    globals.player_start_x = player_start_x
    globals.player_start_y = player_start_y
    
    # Create the multi-tiles
#     for multi_tile in multi_tiles:
#         type, x, y = multi_tile
#         width, height = constants.IMAGES[type].multi_tile
#         if (globals.map[x][y] and globals.map[x][y].type == constants.DEFAULT_TILE and 
#                 tiles.area_is_free(x, y, width, height)):
#             tiles.make_tile(type, x, y)
    
def pixel_type(pixel, x, y):
    ''' Function for checking a pixel color code and from that figuring out which kind of tile should go to that index in the map.
        Finds the color codes in the the constants.py IMAGES dictionary. If the color code is just 0, don't check that image.
        
        "pixel" should be a value in a pixel access object from PIL, which is a RGB value in a tuple.
        "x" and "y" are coordinates of the pixel in the pixel access object, for debugging purposes.
    '''
    for key in constants.IMAGES:
        # if the RGB value actually exists (and as such it is a tile)
        if constants.IMAGES[key].color_code != None:
            # if the RGB value was found, return the key of that entry.
            if pixel == constants.IMAGES[key].color_code:
                return key
    # If no match was found, make the spot the standard tile and print a message containing the RGB 
    print "The pixel at x:", x, "y:", y, "in the map file is not a valid color. The RGB is", str(pixel)
    return constants.DEFAULT_TILE
    
def paint_map(screen):
    ''' Iterates through the map and paints all the tiles in that map on the screen.
        
        Uses variables from globals.py and constants.py
         
        DEPRECATED! use update_map and screen.blit instead! (Much quicker as it doesn't
            have to update the entire screen every frame then)
    '''
    globals.screen.fill(constants.BLACK)
    for i in range(len(map)):
        for j in range(len(map[i])):
            image = images[map[i][j].type()].get()
            screen.blit(image, (i*TILE_SIZE, j*TILE_SIZE))
            
def update_map():
    ''' Iterates through the map and paints all the tiles in that map in a surface object
        returns that pygame.Surface object
        
        uses variables from the globals and constants files
    '''
    map_screen_buffer = pygame.Surface((len(globals.map)*constants.TILE_SIZE, len(globals.map[1])*constants.TILE_SIZE))
    
    map_screen_buffer.fill(constants.BACKGROUND_COLOR)
    for i in range(len(globals.map)):
        for j in range(len(globals.map[i])):
            try:
                image = globals.images[globals.map[i][j].get_image()].get()
            except:
                import pdb, sys
                e, m, tb = sys.exc_info()
                pdb.post_mortem(tb)
            map_screen_buffer.blit(image, (i*constants.TILE_SIZE, j*constants.TILE_SIZE))
            
    return map_screen_buffer


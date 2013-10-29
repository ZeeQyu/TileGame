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
    
    This module uses PIL for loading the map.png and reading individual pixels.
    Note that graphics.py uses the pygame built-in image library instead.
'''

import Image
from pygame import Surface

import constants
import tiles
import globals

class InvalidMapColorException(Exception):
    ''' Exception sub-class for fancy error messages
    
        Used when you have an invalid color in the map.png that isn't specified in the constants.py IMAGES dictionary.
        Used in the pixel_type() function in this module.
    '''
    pass

def generate_map(map_name):
    ''' Function that loads a PIL image and reads it, pixel by pixel, to decode it into a tile map. 
        
        "map_name" should be a file name in the res folder.
        returns a map (two-dimensional list of Tiles), the width and height of the image loaded 
        and the player starting point, x and y, from the file. (5 items)
        if no starting point is found, return 0, 0 as the starting point. 
    '''
    # Load the image and declare variables
    map_image = Image.open("res\\" + map_name)
    pixels = map_image.load()
    map = []
    width, height = map_image.size
    player_start_x = 0
    player_start_y = 0
    
    for x in range(width):
        map.append([]) # Create a new vertical column for every pixel the image is wide.
        
        for y in range(height):
            pixel = pixels[x, y] # The pixel variable is the pixel we're currently checking.
            type = pixel_type(pixel, x, y)
            if type == "start_tile":    # If the pixel is the player start tile, save the location of that pixel.
                player_start_x = x * constants.TILE_SIZE
                player_start_y = y * constants.TILE_SIZE
            
            # Make a new tile and add it to the map
            tile = tiles.make_tile(type, x, y)
            map[x].append(tile)
            
    # Return the map, image size (for size of windows) and player start point
    return map, width, height, player_start_x, player_start_y
    
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
         
        DEPRECATED! use update_map and screen.blit instead! (Much quicker)
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
    map_screen_buffer = Surface((len(globals.map)*constants.TILE_SIZE, len(globals.map[1])*constants.TILE_SIZE))
    
    map_screen_buffer.fill(constants.BACKGROUND_COLOR)
    for i in range(len(globals.map)):
        for j in range(len(globals.map[i])):
            image = globals.images[globals.map[i][j].get_image()].get()
            map_screen_buffer.blit(image, (i*constants.TILE_SIZE, j*constants.TILE_SIZE))
            
    return map_screen_buffer


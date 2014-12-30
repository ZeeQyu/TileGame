#!/usr/bin/env python
# coding=utf-8
""" Module /src/maps.py
    TileGame for Python 3
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Module for handling loading and painting of the map.
    The map is the multidimensional array of tiles 
    which is used for painting the game world on the screen.
    It can be edited easily by replacing an index with a new tile instance.
"""
import os, sys
import random

import pygame

sys.path.append(os.path.join(os.getcwd(), "sys"))
import tiles
import constants as c
import globals as g


def load_map(map_image=None):
    """ Function that loads a PIL image and reads it, pixel by pixel, to decode it into a tile map. 
        
        Gets the map from the c.IMAGES["map"] object.
        Sets a map (two-dimensional list of Tiles), the width and height of the image loaded 
        and the player starting point, x and y, from the file as variables in the g module.
        (5 items) If no starting point is found, return 0, 0 as the starting point. 
    """
    if map_image is None:
        # Load the image
        map_image = pygame.image.load(os.path.join(os.getcwd(), c.RES_FOLDER, c.IMAGES["map"].png))

    g.map = []
    # Variable for holding multi_tiles until after the primary generation.
    multi_tiles = []
    width, height = map_image.get_size()
    player_start_x = 0
    player_start_y = 0
    
    for x in range(width):
        # Create a new vertical column for every pixel the image is wide.
        g.map.append([])
        for y in range(height):
            # The pixel variable is the pixel we're currently checking.
            pixel = map_image.get_at((x, y))[:3]
            px_type = pixel_type(pixel, x, y)
            # If the pixel is the player start tile, save the location of that pixel.
            if px_type == "start_tile":
                player_start_x = x * c.TILE_SIZE
                player_start_y = y * c.TILE_SIZE
                px_type = c.DEFAULT_TILE
            # Check to see if it's a multi-tile and, if so, store that in a variable to be done last
            g.map[x].append(None)
            if c.IMAGES[px_type].multi_tile:
                multi_tiles.append([px_type, x, y])
                tiles.make_tile(c.DEFAULT_TILE, x, y)
            else:
                # Make a new tile and add it to the map
                tiles.make_tile(px_type, x, y)
            
    # Sets the values to the global values
    g.width = width
    g.height = height
    g.player_start_x = player_start_x
    g.player_start_y = player_start_y
    
    # Create the multi-tiles
    for multi_tile in multi_tiles:
        px_type, x, y = multi_tile
        width, height = c.IMAGES[px_type].multi_tile
        if (g.map[x][y] and g.map[x][y].type == c.DEFAULT_TILE and 
                tiles.area_is_free(x, y, width, height)):
            tiles.make_tile(px_type, x, y)
    

def pixel_type(pixel, x, y):
    """ Function for checking a pixel color code and from that figuring out which kind of tile should go to that index in the map.
        Finds the color codes in the the c.py IMAGES dictionary. If the color code is just 0, don't check that image.
        
        "pixel" should be a value in a pixel access object from PIL, which is a RGB value in a tuple.
        "x" and "y" are coordinates of the pixel in the pixel access object, for debugging purposes.
    """
    for key in c.IMAGES:
        # if the RGB value actually exists (and as such it is a tile)
        if c.IMAGES[key].color_code != None:
            # if the RGB value was found, return the key of that entry.
            if pixel == c.IMAGES[key].color_code:
                return key
    # If no match was found, make the spot the standard tile and print a message containing the RGB 
    print("The pixel at x:", x, "y:", y, "in the map file is not a valid color. The RGB is", str(pixel))
    return c.DEFAULT_TILE
    

def paint_map(screen):
    """ Iterates through the map and paints all the tiles in that map on the screen.
        
        Uses variables from g.py and c.py
         
        DEPRECATED! use update_map and screen.blit instead! (Much quicker as it doesn't
            have to update the entire screen every frame then)
    """
    g.screen.fill(c.BLACK)
    for i in range(len(g.map)):
        for j in range(len(g.map[i])):
            image = c.images[g.map[i][j].type()].get()
            screen.blit(image, (i*c.TILE_SIZE, j*c.TILE_SIZE))
            

def update_map():
    """ Iterates through the map and paints all the tiles in that map in a surface object
        returns that pygame.Surface object
    """

    map_screen_buffer = pygame.Surface((len(g.map)*c.TILE_SIZE, len(g.map[1])*c.TILE_SIZE))
    
    map_screen_buffer.fill(c.BACKGROUND_COLOR)
    for i in range(len(g.map)):
        for j in range(len(g.map[i])):
            try:
                image = g.images[g.map[i][j].get_image()].get()
            except:
                import pdb, sys
                e, m, tb = sys.exc_info()
                pdb.post_mortem(tb)
            map_screen_buffer.blit(image, (i*c.TILE_SIZE, j*c.TILE_SIZE))
            
    return map_screen_buffer


def generate_map():
    """ Map generation function using cellular automata
    """
    return_image = pygame.Surface(c.GEN_MAP_SIZE)
    return_image.fill(c.IMAGES["grass"].color_code)
    for i in range(return_image.get_width()):
        for j in range(return_image.get_width()):
            random_number = random.randint(1, 1000)
            if random_number <= c.GEN_TREE_PER_MILLE:
                return_image.set_at((i, j), c.IMAGES["tree"].color_code)
            elif random_number >= 1000 - c.GEN_ORE_PER_MILLE:
                return_image.set_at((i, j), c.IMAGES["ore"].color_code)
            elif random_number >= 1000 - c.GEN_ORE_PER_MILLE - c.GEN_ROCK_PER_MILLE:
                return_image.set_at((i, j), c.IMAGES["rock"].color_code)
            else:
                return_image.set_at((i, j), c.IMAGES["grass"].color_code)
    for i in range(c.GEN_ITERATIONS):
        return_image = _iterate_generation(return_image)

    for i in range(c.GEN_ROCK_ITERATIONS):
        return_image = _iterate_rocks(return_image)

    # Put out a random endless package in the middle
    return_image.set_at((return_image.get_width() // 2, return_image.get_height() // 2),
                        c.IMAGES["endless_package"].color_code)
    return_image.set_at((return_image.get_width() // 2 + 1, return_image.get_height() // 2),
                        c.IMAGES["start_tile"].color_code)
    return return_image


def _yield_image_conversion(return_image):
    # Put out a random endless package in the middle
    return_image.set_at((return_image.get_width() // 2, return_image.get_height() // 2),
                        c.IMAGES["endless_package"].color_code)
    return_image.set_at((return_image.get_width() // 2 + 1, return_image.get_height() // 2),
                        c.IMAGES["start_tile"].color_code)
    return return_image


def generate_map_generator():
    """ A generator version for the cellular automata function above that lets the player
        step through the stages of generation of the maps.
    """
    return_image = pygame.Surface(c.GEN_MAP_SIZE)
    return_image.fill(c.IMAGES["grass"].color_code)
    for i in range(return_image.get_width()):
        for j in range(return_image.get_width()):
            random_number = random.randint(1, 1000)
            if random_number <= c.GEN_TREE_PER_MILLE:
                return_image.set_at((i, j), c.IMAGES["tree"].color_code)
            elif random_number >= 1000 - c.GEN_ORE_PER_MILLE:
                return_image.set_at((i, j), c.IMAGES["ore"].color_code)
            elif random_number >= 1000 - c.GEN_ORE_PER_MILLE - c.GEN_ROCK_PER_MILLE:
                return_image.set_at((i, j), c.IMAGES["rock"].color_code)
            else:
                return_image.set_at((i, j), c.IMAGES["grass"].color_code)

    yield _yield_image_conversion(return_image)

    for i in range(c.GEN_ITERATIONS):
        return_image = _iterate_generation(return_image)
        yield _yield_image_conversion(return_image)

    for i in range(c.GEN_ROCK_ITERATIONS):
        return_image = _iterate_rocks(return_image)
        yield _yield_image_conversion(return_image)


map_image = None


def _iterate_generation(passed_image):
    """ Function for iteratively making the generated area more smooth and evolving ore formations
    """
    global map_image
    map_image = passed_image
    iterated_image = pygame.Surface((map_image.get_width(), map_image.get_height()))
    iterated_image.fill(c.IMAGES["grass"].color_code)
    for x in range(map_image.get_width()):
        for y in range(map_image.get_height()):
            # Check the surroundings of the tile
            amount = 0
            ores = 0
            for i in range(x - 1, x + 2, 1):
                for j in range(y - 1, y + 2, 1):
                    blocked, ore = _is_blocked(x, y, i, j)[:2]
                    if blocked:
                        amount += 1
                    if ore:
                        ores += 1
            if ores is 1 and random.randint(1, 100) < c.GEN_ORE_CHANCE:
                iterated_image.set_at((x, y), c.IMAGES["ore"].color_code)
            elif amount >= 5:
                if _compare("ore", x, y):
                    iterated_image.set_at((x, y), c.IMAGES["ore"].color_code)
                elif _compare("rock", x, y):
                    iterated_image.set_at((x, y), c.IMAGES["rock"].color_code)
                else:
                    iterated_image.set_at((x, y), c.IMAGES["tree"].color_code)
            else:
                iterated_image.set_at((x, y), c.IMAGES["grass"].color_code)
    return iterated_image


def _iterate_rocks(passed_image):
    """ Evolves rock formations every iteration
    """
    global map_image
    map_image = passed_image
    iterated_image = passed_image
    for x in range(map_image.get_width()):
        for y in range(map_image.get_height()):
            if _compare("rock", x, y):
                rocks = 0
                for i in range(x - 1, x + 2, 1):
                    for j in range(y - 1, y + 2, 1):
                        rock = _is_blocked(x, y, i, j)[2:][0]
                        if rock:
                            rocks += 1
                if rocks <= 2:
                    relative_x = relative_y = 0
                    while relative_x is 0 and relative_y is 0:
                        relative_x = random.randint(-1, 1)
                        relative_y = random.randint(-1, 1)
                    iterated_image.set_at((x + relative_x, y + relative_y), c.IMAGES["rock"].color_code)

    return iterated_image


def _is_blocked(x, y, i, j):
    """ Finds out if the selected coordinate has a collidable tile
    """
    ore = False
    rock = False
    if (i < 0 or i >= map_image.get_width() or
            j < 0 or j >= map_image.get_height()):
        return True, False, False
    else:
        if _compare("ore", i, j) and not (x == i and y == j):
            ore = True
        if _compare("rock", i, j) and not (x == i and y == j):
            rock = True
        if (map_image.get_at((i, j)) == c.IMAGES["tree"].color_code or
                map_image.get_at((i, j)) == c.IMAGES["rock"].color_code):
            return True, ore, rock
        else:
            return False, ore, rock


def _compare(tile_type, x, y):
    """ Compares the color code of the tile at (x, y) with the one provided in by tile_type.
        returns true or false
    """
    return map_image.get_at((x, y))[:3] == (c.IMAGES[tile_type].color_code[:])
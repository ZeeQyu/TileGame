#!/usr/bin/env python
# coding=utf-8
''' Module /src/globals.py
    TileGame by ZeeQyu
    https://github.com/ZeeQyu/TileGame

    Module for initating global variables that should be available in all modules
'''
import pygame
import pygame.locals as pgl

from maps import generate_map
import graphics
import constants

# Define all the concerned variables as global
global map, width, height, player_start_x, player_start_y, images, entity_list, screen

# Load map using functions from maps.py and store into the map variable
# Get the size of the image as well as the player start point from the map.png file.
map, width, height, player_start_x, player_start_y = generate_map("map.png")
# Making some variables that should be available for use in all modules
images = {}

# Initiate an entity list. Order of this list does not matter
entity_list = []
images = graphics.load_graphics()

# Creates a window just the size to fit all the tiles in the map file.
screen = pygame.display.set_mode((width * constants.TILE_SIZE, height * constants.TILE_SIZE))

key_config = {
    "move_up": pgl.K_RIGHT,
    "move_down": pgl.K_LEFT,
    "move_right": pgl.K_DOWN,
    "move_left": pgl.K_UP,

    "look_up": pgl.K_i,
    "look_down": pgl.K_k,
    "look_right": pgl.K_l,
    "look_left": pgl.K_j,
    
    "remove_tile": pgl.K_o,
    "place_tile": pgl.K_u,
    
    "spawn_beetle": pgl.K_SPACE,
    "duplicate_beetles": pgl.K_d
}

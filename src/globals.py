#!/usr/bin/env python
# coding=utf-8
""" Module /src/globals.py
    TileGame for Python 3
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame

    Module for initating global variables that should be available in all modules
"""
import os, sys

import pygame
import pygame.locals as pgl

sys.path.append(os.path.join(os.getcwd(), "sys"))
from maps import generate_map
import graphics
import constants as c

# Making some variables that should be available for use in all modules
map = width = height = player_start_x = player_start_y = screen = None
images = {}

# If the map should be rerendered next time.
force_update = True

# Initiate an entity list. This contains all entites that aren't special.
entity_list = []
# This entity list holds named entities that will be accessed by name.
# The syntax for this list is {"string_key": Entity}
special_entity_list = {}
# A special list for things like menus that aren't entities.
non_entity_list = {}

images = graphics.load_graphics()

# List of tiles that should be ticked (tick function called).
# This is because all tiles shouldn't be ticked, for performance.
# Should follow the format [[x, y], [x, y]]
tick_tiles = []

# map_screen_buffer is a surface to which the map is painted when it is 
# updated so that the screen isn't rerendered every frame 
map_screen_buffer = None
# If the map should be rerendered
update_map = True

# The selection coordinate for the current on-screen menu
selected = [0, 0]


def update_key_dict(key_list):
    """ Copies the key_list list of lists and converts it to a dictionary, key_dict.
        Uses the first index in each index as the key and the other values in a list as the value. 
    """
    for item in key_list:
        key_dict[item[0]] = item[1:]

# Dictionary that is copied from key_config. key_config exists because interface.py key_reconfig 
# should ask for the keys in a proper order.
key_list = c.key_list
key_dict = {}

update_key_dict(key_list)
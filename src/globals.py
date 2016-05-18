#!/usr/bin/env python
# coding=utf-8
""" Module /src/globals.py
    TileGame for Python 3
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame

    Module for initating global variables that should be available in all modules
"""
from src import constants as c, graphics

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
# Has a microtile (tile constructed from several smaller pieces, dependent on surrounding tiles)
# been changed, so the microtiles need to be updated?
update_microtiles = True

# The position of menus. Is carried over between different times that the menu created.
menu_coords = ["Empty", "Empty"]
# The selection coordinate for the current on-screen menu
menu_selection = [0, 0]
# Temporary variable for where the target of the tile should be while selecting it
tile_target_selection = None

# A variable for storing the map generator temporarily while showing off the map generation
map_generator = None

# A queue for classes under tiles that still need to modify the map. Follows the format
# [["tile_type", x, y], ["tile_type", x, y]]
tile_maker_queue = []


def create_key_dict(key_list):
    """ Copies the key_list list of lists and converts it to a dictionary, key_dict.
        Uses the first index in each index as the key and the other values in a list as the value. 
    """
    for item in key_list:
        key_dict[item[0]] = item[1:]

# Dictionary that is copied from key_config. key_config exists because interface.py key_reconfig 
# should ask for the keys in a proper order.
key_dict = {}
create_key_dict(c.key_list)

# This is created because key_reconfig references it.
key_list = c.key_list


def update_key_dict():
    create_key_dict(key_list)


def in_map(x, y):
    return 0 <= x < width and 0 <= y < height


def get_img(x, y):
    """ Gets the Img class from constants.IMAGES of the tile at x, y.
        returns an Img object
    """
    return c.IMAGES[map[x][y].type]

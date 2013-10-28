#!/usr/bin/env python
# coding=utf-8
''' Module /src/constants.py
    TileGame
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Module containing various constants and the important IMAGES dictionary that is used to load maps and images.
    
    To add a new image, add a new line to the IMAGES dictionary containing the image name as the key, the filename of the image in the res folder
    and either a tuple containing a RGB value for loading maps or the number zero if that image shouldn't be used for loading the map.
'''
import pygame.locals as pgl

BACKGROUND_COLOR = (0, 0, 0)

# The speed the player moves at. Any number greater than or equal to 0
PLAYER_MOVEMENT_SPEED = 50

# The frequency of the ticks in seconds (seconds between every tick) A tick is a time unit for
# calculations that should be more periodical than cycles or frames
TICK_FREQ = 0.05

# The amount of seconds the game should sleep each loop to not bog the processor too much
SLEEP_TIME = 0.001

# Dictionary containing image data. Read module docstring above for more details.
IMAGES = {# Format : "image_name_in_code": 
          # ["filename in res", (color code in map.png) or 0,
          # [tile remove time in ticks or -1 for unremovable,
          # "tile_that_should_be_used_if_this_is_removed]],
          
          # tiles
         "grass": ["grassTile1.png", (255, 255, 255)],
         "grass2": ["grassTile2.png", 0],
         "grass3": ["grassTile3.png", 0],
         "grass4": ["grassTile4.png", 0],
         "grass5": ["grassTile5.png", 0],
         "grass6": ["grassTile6.png", 0],
         "grass7": ["grassTile7.png", 0],
         "grass8": ["grassTile8.png", 0],
         "grass9": ["grassTile9.png", 0],
         "grass10": ["grassTile10.png", 0],
         "grass11": ["grassTile11.png", 0],
         "grass12": ["grassTile12.png", 0],
         "grass13": ["grassTile13.png", 0],
         "grass14": ["grassTile14.png", 0],
         "grass15": ["grassTile15.png", 0],
         "grass16": ["grassTile16.png", 0],
         "dirt": ["dirtTile.png", 0],
         "rock": ["rocktile.png", (0, 0, 0)],
         "ore": ["oreTile.png", (255, 216, 0)],
         "tree": ["tree1.png", (124, 124, 124), [10, "stump"]],
         "tree2": ["tree2.png", 0],
         "tree3": ["tree3.png", 0],
         "tree4": ["tree4.png", 0],
         "tree5": ["tree5.png", 0],
         "tree6": ["tree6.png", 0],
         "tree7": ["tree7.png", 0],
         "tree8": ["tree8.png", 0],
         "tree9": ["tree9.png", 0],
         "tree10": ["tree10.png", 0],
         "tree11": ["tree11.png", 0],
         "tree12": ["tree12.png", 0],
         "tree13": ["tree13.png", 0],
         "tree14": ["tree14.png", 0],
         "tree15": ["tree15.png", 0],
         "tree16": ["tree16.png", 0],
         "tree17": ["tree17.png", 0],
         "tree18": ["tree18.png", 0],
         "tree19": ["tree19.png", 0],
         "tree20": ["tree20.png", 0],
         "sapling": ["sapling.png", 0, [0, "grass"]],
         "sapling2": ["sapling2.png", 0],
         "sapling3": ["sapling3.png", 0],
         "sapling4": ["sapling4.png", 0],
         "sapling5": ["sapling5.png", 0],
         "sapling6": ["sapling6.png", 0],
         "sapling7": ["sapling7.png", 0],
         "stump": ["stump.png", 0, [15, "grass"]],
         "stump2": ["stump2.png", 0],
         "stump3": ["stump3.png", 0],
         "hq": ["placeholder.png", (255, 106, 0)],
         "start_tile": ["grassTile1.png", (178, 0, 255)],
         "package": ["package.png", (255, 0, 0)],
         
         # entities
         "player": ["player.png"],
         "beetle": ["beetle.png"],
         
         # other
         "aim": ["aim.png"]
        }

# The identifier of the tile that should be used
# when the map.png decoding fails
DEFAULT_TILE = "grass"
# Tiles that can be overwritten by the players place button
PLACEABLE_TILES = ["grass", "stump"]
# The tile that is placed 
PLACE_TILE = "sapling"

# List of tiles that should be used in collision detection
COLLIDING_TILES = ["rock", "tree", "hq"]

# List of tiles that should have random textures. It will check the IMAGES dict for keys containing this value
# IMAGES should contain a texture with this exact name, with an initialization color code (RGB)
RANDOM_TILES = ["tree", "grass", "stump", "sapling"]
DEACTIVATE_RANDOM_TEXTURES = False

# The size of tiles. Probably will never be anything else than 16.
TILE_SIZE = 16

# Entities
# Movement speed of beetle
BEETLE_MOVEMENT_SPEED = 70
# Max travel length of the beetle (the maximum distance in pixels before the beetle changes direction)
BEETLE_MAX_TRAVEL_PX = 24

# Key for key configuration
CONFIG_KEYS_KEY = pgl.K_INSERT
# Messages for when you configure keys.
CONFIG_KEYS_MESSAGE = "Reconfigure keys: Press insert to cancel."
CONFIG_KEYS_TEXT_PREFIX = "Please press the key for "
CONFIG_KEYS_ERROR_MESSAGE = "Sorry, you already used that key."
CONFIG_KEYS_FONT_COLOR = (255, 255, 255)
# Time in (~)ticks for the "invalid key" text to be displayed each time
CONFIG_KEYS_INVALID_TIMER = 15

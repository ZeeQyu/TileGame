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

# The frequency of the ticks in seconds (seconds between every tick) A tick is a time unit for
# calculations that should be more periodical than cycles or frames
TICK_FREQ = 0.05

# The amount of seconds the game should sleep each loop to not bog the processor too much
SLEEP_TIME = 0.001

class Img(object):
    ''' Small class for keeping track of data related to different images.
        Uses a short name because it shouldn't ever be used outside of this file and saves screen space.
    '''
    def __init__(self, png, color_code=None, random=False, placeable=False, destroy=None, evolve=None):
        ''' Initializes a tile image or other image. Should be stored in a dictionary where the
                key is the string identifier for the image (example: "sapling")
            "png" should be the filename in the res folder (example: "sapling.png", "sapling4.png")
                Leave everything else blank if this isn't a tile.
            "color_code" should be the color code of the pixels in map.png that should be this tile.
                (example: (0, 255, 0)) Leave empty for no loading from map.png
            "random" should be True if the tile should be randomized. If it is, only the first
                image should have random=True. All other textures that should be used should
                be simple(nothing other than png) and have the base identifier in the identifier
                (example: if base is "grass", the others might be "grass5" and "other_grass")
                Leave empty for false, (single texture tile)
            "placeable" should be True if this tile can be overwritten when something is placed,
                for example, a tree. Leave blank if it shouldn't be removable.
            "destroy" should be a list containing the time in ticks for a tile to be destroyed
                and which tile it should turn into. (example: [15, "grass"]) Leave blank for 
            "evolve" should be a list containing the minimum time it takes for the tile
                to evolve (change into another tile) and which tile it should evolve to
                (example: [30, 60, "tree"]) Leave blank if it doesn't evolve. 
        '''
        self.type = type
        self.png = png
        self.color_code = color_code
        self.random = random
        self.placeable = placeable
        self.destroy = destroy
        self.evolve = evolve
        

# Dictionary containing image data. Read module docstring above for more details.
IMAGES = {
          # tiles
<<<<<<< HEAD
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
         "stump": ["stump.png", 0, [15, "grass"]],
         "stump2": ["stump2.png", 0],
         "stump3": ["stump3.png", 0],
         "hq": ["placeholder.png", (255, 106, 0)],
         "start_tile": ["grassTile1.png", (178, 0, 255)],
         "package": ["package.png", (255, 0, 0)],
=======
         "grass": Img("grassTile1.png", color_code=(255, 255, 255), random=True, placeable=True),
         "grass2": Img("grassTile2.png"),
         "grass3": Img("grassTile3.png"),
         "grass4": Img("grassTile4.png"),
         "grass5": Img("grassTile5.png"),
         "grass6": Img("grassTile6.png"),
         "grass7": Img("grassTile7.png"),
         "grass8": Img("grassTile8.png"),
         "grass9": Img("grassTile9.png"),
         "grass10": Img("grassTile10.png"),
         "grass11": Img("grassTile11.png"),
         "grass12": Img("grassTile12.png"),
         "grass13": Img("grassTile13.png"),
         "grass14": Img("grassTile14.png"),
         "grass15": Img("grassTile15.png"),
         "grass16": Img("grassTile16.png"),
         "dirt": Img("dirtTile.png"),
         "rock": Img("rocktile.png", color_code=(0, 0, 0)),
         "ore": Img("oreTile.png", color_code=(255, 216, 0)),
         "tree": Img("tree1.png", color_code=(124, 124, 124), random=True, destroy=[10, "stump"]),
         "tree2": Img("tree2.png"),
         "tree3": Img("tree3.png"),
         "tree4": Img("tree4.png"),
         "tree5": Img("tree5.png"),
         "tree6": Img("tree6.png"),
         "tree7": Img("tree7.png"),
         "tree8": Img("tree8.png"),
         "tree9": Img("tree9.png"),
         "tree10": Img("tree10.png"),
         "tree11": Img("tree11.png"),
         "tree12": Img("tree12.png"),
         "tree13": Img("tree13.png"),
         "tree14": Img("tree14.png"),
         "tree15": Img("tree15.png"),
         "tree16": Img("tree16.png"),
         "tree17": Img("tree17.png"),
         "tree18": Img("tree18.png"),
         "tree19": Img("tree19.png"),
         "tree20": Img("tree20.png"),
         "sapling": Img("sapling.png", random=True, destroy=[0, "grass"], evolve=[30, 60, "tree"]),
         "sapling2": Img("sapling2.png"),
         "sapling3": Img("sapling3.png"),
         "sapling4": Img("sapling4.png"),
         "sapling5": Img("sapling5.png"),
         "stump": Img("stump.png", random=True, placeable=True, destroy=[15, "grass"]),
         "stump2": Img("stump2.png"),
         "stump3": Img("stump3.png"),
         "hq": Img("placeholder.png", color_code=(255, 106, 0)),
         "start_tile": Img("grassTile1.png", color_code=(178, 0, 255)),
         "package": Img("package.png", color_code=(255, 0, 0)),
>>>>>>> origin/developing
         
         # entities
         "player": Img("player.png"),
         "beetle": Img("beetle.png"),
         
         # other
         "aim": Img("aim.png")
        }

# The identifier of the tile that should be used
# when the map.png decoding fails
<<<<<<< HEAD
DEFAULT__TILE = "grass"
=======
DEFAULT_TILE = "grass"
# The tile that is placed 
PLACE_TILE = "sapling"
>>>>>>> origin/developing

# List of tiles that should be used in collision detection
COLLIDING_TILES = ["rock", "tree", "hq"]

<<<<<<< HEAD
# List of tiles that should have random textures. It will check the IMAGES dict for keys containing this value
# IMAGES should contain a texture with this exact name, with an initialization color code (RGB)
RANDOM_TILES = ["tree", "grass", "stump"]
=======
# Set to true if all textures should be non-random
>>>>>>> origin/developing
DEACTIVATE_RANDOM_TEXTURES = False

# The size of tiles. Probably will never be anything else than 16.
TILE_SIZE = 16

# Entities
# The speed the player moves at. Any number greater than or equal to 0
PLAYER_MOVEMENT_SPEED = 50
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

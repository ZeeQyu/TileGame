#!/usr/bin/env python
# coding=utf-8
''' Module /src/constants.py
    TileGame
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Module containing various constants and the important IMAGES dictionary that is used to load maps and images.
'''
import pygame.locals as pgl

# Change this to True if you want the screen to update every cycle (all the time) and get max FPS (change sleep time)
FORCE_UPDATE = False

class Img(object):
    ''' Small class for keeping track of data related to different images.
        Uses a short name because it shouldn't ever be used outside of this file and saves screen space.
    '''
    def __init__(self, png, color_code=None, random=False, collides=False,
                 placeable=False, destroy=None, evolve=None, grabbable=None,
                 multi_tile=None):
        ''' Initializes a tile image or other image. Should be stored in a dictionary where the
                key is the string identifier for the image (example: "sapling")
            "png" should be the filename in the res folder (example: "sapling.png", "sapling4.png")
                Leave everything else blank if this isn't a tile.
            "color_code" should be the color code of the pixels in map.png that should be this tile.
                (example: (0, 255, 0)) Leave empty for no loading from map.png
            "random" should be True if the tile should be randomized. If it is, only the first
                image should have random=True. All other textures that should be used should
                be simple(nothing other than png) and have the base identifier in the identifier,
                followed by a number (example: if base is "grass", the others might be
                "grass5" and "grass7") Leave empty for false, (single texture tile).
            "collides" should be True if this tile should collide with Entities.
            "placeable" should be True if this tile can be overwritten when something is placed,
                for example, a tree. Leave blank if it shouldn't be removable.
            "destroy" should be a list containing the time in ticks for a tile to be destroyed
                and which tile it should turn into. (example: [15, "grass"]) Leave blank for 
                indestructible. Multi-tiles should have a third value denoting which tile the
                other tiles in that multitile turns into. (example: [50, "dirt", "tree"]
            "evolve" should be a list containing the minimum time it takes for the tile
                to evolve (change into another tile) and which tile it should evolve to
                (example: [30, 60, "tree"]) Leave blank if it doesn't evolve.
            "grabbable" should be a string with the class name of the entity it should become
                if the grab key is used on that Tile. (example: Package) Leave as None if
                it shouldn't be grabbable.
            "multi_tile" should be a tuple of the width and height in tiles of the tile if
                it is a multi-tile. (example: (3, 3))
        '''
        self.type = type
        self.png = png
        self.color_code = color_code
        self.random = random
        self.collides = collides
        self.placeable = placeable
        self.destroy = destroy
        self.evolve = evolve
        self.grabbable = grabbable
        self.multi_tile = multi_tile

# Dictionary containing image data. Read class Img docstring above for more details.
IMAGES = {
          # tiles
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
         "dirt": Img("dirt.png", random=True, placeable=True, evolve=[75, 100, "grass"]),
         "dirt2": Img("dirt2.png"),
         "dirt3": Img("dirt3.png"),
         "dirt4": Img("dirt4.png"),
         "dirt5": Img("dirt5.png"),
         "tree": Img("tree1.png", color_code=(124, 124, 124), random=True, collides=True, destroy=[10, "stump"]),
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
         "megatree": Img("multiTree.png", collides=True, destroy=[15, "stump", "tree"], multi_tile=(3, 2)),
         "stump": Img("stump.png", random=True, destroy=[15, "dirt"]),
         "stump2": Img("stump2.png"),
         "stump3": Img("stump3.png"),
         "sapling": Img("sapling.png", random=True, destroy=[0, "grass"], evolve=[100, 200, "tree"]),
         "sapling2": Img("sapling2.png"),
         "sapling3": Img("sapling3.png"),
         "sapling4": Img("sapling4.png"),
         "sapling5": Img("sapling5.png"),
         "dirt-sapling": Img("dirtSapling.png", random=True, destroy=[0, "dirt"], evolve=[100, 200, "tree"]),
         "dirt-sapling2": Img("dirtSapling2.png"),
         "dirt-sapling3": Img("dirtSapling3.png"),
         "dirt-sapling4": Img("dirtSapling4.png"),
         "dirt-sapling5": Img("dirtSapling5.png"),
         "rock": Img("rockTile.png", color_code=(0, 0, 0), random=True, collides=True),
         "rock2": Img("rockTile2.png"),
         "rock3": Img("rockTile3.png"),
         "ore": Img("ore.png", color_code=(255, 216, 0), random=True),
         "ore2": Img("ore2.png"),
         "ore3": Img("ore3.png"),
         "ore4": Img("ore4.png"),
         "ore5": Img("ore5.png"),
         "large_ore": Img("large_ore1.png", color_code=(255, 255, 0), random=True, multi_tile=(2, 2)),
         "large_ore2": Img("large_ore2.png"),
         "large_ore3": Img("large_ore3.png"),
         "hq": Img("hq.png", color_code=(255, 106, 0), collides=True, destroy=[40, "package_tile"], multi_tile=(2, 2)),
         "start_tile": Img("emptyPixel.png", color_code=(178, 0, 255)),
         "package_tile": Img("package.png", color_code=(255, 0, 0)),
         
         "pointer": Img("emptyPixel.png"),
         "collide_pointer": Img("emptyPixel.png", collides=True),
         
         # entities
         "player": Img("player.png"),
         "beetle": Img("beetle.png"),
         "moving_package": Img("packageNograss.png"),
         "ufo": Img("enemyUfo.png"),
         
         # other
         "map": Img("map.png"),
         "aim": Img("aim.png"),
         "remove_aim": Img("removeAim.png"),
         "icon": Img("logo.png"),
         "menu_background": Img("menuBackground.png")
        }

BACKGROUND_COLOR = (0, 0, 0)
# The frequency of the ticks in seconds (seconds between every tick) A tick is a time unit for
# calculations that should be more periodical than cycles or frames
TICK_FREQ = 0.05
# The amount of seconds the game should sleep each loop to not bog the processor too much
if FORCE_UPDATE:
    SLEEP_TIME = 0.00001
else:
    SLEEP_TIME = 0.001

# The identifier of the tile that should be used
# when the map.png decoding fails. This tile should always have placeable=True.
DEFAULT_TILE = "grass"
# The tile that is placed with the players place key
SPECIAL_PLACE_TILES = {"dirt": "dirt-sapling"} 
DEFAULT_PLACE_TILE = "sapling"

# Set to true if all textures should be non-random.
DEACTIVATE_RANDOM_TEXTURES = False
# The size of tiles. Probably will never be anything else than 16.
TILE_SIZE = 16

# Entities
# Names of special entities
PLAYER_NAME = "player"
PACKAGE_TILE_NAME = "package_tile"
# The speed various entities moves at. Any number greater than or equal to 0
PLAYER_MOVEMENT_SPEED = 50
BEETLE_MOVEMENT_SPEED = 70
PACKAGE_MOVEMENT_SPEED = 50
# Max travel length of the beetle (the maximum distance in pixels before the beetle changes direction)
BEETLE_MAX_TRAVEL_PX = 24
# The range of distance the package can be from the player while still being pulled in pixels
PACKAGE_PULL_MIN = 9
PACKAGE_PULL_MAX = 20

# Key for key configurIation
CONFIG_KEYS_KEY = pgl.K_INSERT
# Messages for when you configure keys.
CONFIG_KEYS_MESSAGE = "Reconfigure keys: Press insert to cancel."
CONFIG_KEYS_TEXT_PREFIX = "Please press the key you want to use for "
CONFIG_KEYS_ERROR_MESSAGE = "Sorry, you already used that key."
CONFIG_KEYS_FONT_COLOR = (255, 255, 255)
# Time in (~)ticks for the "invalid key" text to be displayed each time
CONFIG_KEYS_INVALID_TIMER = 15

# Menu contants
BORDER_MARGIN = 10

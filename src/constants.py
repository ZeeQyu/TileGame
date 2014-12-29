#!/usr/bin/env python
# coding=utf-8
""" Module /src/constants.py
    TileGame for Python 3
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame

    Module containing various constants and the important IMAGES dictionary that is used to load maps and images.
"""
import pygame.locals as pgl


# Activates various debug callouts that normally should be on, like fps meter.
NORMAL_DEBUG = False
SPECIAL_DEBUG = True

if NORMAL_DEBUG:
    # Change this to True if you want the screen to update every cycle (all the time) and get max FPS (change sleep time)
    FORCE_UPDATE = True
else:
    FORCE_UPDATE = False


class Img(object):
    """ Small class for keeping track of data related to different images.
        Uses a short name because it shouldn't ever be used outside of this file and saves screen space.
    """
    def __init__(self, png, color_code=None, random=False, collides=False,
                 placeable=False, destroy=None, evolve=None, grabbable=None,
                 multi_tile=None):
        """ Initializes a tile image or other image. Should be stored in a dictionary where the
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
                to evolve (change into another tile), makimum time in ticks and which tile
                it should evolve to (example: [30, 60, "tree"]) Leave blank if it doesn't evolve.
            "grabbable" should be a string with the class name of the entity it should become
                if the grab key is used on that Tile. (example: Package) Leave as None if
                it shouldn't be grabbable.
            "multi_tile" should be a tuple of the width and height in tiles of the tile if
                it is a multi-tile. (example: (3, 3))
        """
        self.type = type
        if "." in png:
            self.png = png
        else:
            self.png = png + ".png"
        self.color_code = color_code
        self.random = random
        self.collides = collides
        self.placeable = placeable
        self.destroy = destroy
        self.evolve = evolve
        self.grabbable = grabbable
        self.multi_tile = multi_tile

# This is the folder for the resources (pictures) of the project
RES_FOLDER = "res"

# Dictionary containing image data. Read class Img docstring above for more details.
IMAGES = {
    # tiles
    # "grass": Img("grassTile1.png", color_code=(255, 255, 255), random=True, placeable=True),
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
    "tree": Img("tree1.png", color_code=(124, 124, 124), random=True, collides=True, destroy=[7, "stump"]),
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
    "stump": Img("stump.png", random=True, destroy=[5, "dirt"]),
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
    "ore": Img("ore.png", color_code=(255, 216, 0), random=True, placeable=True),
    "ore2": Img("ore2.png"),
    "ore3": Img("ore3.png"),
    "ore4": Img("ore4.png"),
    "ore5": Img("ore5.png"),
    "ore_mine": Img("oreMine.png", destroy=[10, "ore-package"], random=True),
    "ore_mine2": Img("oreMine2.png"),
    "ore_mine3": Img("oreMine3.png"),
    "ore_mine4": Img("oreMine4.png"),
    "ore_mine5": Img("oreMine5.png"),
    "ore-sapling": Img("oreSapling.png", destroy=[0, "ore"], evolve=[100, 200, "ore-tree"]),
    "ore-tree": Img("oreTree.png", collides=True, destroy=[10, "ore-stump"]),
    "ore-stump": Img("oreStump.png", destroy=[15, "ore"]),
    "large_ore": Img("large_ore1.png", color_code=(255, 255, 0), random=True, multi_tile=(2, 2)),
    "large_ore2": Img("large_ore2.png"),
    "large_ore3": Img("large_ore3.png"),
    "hq": Img("hq.png", color_code=(255, 106, 0), collides=True, destroy=[40, "package_tile"], multi_tile=(2, 2)),
    "start_tile": Img("emptyPixel.png", color_code=(178, 0, 255)),
    "launcher": Img("launcher.png", collides=True, destroy=[15, "package_tile"]),

    "package_tile": Img("package.png", color_code=(255, 0, 0), destroy=[20, "wreckage"]),
    "wreckage": Img("wreckage.png", destroy=[10, "grass"]),
    "ore-package": Img("orePackage.png", destroy=[20, "ore-wreckage"]),
    "ore-wreckage": Img("oreWreckage.png", destroy=[10, "ore"]),
    "dirt-package": Img("dirtPackage.png", evolve=[75, 100, "package_tile"], destroy=[20, "dirt-wreckage"]),
    "dirt-wreckage": Img("dirtWreckage.png", destroy=[10, "dirt"]),
    "endless_package": Img("endless_package_tile.png", color_code=(0, 255, 0), placeable=True),

    "pointer": Img("emptyPixel.png"),
    "collide_pointer": Img("emptyPixel.png", collides=True),

    # entities
    "player": Img("player.png"),
    "beetle": Img("beetle.png"),
    "moving_package": Img("packageNograss.png"),
    "ufo": Img("enemyUfo.png"),
    "robot_empty": Img("robotEmpty.png"),
    "robot_ore": Img("robotOre.png"),

    # other
    "empty": Img("emptyPixel.png"),
    "map": Img("map.png"),
    "aim": Img("aim.png"),
    "remove_aim": Img("removeAim.png"),
    "remove_aim_fail": Img("removeAimFail.png"),
    "icon": Img("logo.png"),
    "menu_background": Img("menuBackground.png"),
    "button": Img("placeholder_button.png"),
    "button1": Img("button1.png"),
    "button2": Img("button2.png"),
    "button3": Img("button3.png"),
    "launcher_button": Img("launcher_button.png"),
    "ore_mine_button": Img("oreMineButton.png"),
    "button_border": Img("button_border.png"),
    "button_close": Img("close_button.png")
}

key_list = [  # Custom keys. Format:
              # "dict_key": [pgl.default_ley, "key config message"],
              # key config message (index 2) is displayed after
              # the constants.CHANGE_KEYS_TEXT_PREFIX when reconfiguring keys
    ["move_up", pgl.K_UP, "moving the player up."],
    ["move_down", pgl.K_DOWN, "moving the player down."],
    ["move_right", pgl.K_RIGHT, "moving the player right."],
    ["move_left", pgl.K_LEFT, "moving the player left."],


    ["remove_tile", pgl.K_f, "removing the tile the player is looking at."],
    ["place_tile", pgl.K_d, "placing a tile on the spot the player is looking at."],
    ["pick_up_tile", pgl.K_e, "picking up or placing down a package."],
    ["build_menu", pgl.K_q, "opening a menu of what can be built."],
    ["select", pgl.K_SPACE, "selecting the current menu item."],
    # ["select", pgl., "selecting the current menu item."],

    ["spawn_beetle", pgl.K_a, "spawning a beetle at the player's feet."],
    ["duplicate_beetles", pgl.K_s, "activating the beetles' self-duplicating process."],
    ["remove_beetles", pgl.K_w, "removing all beetles."]
]

# The identifier of the tile that should be used
# when the map.png decoding fails. This tile should always have placeable=True.
DEFAULT_TILE = "grass"

# Combinations of tiles that, when placed, gives a specific tile
# Syntax is {"tile_to_be_placed+tile_being_placed_on": "resulting tile"}
SPECIAL_PLACE_TILES = {"sapling+dirt": "dirt-sapling",
                       "sapling+ore": "ore-sapling",
                       "package_tile+ore": "ore-package",
                       "package_tile+dirt": "dirt-package",

                       "package_tile+endless_package": "endless_package",
                       "sapling+endless_package": "endless_package"}

# A list of tiles that you can grab a package from.
# Syntax is {"tile_that_become_a_package": "tile_that_is_left_when_you_grab_a_package"}
PACKAGE_TILE_NAMES = {"package_tile": DEFAULT_TILE,
                      "ore-package": "ore",
                      "dirt-package": "dirt",
                      "endless_package": "endless_package"}

BACKGROUND_COLOR = (0, 0, 0)
# The frequency of the ticks in seconds (seconds between every tick) A tick is a time unit for
# calculations that should be more periodical than cycles or frames
TICK_FREQ = 0.05
# The amount of seconds the game should sleep each loop to not bog the processor too much
if FORCE_UPDATE:
    SLEEP_TIME = 0.00001
else:
    SLEEP_TIME = 0.001

# The tile that is placed with the players place key
DEFAULT_PLACE_TILE = "sapling"

# Set to true if all textures should be non-random.
DEACTIVATE_RANDOM_TEXTURES = False
# The size of tiles. Probably will never be anything else than 16.
TILE_SIZE = 16

# Entities
# Names of special entities
PLAYER_NAME = "player"
# The speed various entities moves at. Any number greater than or equal to 0
PLAYER_MOVEMENT_SPEED = 80
BEETLE_MOVEMENT_SPEED = 90
PACKAGE_MOVEMENT_SPEED = 80
PATHER_MOVEMENT_SPEED = 120
# Max travel length of the beetle (the maximum distance in pixels before the beetle changes direction)
BEETLE_MAX_TRAVEL_PX = 24
# The range of distance the package can be from the player while still being pulled in pixels
PACKAGE_PULL_MIN = 10
PACKAGE_PULL_MAX = 24

# Key for key configuration
CONFIG_KEYS_KEY = pgl.K_INSERT
# Messages for when you configure keys.
CONFIG_KEYS_MESSAGE = "Reconfigure keys: Press insert to cancel."
CONFIG_KEYS_TEXT_PREFIX = "Please press the key you want to use for "
CONFIG_KEYS_ERROR_MESSAGE = "Sorry, you already used that key."
CONFIG_KEYS_FONT_COLOR = (255, 255, 255)
# Time in (~)ticks for the "invalid key" text to be displayed each time
CONFIG_KEYS_INVALID_TIMER = 20

# Menu constants in pixels
# Space between screen border and menu border
BORDER_MARGINS = 10
# Space between menu border and buttons
BUTTON_PADDING = 35
# Space between menu border and buttons on the top side
BUTTON_TOP_PADDING = 35
# Space between menu border and buttons on the bottom side
BUTTON_BOTTOM_PADDING = 35
# The size of the button files
BUTTON_SIZE = 56
# The spacing between buttons
BUTTON_SPACING = 6
# The color of the tooltips in the menus
MENU_FONT_COLOR = (255, 255, 255)

# Map generation
# Size of the generated map
GEN_MAP_SIZE = (60, 50)
# Per mille chance of generating that tile at first generation
GEN_TREE_PER_MILLE = 500
GEN_ORE_PER_MILLE = 5
GEN_ROCK_PER_MILLE = 5
# Number of times the terrain should be smoothed (3)
GEN_ITERATIONS = 3
# The chance of ore clusters evolving from ores every iteration
GEN_ORE_CHANCE = 20
# The number of times the rock formations should be evolved (16)
GEN_ROCK_ITERATIONS = 16

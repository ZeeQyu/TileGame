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
NORMAL_DEBUG = True
SPECIAL_DEBUG = False

# Times speed the game should run in. Raise up from 1 if the game is running too slow f.ex. on linux.
GAME_SPEED = 1

if NORMAL_DEBUG:
    # Change this to True if you want the screen to
    # update every cycle (all the time) and get max FPS (change sleep time)
    FORCE_UPDATE = False
else:
    FORCE_UPDATE = False


class Img(object):
    """ Small class for keeping track of data related to different images.
        Uses a short name because it shouldn't ever be used outside of this file and saves screen space.
    """
    def __init__(self, png, color_code=None, random=False, collides=False,
                 placeable=False, destroy=None, evolve=None, multi_tile=None,
                 factory_input=[], factory_output=[], factory_timer=0, factory_alt_image=None, microtiles=None):
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
            "multi_tile" should be a tuple of the width and height in tiles of the tile if
                it is a multi-tile. (example: (3, 3))
            "factory_input" should be a list containing lists where each nested list has two values
                where the first is the type of goods that is needed to produce the output goods
                and the second is the amount of goods required of that goods. If the amount is less than zero,
                infinite amounts will be recieved.
                (example: [["banana_seeds", 1], ["fertilizer", 5]] )
            "factory_output" should be a list with lists where every nested list has the output goods that will be
                produced after the timer runs out, following the same syntax as the input goods above.
                (example: [["banana", 3], ["leaves", 15]] )
            "factory_timer" should be the time in ticks the factory needs to produce the output
                goods from when it recieves the input goods. Defaults to 0.
            "factory_alt_img" should be a string with an identifier of an image in the
                IMAGES list that is used when the factory is working.
            "micro_tiles" should be a list of four strings or None. The four strings should be the image names of
                the top left corners used to construct this micro tile, in following order: similar tiles to all sides,
                similar tiles to both sides but not the corner, similar tile on tbe top and similar tile nowhere. For
                more information, please read doc/microtiles.txt

            If factory_input and evolve is present in the same tile,
                said tile will evolve the evolve-time in ticks after the required goods are delivered.


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
        self.multi_tile = multi_tile
        self.factory_timer = factory_timer
        self.factory_alt_image = factory_alt_image
        self.microtiles = microtiles

        # The following code makes sure the factory input and output are lists in lists and not just lists.
        for item in factory_input:
            if type(item) is not list:
                self.factory_input = [factory_input]
                break
        else:
            self.factory_input = factory_input

        for item in factory_output:
            if type(item) is not list:
                self.factory_output = [factory_output]
                break
        else:
            self.factory_output = factory_output


# This is the folder for the resources (pictures) of the project
RES_FOLDER = "res"

# Dictionary containing image data. Read class Img docstring above for more details.
IMAGES = {
    # tiles
    # "grass": Img("grassTile1.png", color_code=(255, 255, 255), random=True, placeable=True),

    # Nature
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
    "stump": Img("stump.png", random=True, destroy=[5, "dirt"]),
    "stump2": Img("stump2.png"),
    "stump3": Img("stump3.png"),
    "sapling": Img("sapling.png", random=True, destroy=[0, "grass"], evolve=[100, 200, "tree"]),
    "sapling2": Img("sapling2.png"),
    "sapling3": Img("sapling3.png"),
    "sapling4": Img("sapling4.png"),
    "sapling5": Img("sapling5.png"),
    "dirt-sapling": Img("saplingDirt.png", random=True, destroy=[0, "dirt"], evolve=[100, 200, "tree"]),
    "dirt-sapling2": Img("saplingDirt2.png"),
    "dirt-sapling3": Img("saplingDirt3.png"),
    "dirt-sapling4": Img("saplingDirt4.png"),
    "dirt-sapling5": Img("saplingDirt5.png"),
    "rock": Img("rockTile.png", color_code=(0, 0, 0), random=True, collides=True),
    "rock2": Img("rockTile2.png"),
    "rock3": Img("rockTile3.png"),
    "ore": Img("ore.png", color_code=(255, 216, 0), random=True, placeable=True),
    "ore2": Img("ore2.png"),
    "ore3": Img("ore3.png"),
    "ore4": Img("ore4.png"),
    "ore5": Img("ore5.png"),
    "ore-sapling": Img("oreSapling.png", destroy=[0, "ore"], evolve=[300, 400, "ore-tree"]),
    "ore-tree": Img("oreTree.png", collides=True, destroy=[10, "ore-stump"]),
    "ore-stump": Img("oreStump.png", destroy=[15, "ore"]),
    "water": Img("waterPlaceholder.png", color_code=(0, 0, 255),
                 microtiles=["full_water_quartet", "small_corner_water_quartet",
                             "side_water_quartet", "full_corner_water_quartet"]),
    "full_water_quartet": Img("water1.png"),
    "small_corner_water_quartet": Img("water2.png"),
    "side_water_quartet": Img("water3.png"),
    "full_corner_water_quartet": Img("water4.png"),

    # Large Nature
    "large_ore": Img("oreLarge.png", color_code=(255, 255, 0), random=True, multi_tile=(2, 2)),
    "large_ore2": Img("oreLarge2.png"),
    "large_ore3": Img("oreLarge3.png"),
    "megatree": Img("multiTree.png", collides=True, destroy=[15, "stump", "tree"], multi_tile=(3, 2)),

    # Structures
    "ore_mine": Img("oreMine.png", destroy=[10, "ore-package"], random=True,
                    factory_output=[["ore", 1]]),
    "ore_mine2": Img("oreMine2.png"),
    "ore_mine3": Img("oreMine3.png"),
    "ore_mine4": Img("oreMine4.png"),
    "ore_mine5": Img("oreMine5.png"),
    "hq": Img("hq.png", color_code=(255, 106, 0), collides=True, destroy=[40, "package"], multi_tile=(2, 2)),
    "start_tile": Img("emptyPixel.png", color_code=(178, 0, 255)),
    "furnace": Img("furnaceOff.png", collides=True, destroy=[15, "package"], factory_input=[["ore", 3]],
                   factory_output=[["iron", 1]], factory_timer = 30, factory_alt_image = "furnace_on"),
    "furnace_on": Img("furnace.png"),

    "launcher": Img("launcher.png", collides=True, destroy=[15, "package"],
                    factory_input=[["iron", 1], ["battery", 1]], factory_output=[["rocket", 1]]),
    "package_gen": Img("packageGen.png", placeable=True, destroy=[15, "blink_package"],
                       evolve=[0, 0, "package_gen_iron"], factory_input=[["iron", 1]]),
    "package_gen_iron": Img("packageGenIron.png", evolve=[20, 20, "package_gen_package"], destroy=[15, "package_gen"]),
    "package_gen_package": Img("packageGenPackage.png", destroy=[15, "package_gen"]),
    "battery_factory": Img("batteryFactoryOff.png", collides=True, destroy=[15, "package"],
                           factory_alt_image="battery_factory_on",
                           factory_input=[["iron", 2]], factory_output=[["battery", 1]], factory_timer=65),
    "battery_factory_on": Img("batteryFactoryOn.png"),

    # Packages
    "endless_package": Img("packageGenPackage.png", color_code=(0, 255, 0), placeable=True),
    "package": Img("package.png", color_code=(255, 0, 0), destroy=[40, "wreckage"]),
    "ore-package": Img("packageOre.png", destroy=[20, "ore-wreckage"]),
    "dirt-package": Img("packageDirt.png", evolve=[75, 100, "package"], destroy=[20, "dirt-wreckage"]),
    "wreckage": Img("packageWreckage.png", destroy=[10, "grass"]),
    "ore-wreckage": Img("packageWreckageOre.png", destroy=[10, "ore"]),
    "dirt-wreckage": Img("packageWreckageDirt.png", destroy=[10, "dirt"]),
    # This is a package that instantly becomes a normal package, becaues the package_gen
    # can't be destroyed into a package otherwise.
    "blink_package": Img("package.png", evolve=[0, 0, "package"], destroy=[500, "package"]),

    "pointer": Img("emptyPixel.png"),
    "collide_pointer": Img("emptyPixel.png", collides=True),

    # entities
    "player": Img("player.png"),
    "beetle": Img("beetle.png"),
    "moving_package": Img("packageNograss.png"),
    "ufo": Img("enemyUfo.png"),
    "robot_empty": Img("robotEmpty.png"),
    "robot_ore": Img("robotOre.png"),
    "robot_iron": Img("robotIron.png"),
    "robot_waste": Img("robotWaste.png"),
    "robot_battery": Img("robotBattery.png"),
    "rocket": Img("rocket.png"),

    # interface
    "empty": Img("emptyPixel.png"),
    "map": Img("map.png"),
    "aim": Img("aim.png"),
    "remove_aim": Img("removeAim.png"),
    "remove_aim_fail": Img("removeAimFail.png"),
    "tile_target_aim": Img("tileTargetAim.png"),
    "icon": Img("logo.png"),
    "menu_background": Img("menuBackground.png"),
    "button_shader": Img("buttonShader"),

    "button": Img("buttonPlaceholder.png"),
    "button1": Img("button1.png"),
    "button2": Img("button2.png"),
    "button3": Img("button3.png"),
    "launcher_button": Img("buttonLauncher.png"),
    "furnace_button": Img("buttonFurnace.png"),
    "ore_mine_button": Img("buttonOreMine.png"),
    "package_gen_button": Img("buttonPackageGen.png"),
    "battery_factory_button": Img("buttonBatteryFactory.png"),
    "button_border": Img("buttonBorder.png"),
    "button_close": Img("buttonClose.png"),
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
    ["select2", 13, "the second key for selecting current menu item."], # Enter Key
    ["change_target", pgl.K_w, "changing the target of a factory tile."],

    ["spawn_beetle", pgl.K_z, "spawning a beetle at the player's feet."],
    ["duplicate_beetles", pgl.K_x, "activating the beetles' self-duplicating process."],
    ["remove_beetles", pgl.K_c, "removing all beetles."]
]

# The identifier of the tile that should be used
# when the map.png decoding fails. This tile should always have placeable=True.
DEFAULT_TILE = "grass"

# Combinations of tiles that, when placed, gives a specific tile
# Syntax is {"tile_to_be_placed+tile_being_placed_on": "resulting tile"}
SPECIAL_PLACE_TILES = {"sapling+dirt": "dirt-sapling",
                       "sapling+ore": "ore-sapling",
                       "package+ore": "ore-package",
                       "package+dirt": "dirt-package",

                       "package+endless_package": "endless_package",
                       "sapling+endless_package": "endless_package",

                       "package+package_gen": "package_gen_package",
                       "sapling+package_gen": "package_gen"}

# A list of tiles that you can grab a package from.
# Syntax is {"tile_that_become_a_package": "tile_that_is_left_when_you_grab_a_package"}
PACKAGE_TILE_NAMES = {"package": DEFAULT_TILE,
                      "ore-package": "ore",
                      "dirt-package": "dirt",
                      "endless_package": "endless_package",
                      "package_gen_package": "package_gen"}

# The list of all the goods there is. The format is {"goods_name": "image_name_of_the_entity_carrying_it"}
GOODS = {
    "empty": ["robot_empty"],
    "ore": ["robot_ore", "ore"],
    "iron": ["robot_iron", "package_gen_iron"],
    "waste": ["robot_waste", "dirt"],
    "battery": ["robot_battery", "battery_factory_button"],
    "rocket": ["robot_iron", "launcher"]
}

BACKGROUND_COLOR = (0, 0, 0)
# The frequency of the ticks in seconds (seconds between every tick) A tick is a time unit for
# calculations that should be more periodical than cycles or frames
TICK_FREQ = 0.05 / GAME_SPEED
# The amount of seconds the game should sleep each loop to not bog the processor too much
if FORCE_UPDATE:
    SLEEP_TIME = 0.00001
else:
    SLEEP_TIME = 0.001

# The tile that is placed with the players place key
DEFAULT_PLACE_TILE = "sapling"

# The size of tiles. Probably will never be anything else than 16.
TILE_SIZE = 16
# Set to true if all textures should be non-random.
DEACTIVATE_RANDOM_TEXTURES = False
# Set to true to disable all microtiles and default to one texture
DEACTIVATE_MICROTILES = False

# This is a lookup-table for constructing microtiles. It specifies how the quartets should be used to be constructed
# See doc/microtiles.txt for more information
# "binary_neighbour_combination": [quartet_index, rotation, if it should be horizontally mirrored]
MICROTILE_LEGEND = {
    "111": (0, 0, 0),
    "101": (1, 0, 0),
    "001": (2, 0, 0),
    "100": (2, 90, 1),
    "000": (3, 0, 0)
}

# A list of relative, orthagonal directions to iterate through instead of rewriting this list every time
RELATIVE_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Entities
# Names of special entities
PLAYER_NAME = "player"
# The speed various entities moves at. Any number greater than or equal to 0
PLAYER_MOVEMENT_SPEED = 80
BEETLE_MOVEMENT_SPEED = 90
PACKAGE_MOVEMENT_SPEED = 80
PATHER_MOVEMENT_SPEED = 120
ROBOT_MOVEMENT_SPEED = 70
ROCKET_MOVEMENT_SPEED = 125
# Max travel length of the beetle (the maximum distance in pixels before the beetle changes direction)
BEETLE_MAX_TRAVEL_PX = 24
# The range of distance the package can be from the player while still being pulled in pixels
PACKAGE_PULL_MIN = 10
PACKAGE_PULL_MAX = 24
# Standard time in ticks for robots to deliver wares to a position
ROBOT_DELIVER_TIME = 25
# The time between tries of the robot pathfinding of the factory tiles
ROBOT_RETRY_TIME = 70
# The time in ticks it takes for a robot that's returned to home to be loaded into the tile
ROBOT_COME_HOME_TIME = 5
# The time in ticks it takes for a robot that's been loaded back into its factory to set out again with new goods.
ROBOT_LOAD_TIME = 10
ROBOT_RECONSTRUCT_TIME = 600

# Launcher variables
# The time in ticks between shots at max speed.
LAUNCHER_SHOOT_SPEED = 20

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
# Per mille chance of generating that tile at the first generation
GEN_TREE_PER_MILLE = 500
GEN_ORE_PER_MILLE = 5
GEN_ROCK_PER_MILLE = 5
GEN_WATER_PER_MILLE = 1
# Number of times water should expand from sources
GEN_WATER_ITERATIONS = 5
# Chance in percent of water expanding in a given direction
GEN_WATER_EXPAND_CHANCE = 80
# Number of times the trees  should be smoothed and ores evolved (3)
GEN_TREE_ITERATIONS = 3
# The chance of ore clusters evolving from ores every iteration
GEN_ORE_CHANCE = 20
# The number of times the rock formations should be evolved (16)
GEN_ROCK_ITERATIONS = 16

# Special mode for showing off the map generation. Makes a difference when using the buildmenu regen map button.
GEN_DEMO_MODE = False

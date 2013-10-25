#!/usr/bin/env python
# coding=utf-8
''' Module /src/constants.py
    TileGame by ZeeQyu
    https://github.com/ZeeQyu/TileGame
    
    Module containing various constants and the very important IMAGES dictionary that is used to load maps and images.
    
    To add a new image, add a new line to the IMAGES dictionary containing the image name as the key, the filename of the image in the res folder
    and either a tuple containing a RGB value for loading maps or the number zero if that image shouldn't be used for loading the map.
'''

BLACK = (0, 0, 0)

# The speed the player moves at. Any number greater than 0
PLAYER_MOVEMENT_SPEED = 50

# The frequency of the ticks in seconds (seconds between every tick) A tick is a time unit for
# calculations that should be more periodical than cycles or frames
TICK_FREQ = 0.05

# The amount of seconds the game should sleep each loop to not bog the processor too much
SLEEP_TIME = 0.003

# Dictionary containing image data. Read module docstring above for more details.
IMAGES = {# Format : "image_name_in_code": 
          # ["filename in res", (color code in map.png) or 0,
          # 1 for collision check 0 for not],
          
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
         "tree": ["treeTile1.png", (124, 124, 124)],
         "tree2": ["treeTile2.png", 0],
         "tree3": ["treeTile3.png", 0],
         "tree4": ["treeTile4.png", 0],
         "tree5": ["treeTile5.png", 0],
         "tree6": ["treeTile6.png", 0],
         "tree7": ["treeTile7.png", 0],
         "tree8": ["treeTile8.png", 0],
         "tree9": ["treeTile9.png", 0],
         "hq": ["placeholder.png", (255, 106, 0)],
         "start_tile": ["grassTile1.png", (178, 0, 255)],
         "package": ["package.png", (255, 0, 0)],
         
         # entities
         "player": ["player.png"],
         "beetle": ["beetle.png"]
                 }

#List of tiles that should be used in collision detection
COLLIDING_TILES = ["rock", "tree", "hq"]

# Entities
# Movement speed of beetle
BEETLE_MOVEMENT_SPEED = 70
# Max travel length of the beetle (the maximum distance in pixels before the beetle changes direction)
BEETLE_MAX_TRAVEL_PX = 24

BEETLE_TICK_MAX = int(float(BEETLE_MAX_TRAVEL_PX) / float(BEETLE_MOVEMENT_SPEED) / float(TICK_FREQ))
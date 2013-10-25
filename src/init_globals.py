#!/usr/bin/env python
# coding=utf-8
''' Module /init_globals.py
    TileGame by ZeeQyu
    https://github.com/ZeeQyu/TileGame

    Module for initating global variables that should be available in all modules
'''
from maps import generate_map
import graphics
import pygame


# Load map using functions from maps.py and store into the map variable
# Get the size of the image as well as the player start point from the map.png file.
map, width, height, player_start_x, player_start_y = generate_map("map.png")
# Making some variables that should be available for use in all modules
images = {}

# Initiate an entity list. Order of this list does not matter
entity_list = []
images = graphics.load_graphics()

# Creates a window just the size to fit all the tiles in the map file.
screen = pygame.display.set_mode((width * 16, height * 16))
    
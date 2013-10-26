#!/usr/bin/env python
# coding=utf-8
''' Module /src/interface.py
    TileGame
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Module handling interfaces, menus and prompts
'''
import sys, time

import pygame
import pygame.locals as pgl

import constants, globals

WHITE = (255, 255, 255)

def key_config():
    set_key = None
    screen_updated = True
    
    transparent_surface = pygame.Surface((globals.width*constants.TILE_SIZE,
                                          globals.height*constants.TILE_SIZE)).convert_alpha()
    transparent_surface.fill((0, 0, 0, 150))
    
    font = pygame.font.Font("freesansbold.ttf", 20)
    text_surface = font.render("Hello World!", True, constants.KEY_CHANGE_FONT_COLOR)
    
    config_list_keys = globals.key_config.keys()
    
    while True:
        # Events
        for event in pygame.event.get():
            # Quit code
            if event.type == pgl.QUIT:
                sys.exit()
            # Cancel
            elif event.type == pgl.KEYDOWN and event.key == constants.CHANGE_KEYS_KEY:
                return
            # Key configuration
            elif event.type == pgl.KEYDOWN:
                set_key = event.key
        # If the user pressed a key
        if set_key != None:
            screen_updated = True
            set_key = None
        
        # Only update screen if something updated
        if screen_updated:
            screen_updates = False
            # Draw the map buffer
            globals.screen.blit(globals.map_screen_buffer, (0, 0))
            # Draw entities
            for entity in globals.entity_list:
                entity.paint()
            globals.player.paint()
            # Darken the screen a bit
            globals.screen.blit(transparent_surface, (0, 0))
            # Draw text
            globals.screen.blit(text_surface, (200, 200))
            pygame.display.flip()
        # Sleep by a fixed amount, because this 
        time.sleep(constants.TICK_FREQ)
        
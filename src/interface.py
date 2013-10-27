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

def key_reconfig():
    ''' Function for reconfiguring key mappings. Freezes the screen and darkens it and displays
        prompts for telling the user which key should be inputted next. Closes when done 
    '''
    set_key = None
    screen_updated = True
    invalid_key_timer = 0
    new_keys = []
    
    transparent_surface = pygame.Surface((globals.width*constants.TILE_SIZE,
                                          globals.height*constants.TILE_SIZE)).convert_alpha()
    transparent_surface.fill((0, 0, 0, 150))
    
    font = pygame.font.Font("freesansbold.ttf", 20)
    welcome_surface = font.render(constants.CONFIG_KEYS_MESSAGE, True, constants.CONFIG_KEYS_FONT_COLOR)
    error_surface = font.render(constants.CONFIG_KEYS_ERROR_MESSAGE, True, constants.CONFIG_KEYS_FONT_COLOR)    
    
    while True:
        # Events
        for event in pygame.event.get():
            # Quit code
            if event.type == pgl.QUIT:
                sys.exit()
            # Cancel
            elif event.type == pgl.KEYDOWN and event.key == constants.CONFIG_KEYS_KEY:
                return
            # Key configuration
            elif event.type == pgl.KEYDOWN:
                set_key = event.key
        # If the user pressed a key
        if set_key != None:
            for key in new_keys:
                if set_key == key:
                    invalid_key_timer = constants.CONFIG_KEYS_INVALID_TIMER
                    set_key = None
                    break
            if set_key == None:
                continue
            new_keys.append(set_key)
            screen_updated = True
            set_key = None
        
        # Only update screen if something updated
        if screen_updated:
            screen_updates = False

            # If it's done
            if len(new_keys) == len(globals.key_list):
                for i in range(len(new_keys)):
                    globals.key_list[i][1] = new_keys[i]
                globals.update_key_dict()
                return
            elif len(new_keys) > len(globals.key_list):
                raise Exception("The new_keys dictionary somhow got larger than the old_keys dictionary")
            
            # The text that tells the user which key should be configured next.
            # Uses the lenght of the new_keys to figure out which message it should use
            text_surface = font.render(constants.CONFIG_KEYS_TEXT_PREFIX + 
                                       globals.key_list[len(new_keys)][2],
                                       True, constants.CONFIG_KEYS_FONT_COLOR)
            # Draw the map buffer
            globals.screen.blit(globals.map_screen_buffer, (0, 0))
            # Draw entities
            for entity in globals.entity_list:
                entity.paint()
            globals.player.paint()
            # Darken the screen a bit
            globals.screen.blit(transparent_surface, (0, 0))
            # Draw text
            globals.screen.blit(welcome_surface, (200, 100))
            globals.screen.blit(text_surface, (200, 200))
            if invalid_key_timer > 0:
                invalid_key_timer -= 1
                globals.screen.blit(error_surface, (200, 300))
            pygame.display.flip()
        # Sleep by a fixed amount, because this loop doesn't need to update very constantly 
        time.sleep(constants.TICK_FREQ)
        
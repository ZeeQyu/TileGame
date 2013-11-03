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

class Menu(object):
    ''' Base class for on-screen menus that won't pause the game.
    '''
    def __init__(self, background, target):
        ''' Creates a general-purpose menu.
        
            "background" should be a string identifier pointing
                towards a Graphics object in the globals.images dictionary
                that should be used as a background.
            "target" should be a tuple with an x and y coordinate in pixels
                for where the menu's top left corner should be painted
        '''
        self.background = background
        self.target = target
        
    def paint(self):
        ''' Paints the menu at self.target.
        '''
        globals.screen.blit(globals.images[self.background].get(), self.target)
        
class BuildMenu(Menu):
    ''' Subclass of Menu, used for choosing which building you want to build at a location.
    '''
    def __init__(self):
        self.update_position()
        super(BuildMenu, self).__init__("menu_background", self.target)
        
    def update_position(self):
        player_x = globals.special_entity_list["player"].x
        player_y = globals.special_entity_list["player"].y
        # Put the target variable in the other end of the screen than the player
        background_width, background_height = globals.images["menu_background"].get_size()
        if player_x > globals.width*constants.TILE_SIZE/2.0:
            if player_y > globals.height*constants.TILE_SIZE/2.0:
                self.target = (constants.BORDER_MARGIN, constants.BORDER_MARGIN)
            else:
                self.target = (constants.BORDER_MARGIN,
                          globals.height * constants.TILE_SIZE - background_height - constants.BORDER_MARGIN)
        else:
            if player_y > globals.height*constants.TILE_SIZE/2.0:
                self.target = (globals.width * constants.TILE_SIZE - background_width - constants.BORDER_MARGIN,
                          constants.BORDER_MARGIN)
            else:
                self.target = (globals.width * constants.TILE_SIZE - background_width - constants.BORDER_MARGIN,
                          globals.height * constants.TILE_SIZE - background_height - constants.BORDER_MARGIN)
                
    def paint(self):
        ''' Updates the position of the menu and paints it.
        '''
        self.update_position()
        super(BuildMenu, self).paint()
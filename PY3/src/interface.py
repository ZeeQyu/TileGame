#!/usr/bin/env python
# coding=utf-8
""" Module /src/interface.py
    TileGame for Python 3
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Module handling interfaces, menus and prompts
"""
import os, sys, time

import pygame
import pygame.locals as pgl

import constants as c
import globals as g

WHITE = (255, 255, 255)

def key_reconfig():
    """ Function for reconfiguring key mappings. Freezes the screen and darkens it and displays
        prompts for telling the user which key should be inputted next. Closes when done 
    """
    set_key = None
    screen_updated = True
    invalid_key_timer = 0
    new_keys = []
    
    transparent_surface = pygame.Surface((g.width*c.TILE_SIZE,
                                          g.height*c.TILE_SIZE)).convert_alpha()
    transparent_surface.fill((0, 0, 0, 150))
    
    font = pygame.font.Font("freesansbold.ttf", 20)
    welcome_surface = font.render(c.CONFIG_KEYS_MESSAGE, True, c.CONFIG_KEYS_FONT_COLOR)
    error_surface = font.render(c.CONFIG_KEYS_ERROR_MESSAGE, True, c.CONFIG_KEYS_FONT_COLOR)    
    
    while True:
        # Events
        for event in pygame.event.get():
            # Quit code
            if event.type == pgl.QUIT:
                sys.exit()
            # Cancel
            elif event.type == pgl.KEYDOWN and event.key == c.CONFIG_KEYS_KEY:
                return
            # Key configuration
            elif event.type == pgl.KEYDOWN:
                set_key = event.key
        # If the user pressed a key
        if set_key != None:
            for key in new_keys:
                if set_key == key:
                    invalid_key_timer = c.CONFIG_KEYS_INVALID_TIMER
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
            if len(new_keys) == len(g.key_list):
                for i in range(len(new_keys)):
                    g.key_list[i][1] = new_keys[i]
                g.update_key_dict()
                return
            elif len(new_keys) > len(g.key_list):
                raise Exception("The new_keys dictionary somhow got larger than the old_keys dictionary")
            
            # The text that tells the user which key should be configured next.
            # Uses the lenght of the new_keys to figure out which message it should use
            text_surface = font.render(c.CONFIG_KEYS_TEXT_PREFIX + 
                                       g.key_list[len(new_keys)][2],
                                       True, c.CONFIG_KEYS_FONT_COLOR)
            # Draw the map buffer
            g.screen.blit(g.map_screen_buffer, (0, 0))
            # Draw entities
            for entity in g.entity_list:
                entity.paint()
            # Darken the screen a bit
            g.screen.blit(transparent_surface, (0, 0))
            # Draw text
            g.screen.blit(welcome_surface, (200, 100))
            g.screen.blit(text_surface, (200, 200))
            if invalid_key_timer > 0:
                invalid_key_timer -= 1
                g.screen.blit(error_surface, (200, 300))
            pygame.display.flip()
        # Sleep by a fixed amount, because this loop doesn't need to update very constantly 
        time.sleep(c.TICK_FREQ)

class Menu(object):
    """ Base class for on-screen menus that won't pause the game.
    """
    def __init__(self, background, target):
        """ Creates a general-purpose menu.
        
            "background" should be a string identifier pointing
                towards a Graphics object in the g.images dictionary
                that should be used as a background.
            "target" should be a tuple with an x and y coordinate in pixels
                for where the menu's top left corner should be painted
        """
        self.background = background
        self.target = target

    def update_position(self):
        """ Updates the position of the Menu based on where the player is.
        """
        player_x = g.special_entity_list["player"].x
        player_y = g.special_entity_list["player"].y
        # Put the target variable in the end of the screen the player isn't in.
        background_width, background_height = g.images["menu_background"].get_size()

        # X Coordinate
        if player_x > g.width * c.TILE_SIZE / 3.0 * 2.0:
            self.target_x = c.BORDER_MARGIN
        elif player_x < g.width * c.TILE_SIZE / 3.0:
            self.target_x = g.width * c.TILE_SIZE - background_width - c.BORDER_MARGIN
        elif self.target_x is "Empty":
            self.target_x = c.BORDER_MARGIN

        # Y Coordinate
        if player_y > g.height * c.TILE_SIZE / 3.0 * 2.0:
            self.target_y = c.BORDER_MARGIN
        elif player_y < g.height * c.TILE_SIZE / 3.0:
            self.target_y = g.height * c.TILE_SIZE - background_height - c.BORDER_MARGIN
        elif self.target_y is "Empty":
            self.target_y = c.BORDER_MARGIN

        # Set the variable the outside refers to.
        self.target = (self.target_x, self.target_y)

    def tick(self):
        """ Dummy methods
        """
        pass
    
    def update(self, time_diff):
        """ Dummy method for
        """
        pass

    def has_moved(self):
        pass
    
    def paint(self):
        """ Updates the position of the menu and paints it at that position
        """
        self.update_position()
        g.screen.blit(g.images[self.background].get(), self.target)


class BuildMenu(Menu):
    """ Subclass of Menu, used for choosing which building you want to build at a location.
    """
    def __init__(self):
        """ Sets the menu up.
        """
        self.target_x = self.target_y = "Empty"
        self.update_position()
        super().__init__("menu_background", self.target)
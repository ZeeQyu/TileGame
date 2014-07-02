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
                raise Exception("The new_keys dictionary somehow got larger than the old_keys dictionary")
            
            # The text that tells the user which key should be configured next.
            # Uses the length of the new_keys to figure out which message it should use
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


class MenuButton(object):
    """ A class for use in menus, representing the various buttons in a menu that can be selected.
    """
    def __init__(self, text, image, function=False, vars=[], recommended=False):
        """ "text" should be a short string showing what the button represents
            "image" should be a string identifier pointing to a Graphics object in the
                g.images dictionary, for the thumbnail
            "function" should be a function that is called when this button is selected.
            "vars" should be a list of parameters that should be passed to the function when it's called.
        """
        self.text = text
        self.image = image
        self.function = function
        self.vars = vars
        # Set recommended to True for it to be displayed at the top of the menu
        self.recommended = recommended

    def __call__(self, *args, **kwargs):
        """ Calls the predetermined function
        """
        if self.function:
            if vars:
                return self.function(*self.vars)
            else:
                return self.function()

    def __str__(self):
        return self.text


class Menu(object):
    """ Base class for on-screen menus that won't pause the game.
    """
    def __init__(self, background, buttons):
        """ Creates a general-purpose menu.
        
            "background" should be a string identifier pointing
                towards a Graphics object in the g.images dictionary
                that should be used as a background.
            "target" should be a tuple with an x and y coordinate in pixels
                for where the menu's top left corner should be painted
        """
        self.background = background
        self.buttons = buttons
        self.buttons.reverse()

        self.button_places = []
        self.background_width, self.background_height = g.images["menu_background"].get_size()
        self.target_x = self.target_y = "Empty"
        self.target = (self.target_x, self.target_y)

        self.update_position()

    def update_position(self):
        """ Updates the position of the Menu based on where the player is.
        """
        player_x = g.special_entity_list["player"].x
        player_y = g.special_entity_list["player"].y

        # Put the target variable in the end of the screen the player isn't in.
        # X Coordinate
        if player_x > g.width * c.TILE_SIZE / 3.0 * 2.0:
            self.target_x = c.BORDER_MARGINS
        elif player_x < g.width * c.TILE_SIZE / 3.0:
            self.target_x = g.width * c.TILE_SIZE - self.background_width - c.BORDER_MARGINS
        elif self.target_x is "Empty":
            self.target_x = c.BORDER_MARGINS

        # Y Coordinate
        if player_y > g.height * c.TILE_SIZE / 3.0 * 2.0:
            self.target_y = c.BORDER_MARGINS
        elif player_y < g.height * c.TILE_SIZE / 3.0:
            self.target_y = g.height * c.TILE_SIZE - self.background_height - c.BORDER_MARGINS
        elif self.target_y is "Empty":
            self.target_y = c.BORDER_MARGINS

        # If the background has moved, move the buttons
        if self.target != (self.target_x, self.target_y):
            # Defining where buttons can be put
            area_width = self.background_width - 2 * c.BUTTON_PADDING
            area_height = self.background_height - c.BUTTON_PADDING - c.BUTTON_TOP_PADDING
            buttons_wide = area_width // (c.BUTTON_SIZE + c.BUTTON_SPACING)
            buttons_high = area_height // (c.BUTTON_SIZE + c.BUTTON_SPACING)

            # Define an amount of top left corners for the buttons
            self.button_places = []
            # A distance from the edges that is balanced to center the buttons in the menu
            margin = (area_width - buttons_wide * (c.BUTTON_SIZE + c.BUTTON_SPACING) + c.BUTTON_SPACING) / 2
            # Add all the buttons in an order from top left to top right
            for j in range(buttons_high):
                for i in range(buttons_wide):
                    self.button_places.append((i * (c.BUTTON_SIZE + c.BUTTON_SPACING) +
                                               self.target_x + margin + c.BUTTON_PADDING,
                                               j * (c.BUTTON_SIZE + c.BUTTON_SPACING) +
                                               self.target_y + c.BUTTON_TOP_PADDING,))

        # Set the variable the outside refers to.
        self.target = (self.target_x, self.target_y)

    def paint(self):
        """ Updates the position of the menu and paints it at that position
        """
        # Update the position and paint the background
        self.update_position()
        g.screen.blit(g.images[self.background].get(), self.target)

        spot_number = 0
        buttons = self.buttons
        # Go through all buttons and paint those who are "recommended" first.
        for i in range(len(buttons)-1, -1, -1):
            button = buttons[i]
            if button.recommended:
                g.screen.blit(g.images[button.image].get(),
                              (self.button_places[spot_number][0], self.button_places[spot_number][1]))
                del buttons[i]
                spot_number += 1

        #  Then leave a spot empty.
        spot_number += 1

        # Then add all the other buttons.
        for i in range(len(buttons)-1, -1, -1):
            button = buttons[i]
            g.screen.blit(g.images[button.image].get(),
                         (self.button_places[spot_number][0], self.button_places[spot_number][1]))
            spot_number += 1


def _hello():
    print("Hi there!")

def _hello2(name):
    print("Hi, {}!".format(name))

class BuildMenu(Menu):
    """ Subclass of Menu, used for choosing which building you want to build at a location.
    """
    def __init__(self):
        """ Sets the menu up.
        """

        super().__init__("menu_background", [
            MenuButton("Hello", "button1", _hello),
            MenuButton("Hello, me", "button2", _hello2, ["You"], recommended=True),
            MenuButton("No Function", "button3")
        ])
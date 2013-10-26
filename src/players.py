#!/usr/bin/env python
# coding=utf-8
''' Module /src/players.py
    TileGame by ZeeQyu
    https://github.com/ZeeQyu/TileGame
    
    Module containing the player class.
    Also handles key press events for movement of the player.
'''

import constants
import pygame.locals as pgl
from entities import Entity
import globals

class Player(Entity):
    ''' Player class. Uses the image from the "player" key from the IMAGES dictionary in constants.py
    '''
    
    def __init__(self, x, y):
        ''' "x" and "y" should be ints.
        '''
        super(Player, self).__init__(x, y, "player", constants.PLAYER_MOVEMENT_SPEED)
        
    def event_check(self, event):
        ''' Event checker. Checks if the event is a key press or release on the arrow keys.
        '''
        if event.type == pgl.KEYDOWN:
            if event.key == globals.key_config["move_up"]:
                self.x_plus = True
            elif event.key == globals.key_config["move_down"]:
                self.x_minus = True
            elif event.key == globals.key_config["move_right"]:
                self.y_plus = True
            elif event.key == globals.key_config["move_left"]:
                self.y_minus = True
                
        if event.type == pgl.KEYUP:
            if event.key == globals.key_config["move_up"]:
                self.x_plus = False
            elif event.key == globals.key_config["move_down"]:
                self.x_minus = False
            elif event.key == globals.key_config["move_right"]:
                self.y_plus = False
            elif event.key == globals.key_config["move_left"]:
                self.y_minus = False

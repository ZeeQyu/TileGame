#!/usr/bin/env python
# coding=utf-8
''' Module /src/players.py
    TileGame
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
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
        self.placing_tile = False
        self.removing_tile = False
        self.aiming_tile = [0, 0]
        
    def tick(self):
        super(Player, self).tick()
        aiming_tile = 0
        if self.removing_tile and not self.placing_tile:
            pass
        
    def event_check(self, event):
        ''' Event checker. Checks if the event is a key press or release on the arrow keys.
        '''
        if event.key == globals.key_dict["move_up"][0]:
            self.y_minus = if_down(event.type)
        elif event.key == globals.key_dict["move_down"][0]:
            self.y_plus = if_down(event.type)
        elif event.key == globals.key_dict["move_left"][0]:
            self.x_minus = if_down(event.type)
        elif event.key == globals.key_dict["move_right"][0]:
            self.x_plus = if_down(event.type)
        
        elif event.key == globals.key_dict["place_tile"][0]:
            self.placing_tile = if_down(event.type)
        elif event.key == globals.key_dict["remove_tile"][0]:
            self.removing_tile = if_down(event.type)

def if_down(down_or_up):
    ''' Checks if down_or_up is equal to pgl.KEYDOWN. Returns true if it is, otherwise it returns false.
    '''
    return down_or_up == pgl.KEYDOWN

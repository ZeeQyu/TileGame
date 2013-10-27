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
        self.relative_aiming_tile = [0, 0]
        
    def tick(self):
        super(Player, self).tick()
        if self.removing_tile and not self.placing_tile:
            pass
        
    def get_relative_aim_tile(self):
        x = 0
        y = 0
        if self.x_plus:
            x += 1
        if self.x_minus:
            x -= 1
        if self.y_plus:
            y += 1
        if self.y_minus:
            y -= 1
        
        return x, y
    
    def get_aim_tile(self):
        x, y = self.get_relative_aim_tile()
        x_add, y_add = self.get_tile()[0]
        x += x_add
        y += y_add
        return x, y
        
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

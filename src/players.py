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
import globals, tiles

class Player(Entity):
    ''' Player class. Uses the image from the "player" key from the IMAGES dictionary in constants.py
    '''
    
    def __init__(self, x=globals.player_start_x, y=globals.player_start_y):
        ''' "x" and "y" should be ints.
        '''
        super(Player, self).__init__(x, y, "player", constants.PLAYER_MOVEMENT_SPEED)
        # If the player is currently placing or removing a tile
        self.placing_tile = False
        self.removing_tile = False
        # The last state self.removing_tile was in
        self.last_removing_tile = False
        # Time until the current tile is removed
        self.remove_timer = 0
        # The last tile the player was aiming at
        self.last_relative_aim_tile = (0, 1)
        self.last_aim_tile = self.get_aim_tile()
        
    def paint(self):
        ''' Paints the player and its aim indicator on the screen.
        '''
        super(Player, self).paint()
        if self.removing_tile:
            globals.screen.blit(globals.images["aim"].get(),
                                (self.last_aim_tile[0]*constants.TILE_SIZE,
                                 self.last_aim_tile[1]*constants.TILE_SIZE))
        
    def tick(self):
        ''' What happens every tick. Counts down the remove block timer. 
        '''
        super(Player, self).tick()
        # If the player is pressing remove
        if self.removing_tile and not self.placing_tile:
            # Get which tile the player is looking at
            aim_tile = self.get_aim_tile()
            x, y = aim_tile
            # If the aim tile has changed
            if aim_tile != self.last_aim_tile:
                # Checks if the aim tile has a remove time (can be destroyed).
                # If so, assign that value to self.remove_timer.
                if len(constants.IMAGES[globals.map[x][y].type]) > 2:
                    self.remove_timer = constants.IMAGES[globals.map[x][y].type][2]
                else:
                    self.remove_timer = -1
            self.last_aim_tile = aim_tile
            # 
            if self.removing_tile != self.last_removing_tile:
                self.should_update = True 
            # If the timer is -1 (not removable), return
            if self.remove_timer == -1:
                return
            # If remove_timer has reached 0 which means the countdown is done
            if self.remove_timer == 0:
                globals.map[x][y] = tiles.makeTile(constants.DEFAULT_TILE, x, y)
                self.remove_timer = -1
                globals.update_map = True
                self.should_update = True
                return
            print self.remove_timer
            self.remove_timer -= 1
        
    def get_relative_aim_tile(self):
        ''' Gets the tile the player is aiming at, relative to the player position.
            returns a tuple ranging from (-1, -1) to (1, 1) with the x and y values
        '''
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
            
        if x == 0 and y == 0:
            return self.last_relative_aim_tile
        else:
            return x, y
    
    def get_aim_tile(self):
        ''' Gets the absolute tile the player is looking at.
            returns a tuple of the x and y coordinate of the tile.
        '''
        x, y = self.get_tile()
        x_add, y_add = self.get_relative_aim_tile()
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
        
#         elif event.key == globals.key_dict["place_tile"][0]:
#             self.placing_tile = if_down(event.type)
        elif event.key == globals.key_dict["remove_tile"][0]:
            self.removing_tile = if_down(event.type)

def if_down(down_or_up):
    ''' Checks if down_or_up is equal to pgl.KEYDOWN. Returns true if it is, otherwise it returns false.
    '''
    return down_or_up == pgl.KEYDOWN

#!/usr/bin/env python
# coding=utf-8
""" Module /src/players.py
    TileGame for Python 3
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Module containing the player class.
    Also handles key press events for movement of the player.
"""
import os, sys

sys.path.append(os.path.join(os.getcwd(), "sys"))
import units, tiles
import pygame.locals as pgl
from entities import Entity
import globals as g
import constants as c
import interface


class Player(Entity):
    """ Player class. Uses the image from the "player" key from the IMAGES dictionary in c.py
    """
    
    def __init__(self, x=g.player_start_x, y=g.player_start_y):
        """ "x" and "y" should be ints.
        """
        super(Player, self).__init__(x, y, "player", c.PLAYER_MOVEMENT_SPEED)
        # If the player is currently placing or removing a tile
        self.placing_tile = False
        self.removing_tile = False
        self.toggle_grab = False
        # The last state self.removing_tile was in
        self.last_removing_tile = False
        # Time until the current tile is removed
        self.remove_timer = None
        # The last tile the player was aiming at
        self.last_relative_aim_tile = (0, 1)
        self.last_aim_tile = self.get_aim_tile()
        # Refreshes the tile the player is aiming at if True, for rechecking after removing a tile
        self.update_aim_tile = False
        # If the player has opened a menu. If so, arrow keys should navigate the menu.
        self.browsing_menu = False
        
    def paint(self):
        """ Paints the player and its aim indicator on the screen.
        """
        super(Player, self).paint()

        if self.removing_tile:
            if g.get_img(*self.get_aim_tile()).destroy is not None:
                aim = "remove_aim"
            else:
                aim = "remove_aim_fail"
        else:
            aim = "aim"
        x = ((self.last_aim_tile[0]*c.TILE_SIZE) +
             (c.TILE_SIZE - g.images[aim].get_size()[0]) / 2)
        y = ((self.last_aim_tile[1]*c.TILE_SIZE) +
             (c.TILE_SIZE - g.images[aim].get_size()[1]) / 2)
        g.screen.blit(g.images[aim].get(), (x, y))

    def update(self, time_diff):
        """ Calls the superclass update and updates the state of the aim marker.
            Manages if the player is placing or destroying a block.
        """
        super(Player, self).update(time_diff)
        # Update screen whenever aim marker changes states
        if self.removing_tile != self.last_removing_tile:
            self.last_removing_tile = self.removing_tile
            g.force_update = True
        
        # Get which tile the player is looking at
        aim_tile = self.get_aim_tile()
        x, y = aim_tile
        # If the aim tile has changed
        if aim_tile != self.last_aim_tile or self.update_aim_tile:
            self.update_aim_tile = False
            # Checks if the aim tile has a remove time (can be destroyed).
            # If so, assign that value to self.remove_timer.
            try:
                if c.IMAGES[g.map[x][y].type].destroy is not None:
                    self.remove_timer = c.IMAGES[g.map[x][y].type].destroy[0]
                elif type(g.map[x][y]) == tiles.MultiTilePointer:
                    # Finding out which tile the pointer is pointing to, and if that has a destroy value
                    head_x, head_y = g.map[x][y].target
                    multi_tile_head = g.map[head_x][head_y]
                    if c.IMAGES[multi_tile_head.type].destroy is not None:
                        self.remove_timer = c.IMAGES[multi_tile_head.type].destroy[0]
                    else:
                        self.remove_timer = None
                else:
                    self.remove_timer = None
            except IndexError:
                self.remove_timer = None
            except:
                raise
        self.last_aim_tile = aim_tile
        
        # Placing tile
        if self.placing_tile and not self.removing_tile:
            try:
                if c.IMAGES[g.map[x][y].type].placeable:
                    # If there is a special case for placing tiles, use that. Otherwise, use the default
                    tiles.make_tile(c.DEFAULT_PLACE_TILE, x, y)
            # Ignore IndexErrors because the indices might be outside of the map
            except IndexError:
                pass
            except:
                raise
            
        # Removing tile
        if self.removing_tile and not self.placing_tile:
            # If the timer isn't None (is removable)
            if self.remove_timer is not None:
                # If remove_timer has reached 0 which means the countdown is done
                if self.remove_timer < 1:
                    tiles.destroy_tile(x, y)
                    self.update_aim_tile = True
                    self.remove_timer = None
                    return
                
        # Grabbing tile
        if self.toggle_grab:
            # If the grab button is pressed
            self.toggle_grab = False
            if self.following_entity is not None:
                x, y = self.get_aim_tile()
                if c.IMAGES[g.map[x][y].type].placeable:
                    g.special_entity_list[self.following_entity].target_coords = [x*c.TILE_SIZE,
                                                                                  y*c.TILE_SIZE]
            else:
                if g.map[x][y].type in c.PACKAGE_TILE_NAMES.keys():
                    tiles.make_tile(c.PACKAGE_TILE_NAMES[g.map[x][y].type], x, y)
                    g.update_map = True
                    units.Package(x*c.TILE_SIZE, y*c.TILE_SIZE, "player")

    def tick(self):
        """ What happens every tick. Counts down the remove block timer. 
        """
        super(Player, self).tick()
        if self.removing_tile and not self.placing_tile and self.remove_timer is not None:
            self.remove_timer -= 1
        
    def get_relative_aim_tile(self):
        """ Gets the tile the player is aiming at, relative to the player position.
            returns a tuple ranging from (-1, -1) to (1, 1) with the x and y values
        """
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
            self.last_relative_aim_tile = x, y
            return x, y
    
    def get_aim_tile(self):
        """ Gets the absolute tile the player is looking at.
            returns a tuple of the x and y coordinate of the tile.
        """
        x, y = self.get_tile()
        x_add, y_add = self.get_relative_aim_tile()
        x += x_add
        y += y_add
        return x, y

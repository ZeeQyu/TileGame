#!/usr/bin/env python
# coding=utf-8
""" Module /src/units.py
    TileGame for Python 3
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Units module, containing classes for all friendly and passive units.
"""
import math, os, sys
from random import randint

sys.path.append(os.path.join(os.getcwd(), "sys"))
import entities
import tiles
import globals as g
import constants as c

class Animal(entities.Entity):
    """ Base class for harmless entites that randomly roam about
    """
    def __init__(self, x, y, image, movement_speed, max_travel, collides = True,
                 rotates = True, wall_collides = True):
        """ Calls the entity init and creates another variable
        """
        super(Animal, self).__init__(x, y, image, movement_speed, collides=collides,
                                     rotates=rotates, wall_collides=wall_collides)
        self.movement_timer = 0
        self.max_travel = max_travel
        
    def update(self, delta_remainder):
        """ Updates the animal position and moves it randomly in a direction
            for a random amount of time between
            half of the max travel and the max travel
        """

        # If it moves at all
        if self.movement_speed > 0:
            # When the movement timer is done counting down, give the Animal a new
            # random direction and duration to travel
            if self.movement_timer <= 0:
                # Calculate what value the maximum amount of ticks between direction changes
                # should be
                tick_max = int(float(self.max_travel) /
                   float(self.movement_speed) /
                   float(c.TICK_FREQ))
                # The amount of ticks until direction change, which is a random int
                # between half of tick_max and tick_max
                self.movement_timer =  randint(int(tick_max / 2), tick_max)
                # Set a random direction
                self.x_plus = bool(randint(0, 1))
                self.x_minus = bool(randint(0, 1))
                self.y_plus = bool(randint(0, 1))
                self.y_minus = bool(randint(0, 1))
            
        super(Animal, self).update(delta_remainder)
        
    def tick(self):
        """ Method for what should happen every tick
        """
        super(Animal, self).tick()
        self.movement_timer -= 1


class Beetle(Animal):
    """ Harmless roaming little beetle that will be able to be
        infected in the future by enemies to become some kind of zombie beetle
    """ 
    def __init__(self, x, y, collides=True, rotates=True, wall_collides=True):
        """ Calls the entity init function with the proper movement speed and image
        """
        super(Beetle, self).__init__(x, y, "beetle", c.BEETLE_MOVEMENT_SPEED,
                                     c.BEETLE_MAX_TRAVEL_PX, collides=collides,
                                     rotates=rotates, wall_collides=wall_collides) 


class Package(entities.FollowingEntity):
    """ The detached version of the package, used as building parts for buildings.
        Supposed to be placed where you want to build a building and be a package of
        resources to build with.
    """
    def __init__(self, x, y, attached_entity=None, custom_name=None):
        """ Initalizes a FollowingEntity with some package-specific variables.
        """
        super(Package, self).__init__(x, y, "moving_package", c.PACKAGE_MOVEMENT_SPEED,
                                      attached_entity=attached_entity, pull_min=c.PACKAGE_PULL_MIN,
                                      pull_max=c.PACKAGE_PULL_MAX, rotates=False, custom_name=custom_name)
        # Compensate for the package image being smaller than package_tile image
        self.x += (c.TILE_SIZE - self.width) / 2
        self.y += (c.TILE_SIZE - self.height) / 2
        # The kind of tile this package will become if placed
        self.tile = "package_tile"
        # Variable used only for checking if the Package just got target coords
        self.had_target_coords = False
        
    def update(self, time_diff):
        """ Calls the super update function as well as check for if the package should be turned into a tile.
        """
        if self.target_coords and not self.had_target_coords:
            self.had_target_coords = True
            self.target_coords[0] += (c.TILE_SIZE - self.width) / 2
            self.target_coords[1] += (c.TILE_SIZE - self.height) / 2
            
        if self.target_coords == [int(self.x), int(self.y)]:
            x, y = self.get_tile()
            tiles.make_tile(self.tile, x, y)
            if self.attached_entity is not None:
                g.special_entity_list[self.attached_entity].following_entity = None
                del g.special_entity_list[self.attached_entity + "-" + self.image]
            elif self.custom_name:
                del g.special_entity_list[self.custom_name]
            else:
                del self

            return "deleted"
        super(Package, self).update(time_diff)


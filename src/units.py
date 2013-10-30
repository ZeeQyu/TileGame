#!/usr/bin/env python
# coding=utf-8
''' Module /src/units.py
    TileGame
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Units module, containing classes for all friendly and passive units.
'''
import math

from entities import Entity
import constants, globals
from random import randint

class Animal(Entity):
    ''' Base class for harmless entites that randomly roam about
    '''
    def __init__(self, x, y, image, movement_speed, max_travel, collides = True, rotates = True, wall_collides = True):
        ''' Calls the entity init and creates another variable
        '''
        super(Animal, self).__init__(x, y, image, movement_speed,collides=collides,
                                     rotates=rotates, wall_collides=wall_collides)
        self.movement_timer = 0
        self.max_travel = max_travel
        
    def update(self, delta_remainder):
        ''' Updates the animal position and moves it randomly in a direction
            for a random amount of time between
            half of the max travel and the max travel
        '''

        # If it moves at all
        if self.movement_speed > 0:
            # When the movement timer is done counting down, give the Animal a new
            # random direction and duration to travel
            if self.movement_timer <= 0:
                # Calculate what value the maximum amount of ticks between direction changes
                # should be
                tick_max = int(float(self.max_travel) /
                   float(self.movement_speed) /
                   float(constants.TICK_FREQ))
                # The amount of ticks until direction change, which is a random int
                # between half of tick_max and tick_max
                self.movement_timer =  randint(tick_max / 2, tick_max)
                # Set a random direction
                self.x_plus = bool(randint(0, 1))
                self.x_minus = bool(randint(0, 1))
                self.y_plus = bool(randint(0, 1))
                self.y_minus = bool(randint(0, 1))
            
        super(Animal, self).update(delta_remainder)
        
    def tick(self):
        ''' Method for what should happen every tick
        '''
        super(Animal, self).tick()
        self.movement_timer -= 1
        
class Beetle(Animal):
    ''' Harmless roaming little beetle that will be able to be
        infected in the future by enemies to become some kind of zombie beetle
    ''' 
    def __init__(self, x, y, collides=True, rotates=True, wall_collides=True):
        ''' Calls the entity init function with the proper movement speed and image
        '''
        super(Beetle, self).__init__(x, y, "beetle", constants.BEETLE_MOVEMENT_SPEED,
                                     constants.BEETLE_MAX_TRAVEL_PX, collides=collides,
                                     rotates=rotates, wall_collides=wall_collides) 
        
class Package(Entity):
    ''' The detached version of the package, used as building parts for buildings.
        Supposed to be placed where you want to build a building and be a package of
        resources to build with.
    '''
    def __init__(self, x, y):
        super(Package, self).__init__(x, y, "package", constants.PACKAGE_MOVEMENT_SPEED, rotates=False)
        
    def update(self, time_diff):
        super(Package, self).update(time_diff)
        
        x_dist = ((self.x+self.width) / 2) - ((globals.special_entity_list["player"].x +
                                               globals.special_entity_list["player"].width) / 2)
        y_dist = ((self.y+self.height) / 2) - ((globals.special_entity_list["player"].y +
                                                globals.special_entity_list["player"].height) / 2)
        
        print x_dist, y_dist
        dist = math.hypot(self.x - globals.special_entity_list["player"].x,
                          self.y - globals.special_entity_list["player"].y)
        print dist
        if dist < constants.PACKAGE_PULL_MAX * 1.5:
            if (constants.PACKAGE_PULL_MIN < x_dist < constants.PACKAGE_PULL_MAX or
                -constants.PACKAGE_PULL_MIN > x_dist > -constants.PACKAGE_PULL_MAX):
                if x_dist > 0:
                    self.x_minus = True
                    self.x_plus = False
                else:
                    self.x_plus = True
                    self.x_minus = False
            else:
                self.x_plus = self.x_minus = False
                
            if (constants.PACKAGE_PULL_MIN < y_dist < constants.PACKAGE_PULL_MAX or
                -constants.PACKAGE_PULL_MIN > y_dist > -constants.PACKAGE_PULL_MAX):
                if y_dist > 0:
                    self.y_minus = True
                    self.y_plus = False
                else:
                    self.y_plus = True
                    self.y_minus = False
            else:
                self.y_plus = self.y_minus = False
        else:
            self.y_plus = self.y_minus = self.x_plus = self.x_minus = False
        
    
        
        
        
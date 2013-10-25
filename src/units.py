#!/usr/bin/env python
# coding=utf-8
''' Module /src/units.py
    TileGame by ZeeQyu
    https://github.com/ZeeQyu/TileGame
    
    Units module, containing classes for all friendly and passive units.
'''
from entities import Entity
from constants import *
from random import randint

class Animal(Entity):
    ''' Base class for harmless entites that randomly roam about
    '''
    def __init__(self, x, y, image, movement_speed, max_travel):
        ''' Calls the entity init and creates another variable
        '''
        super(Animal, self).__init__(x, y, image, movement_speed)
        self.movement_timer = 0
        self.max_travel = max_travel
        
    def update(self, delta_remainder):
        ''' Updates the animal position and moves it randomly in a direction
            for a random amount of time between
            half of the max travel and the max travel
        '''


        # When the movement timer is done counting down, give the Animal a new
        # random direction and duration to travel
        if self.movement_timer <= 0:
            # Calculate what value the maximum amount of ticks between direction changes
            # should be
            tick_max = int(float(self.max_travel) /
               float(self.movement_speed) /
               float(TICK_FREQ))
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
    def __init__(self, x, y):
        ''' Calls the entity init function with the proper movement speed and image
        '''
        super(Beetle, self).__init__(x, y, "beetle", BEETLE_MOVEMENT_SPEED,
                                     BEETLE_MAX_TRAVEL_PX)
        
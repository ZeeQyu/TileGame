#!/usr/bin/env python
# coding=utf-8
''' Module /src/entities.py
    TileGame
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Module containing the player class.
    Also handles key press events for movement of the player.
'''

import pygame
from pygame import Rect

import globals
import constants
from graphics import Graphics

class InvalidCallParameterException(Exception):
    ''' A fancy class name for if the programmer (me) somehow mistook what variables
        should be passed to the __init__ function in the Entity class in entities.py 
    ''' 
    pass

class Entity(object):
    ''' Entity base class for all the other entities to build upon.
    '''
    
    def __init__(self, x, y, image, movement_speed, rotates = True, collides = True, wall_collides = True):

        ''' "x" and "y" should be ints.
            "image" should be a string with the IMAGES identifier
            "width_or_size" should either be an int denoting the width of the entity
            or a tuple containing both width and height in that order.
            In the latter case, height should be left empty
        '''
        self.x = x
        self.y = y
        # Getting width and height from image file
        self.width, self.height = globals.images[image].get_size()
        # Variables for checking if the entity should move.
        self.x_plus = False
        self.x_minus = False
        self.y_plus = False
        self.y_minus = False
        
        # Variables for checking if the entity has moved.
        self.old_x = x
        self.old_y = y
        # Set picture string
        self.image = image
        # The movement speed of the entity, specified by 1 / movement_speed
        # seconds for each pixel
        self.movement_speed = float(movement_speed)
        # Creates four rectangles for collision checking
        self.update_collision_rects()
        # Whether or not the entity collides with terrain
        self.collides = collides
        self.wall_collides = wall_collides
        # Whether or not the entity rotates when it changes direction
        self.rotates = rotates
        # The amount of degrees from facing down the unit should rotate and the angle of the last time 
        # paint was called
        self.angle = 0
        self.last_angle = 0
        
    def update(self, delta_remainder):
        ''' Updates the entity location if any of the plus and minus variables are set to True
            "delta_remainder" should be the time since the last update in seconds.
            
            moves the enitity one pixel at the time if the delta_remainder is too large
                (Larger than 1 / movement_speed. if so, it subtracts 1 / movement_speed and uses that as the delta, 
                because the entity shouldn't move more than one pixel per update because of collision detection)
        '''
        # If the delta value (the time passed) is too large, make sure the player doesn't move more than one pixel.
        if self.movement_speed > 0:
            delta = 0
            while delta_remainder > 0:
                if delta_remainder > (1 / self.movement_speed):
                    delta = (1 / self.movement_speed)
                    delta_remainder = (delta_remainder - delta)
                else:
                    delta = delta_remainder
                    delta_remainder = 0
                # Variables for checking if the entity changed pixel
                prev_x = self.x
                prev_y = self.y
                # Move the entity in the direction the variables denote it should be.
                if self.x_plus:
                   self.x += self.movement_speed * delta
                if self.x_minus:
                    self.x -= self.movement_speed * delta
                if self.y_plus:
                    self.y += self.movement_speed * delta
                if self.y_minus:
                    self.y -= self.movement_speed * delta
                        
                self.collision_check()
        if self.rotates:
            # Rotation logic, which direction is the entity facing and how many degrees should it rotate
            # Uses last angle if the entity is not moving
            if self.x_plus and not self.x_minus:
                if self.y_plus and not self.y_minus:
                    self.angle = 45
                elif self.y_minus and not self.y_plus:
                    self.angle = 135
                else:
                    self.angle = 90
            elif self.x_minus and not self.x_plus:
                if self.y_plus and not self.y_minus:
                    self.angle = -45
                elif self.y_minus and not self.y_plus:
                    self.angle = -135
                else:
                    self.angle = -90
            else:
                if self.y_plus and not self.y_minus:
                    self.angle = 0
                elif self.y_minus and not self.y_plus:
                    self.angle = 180
                else:
                    self.angle = self.last_angle
            # Update the player if he's aiming in a new direction
            if self.angle != self.last_angle:
                globals.force_update = True
            # Remember the angle until next time
            self.last_angle = self.angle
            
    def tick(self):
        ''' Dummy method for what happens every tick
        '''
        pass
    
            
    def paint(self):
        ''' Paints the player on the screen
        '''
        if self.rotates:
            # Create a key with the current entity string and the angle
            key = self.image
            if self.angle != 0:
                key = key + str(self.angle)
            # Check the images dict for a key with the current entity and rotation 
            if globals.images.has_key(key):
                image = globals.images[key].get()
            else:
                # The images dict doesn't have the current sprite with that rotation, create it
                globals.images[key] = Graphics(pygame.transform.rotate(globals.images[self.image].get(), self.angle))
                image = globals.images[key].get()
        else:
            image = globals.images[self.image].get()
            
        # Actually paint the object
        if float(int(self.angle / 90.0)) != self.angle / 90.0:
            # Compensate for rotated entities
            globals.screen.blit(image, (int(self.x) - int(self.width/5.0),
                                        int(self.y) - int(self.height/5.0)))
        else:
            globals.screen.blit(image, (int(self.x), int(self.y)))
        
    def has_moved(self, update=True):
        ''' Compares an old x and y value with the current one. 
            If the value has changed, the unit has moved to another pixel and should be redrawn.
            update should be 1 if you want to update the checking to a new pixel and 0 if you don't
            
            returns True if the player has changed pixel and False if it hasn't
        '''

        if self.old_x != int(self.x) or self.old_y != int(self.y):
            if update:
                self.old_x = int(self.x)
                self.old_y = int(self.y)
            return True
        else:
            return False
            
    def get_tile(self):
        ''' Returns the coordinates of tile the entity is currently on (x and y) 
        ''' 
        return int((self.x + self.width/2) / float(constants.TILE_SIZE)), int((self.y + self.height/2) / float(constants.TILE_SIZE))
    
    def corner_in_tile(self, tile):
        ''' Checks if any of the entities corners are inside of the specified tile.
            "tile" should be a tiles.Tile object
        '''
        # Get the corners of the entity
        corners = [(self.x, self.y),
                   (self.x+self.width, self.y),
                   (self.x, self.y+self.height),
                   (self.x+self.width, self.y+self.height)]
        # And get rects for those corners
        corner_rects = []
        for corner in corners:
            corner_rects.append(Rect(corner, (1, 1)))
        
        if tile.rect().collidelist(corner_rects) != -1:
            return True
        else:
            return False
        
    def update_collision_rects(self):
        ''' Method for creating four pygame Rect object along the sides of the entity for use in collision detection 
        '''
        self.col_right = Rect(self.x + self.width - 1, 
                              self.y + 1,
                              1,
                              self.height - 2)
        
        self.col_left = Rect(self.x,
                             self.y + 1,
                             1,
                             self.height - 2)
        
        self.col_top = Rect(self.x + 1,
                            self.y,
                            self.width - 2,
                            1)
        
        self.col_bottom = Rect(self.x + 1,
                               self.y + self.height - 1,
                               self.width - 2,
                               1)
        
    def collision_check(self):
        ''' Method for checking if the entity has run into a tree or something
            and move it back a pixel if it has
        '''
        if self.wall_collides:
            # Move the entity inside of the window (border collision)
            entity_rect = Rect(self.x, self.y, self.width,self.height)
            window_rect = Rect(0, 0, globals.width * constants.TILE_SIZE, globals.height * constants.TILE_SIZE)
            if not window_rect.contains(entity_rect):
                entity_rect.clamp_ip(window_rect)
                self.x = entity_rect.left
                self.y = entity_rect.top

        if self.collides:
            # Make sure collision rectangles are up to date
            self.update_collision_rects()
            # Get the tile the entity is standing on
            tile_pos = self.get_tile()
            checked_tiles = []
            # Loop through a 3x3 tile square around the entity, to not check the entire map
            for i in range(tile_pos[0] - 1, tile_pos[0] + 2):
                for j in range(tile_pos[1] - 1, tile_pos[1] + 2):
                    try:
                        if constants.IMAGES[globals.map[i][j].type].collides:
                            checked_tiles.append(globals.map[i][j].rect())
                    except IndexError:
                        # That index was apparently outside of the map
                        pass
                    except:
                        raise
                    
            # Check if each of the zones collides with any of the tiles
            if self.col_left.collidelist(checked_tiles) != -1:
                self.x += 1
            if self.col_right.collidelist(checked_tiles) != -1:
                self.x -= 1
            if self.col_bottom.collidelist(checked_tiles) != -1:
                self.y -= 1
            if self.col_top.collidelist(checked_tiles) != -1:
                self.y += 1

def free_of_entities(tile):
    ''' A function to check if any of the entities has any of its corners inside the specified tile.
    '''
    free_of_entities = True
    for entity in globals.entity_list:
        if entity.corner_in_tile(tile):
            free_of_entities = False
    for entity in globals.special_entity_list.values():
        if entity.corner_in_tile(tile):
            free_of_entities = False
    return free_of_entities
                    
#!/usr/bin/env python
# coding=utf-8
""" Module /src/entities.py
    TileGame for Python 3
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Module containing the player class.
    Also handles key press events for movement of the player.
"""

import sys
import os
import math

import pygame
from pygame import Rect


sys.path.append(os.path.join(os.getcwd(), "sys"))
from src import globals as g
from src import constants as c
from src.graphics import Graphics


class Entity(object):
    """ Entity base class for all the other entities to build upon.
    """
    
    def __init__(self, x, y, image, movement_speed, rotates=True, collides=True, wall_collides=True):

        """ "x" and "y" should be ints.
            "image" should be a string with the IMAGES identifier
            or a tuple containing both width and height in that order.
            In the latter case, height should be left empty
        """
        self.x = x
        self.y = y
        # Getting width and height from image file
        self.width, self.height = g.images[image].get_size()
        # The current direction the entity is moving.
        self.dir = [0, 0]
        self.x_move_limit = self.y_move_limit = None

        # Variables for checking if the entity has moved.
        self.old_x = x
        self.old_y = y
        # Set picture string
        self.image = image
        # The movement speed of the entity, specified by 1 / movement_speed
        # seconds for each pixel
        self.movement_speed = float(movement_speed)
        # Creates four rectangles for collision checking
        # Format for rects is
        self.rects = {}
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
        # The name in g.special_entity_list of the FollowingEntity following this entity.
        self.following_entity = None
        # If the entity has collided since last check.
        self.collided = False
        self.update_sizes = False

        self.delete = False
        # Update screen
        g.force_update = True
        
    def update(self, delta_remainder):
        """ Updates the entity location if any of the plus and minus variables are set to True
            "delta_remainder" should be the time since the last update in seconds.
            
            moves the enitity one pixel at the time if the delta_remainder is too large
                (Larger than 1 / movement_speed. if so, it subtracts 1 / movement_speed and uses that as the delta, 
                because the entity shouldn't move more than one pixel per update because of collision detection)
        """

        # If the delta value (the time passed) is too large, make sure the entity doesn't move more than one pixel.
        if self.movement_speed > 0:
            while delta_remainder > 0:
                if delta_remainder > (1 / self.movement_speed):
                    delta = (1 / self.movement_speed)
                    delta_remainder = (delta_remainder - delta)
                else:
                    delta = delta_remainder
                    delta_remainder = 0
                # Variables for checking if the entity changed pixel
                if self.x_move_limit is not None:
                    self.x += min(self.movement_speed * delta, abs(self.x_move_limit)) * self.dir[0]
                else:
                    self.x += self.movement_speed * delta * self.dir[0]
                if self.y_move_limit is not None:
                    self.y += min(self.movement_speed * delta, abs(self.y_move_limit)) * self.dir[1]
                else:
                    self.y += self.movement_speed * delta * self.dir[1]

                self.collision_check()

        if self.update_sizes:
            self.update_sizes = False
            self.width, self.height = g.images[self.image].get_size()

        if self.rotates:
            # Rotation logic, which direction is the entity facing and how many degrees should it rotate
            # Uses last angle if the entity is not moving
            if self.dir[0] > 0:
                if self.dir[1] > 0:
                    self.angle = 45
                elif self.dir[1] < 0:
                    self.angle = 135
                else:
                    self.angle = 90
            elif self.dir[0] < 0:
                if self.dir[1] > 0:
                    self.angle = -45
                elif self.dir[1] < 0:
                    self.angle = -135
                else:
                    self.angle = -90
            else:
                if self.dir[1] > 0:
                    self.angle = 0
                elif self.dir[1] < 0:
                    self.angle = 180
                else:
                    self.angle = self.last_angle

            # Update the entity if it's aiming in a new direction
            if self.angle != self.last_angle:
                g.force_update = True
                self.update_sizes = True
            # Remember the angle until next time
            self.last_angle = self.angle

    def tick(self):
        """ Dummy method for what happens every tick
        """
        if self.delete:
            return "delete"

    def paint(self):
        """ Paints the entity on the screen
        """
        if self.rotates:
            # Create a key with the current entity string and the angle
            key = self.image
            if self.angle != 0:
                key += str(self.angle)
            # Check the images dict for a key with the cutrrent entity and rotation
            if key in g.images:
                image = g.images[key].get()
            else:
                # The images dict doesn't have the current sprite with that rotation, create it
                g.images[key] = Graphics(pygame.transform.rotate(g.images[self.image].get(), self.angle))
                image = g.images[key].get()
        else:
            image = g.images[self.image].get()
            
        # Actually paint the object
        if float(int(self.angle / 90.0)) != self.angle / 90.0:
            # Compensate for rotated entities
            g.screen.blit(image, (int(self.x) - int(self.width/5.0),
                          int(self.y) - int(self.height/5.0)))
        else:
            g.screen.blit(image, (int(self.x), int(self.y)))
        
    def has_moved(self, update=True):
        """ Compares an old x and y value with the current one. 
            If the value has changed, the unit has moved to another pixel and should be redrawn.
            update should be 1 if you want to update the checking to a new pixel and 0 if you don't
            
            returns True if the entity has changed pixel and False if it hasn't
        """

        if self.old_x != int(self.x) or self.old_y != int(self.y):
            if update:
                self.old_x = int(self.x)
                self.old_y = int(self.y)
            return True
        else:
            return False
            
    def get_tile(self):
        """ Returns the coordinates of tile the entity is currently on (x and y) 
        """ 
        return int((self.x + self.width/2) / float(c.TILE_SIZE)), int((self.y + self.height/2) / float(c.TILE_SIZE))
    
    def corner_in_tile(self, tile):
        """ Checks if any of the entities corners are inside of the specified tile.
            "tile" should be a tiles.Tile object
        """
        # Get the corners of the entity
        # And get rects for those corners
        corner_rects = []
        for corner in [(self.x, self.y),
                       (self.x + self.width, self.y),
                       (self.x, self.y + self.height),
                       (self.x + self.width, self.y + self.height)]:
            corner_rects.append(Rect(corner, (1, 1)))
        
        if tile.rect().collidelist(corner_rects) != -1:
            return True
        else:
            return False
        
    def update_collision_rects(self):
        """ Method for creating four pygame Rect object along the sides of the entity for use in collision detection 
        """
        self.rects[(-1, 0)] = Rect(self.x + self.width - 1,  # Right
                              self.y + 1,
                              1,
                              self.height - 2)
        
        self.rects[(1, 0)] = Rect(self.x,  # Left
                             self.y + 1,
                             1,
                             self.height - 2)
        
        self.rects[(0, 1)] = Rect(self.x + 1,  # Top
                            self.y,
                            self.width - 2,
                            1)

        self.rects[(0, -1)] = Rect(self.x + 1,
                               self.y + self.height - 1,  # Bottom
                               self.width - 2,
                               1)

    def collision_check(self):
        """ Method for checking if the entity has run into a tree or something
            and move it back a pixel if it has
        """
        if self.wall_collides:
            # Move the entity inside of the window (border collision)
            entity_rect = Rect(self.x, self.y, self.width,self.height)
            window_rect = Rect(0, 0, g.width * c.TILE_SIZE, g.height * c.TILE_SIZE)
            if not window_rect.contains(entity_rect):
                entity_rect.clamp_ip(window_rect)
                self.x = entity_rect.left
                self.y = entity_rect.top

        collided = False
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
                        if c.IMAGES[g.map[i][j].type].collides:
                            checked_tiles.append(g.map[i][j].rect())
                    except IndexError:
                        # That index was apparently outside of the map
                        pass

            # Check if each of the zones collides with any of the tiles
            # If so, move it in the appropriate direction, specified in update_collision_rects() as the keys
            for rect in self.rects:
                if self.rects[rect].collidelist(checked_tiles) != -1:
                    self.x += rect[0]
                    self.y += rect[1]
                    collided = True

        self.collided = collided


class FollowingEntity(Entity):
    """ A subclass of Entity that attaches itself to another entity and follows it around.
        Made for packages, could potentially be reused.
    """
    def __init__(self, x, y, image, movement_speed, attached_entity, pull_min, pull_max,
                 rotates=True, collides=True, wall_collides=True, custom_name=None, target_coords=None):
        """ Initalizes the FollowingEntity.
        """
        super(FollowingEntity, self).__init__(x=x, y=y, image=image, movement_speed=movement_speed,
                                              rotates=rotates, collides=collides, wall_collides=wall_collides)

        if attached_entity is not None:
            if g.special_entity_list[attached_entity].following_entity is None:
                g.special_entity_list[attached_entity].following_entity = attached_entity + "-" + image
        self.attached_entity = attached_entity
        self.pull_min = pull_min
        self.pull_max = pull_max
        # The coordinates the entity currently is travelling towards.
        # Should be None if it's currently following the attached_entity.
        # Otherwise, it should be pixel coordinates (example: (45, 120))
        self.target_coords = target_coords
        if custom_name:
            g.special_entity_list[custom_name] = self
            self.custom_name = custom_name
        # if this doesn't have a name or an attached entity it should be a unnamed entity.
        elif attached_entity is not None:
            g.special_entity_list[attached_entity + "-" + image] = self
            self.custom_name = None
        else:
            g.entity_list.append(self)
            self.custom_name = None

    def update(self, time_diff):
        if self.target_coords is None and self.attached_entity is not None:
            # The horizontal and vertical distances between the middle of FollowingEntity
            # and the middle of attached_entity.
            x_dist = (self.x + self.width/2) - (g.special_entity_list[self.attached_entity].x +
                                                g.special_entity_list[self.attached_entity].width / 2)
            y_dist = (self.y + self.height/2) - (g.special_entity_list[self.attached_entity].y +
                                                 g.special_entity_list[self.attached_entity].height / 2)
            # The diagonal distance between the entities.
            dist = math.hypot(self.x - g.special_entity_list[self.attached_entity].x,
                              self.y - g.special_entity_list[self.attached_entity].y)
            pull_max = self.pull_max
            pull_min = self.pull_min
        elif self.target_coords is not None:
            # The entity is currently travelling towards some coordinates.
            x_dist = self.x - self.target_coords[0]
            y_dist = self.y - self.target_coords[1]
            # The diagonal distance between the entities.
            dist = math.hypot(x_dist, y_dist)
            pull_min = 0
            pull_max = g.width*c.TILE_SIZE + g.height*c.TILE_SIZE
        else:
            return

        self.x_move_limit = x_dist
        self.y_move_limit = y_dist
        # If the diagonal distance isn't too far
        if dist < pull_max * 1.5:
            # If it's positive, move left
            if pull_min < x_dist < pull_max:
                self.dir[0] = -1
            # If it's negative, move right
            elif -pull_min > x_dist > -pull_max:
                self.dir[0] = 1
            # If it is outside the range, stop moving
            else:
                self.dir[0] = 0

            # If it's positive, move up
            if pull_min < y_dist < pull_max:
                self.dir[1] = -1
            # If it's negative, move down
            elif -pull_min > y_dist > -pull_max:
                self.dir[1] = 1
            # If it is outside the range, stop moving
            else:
                self.dir[1] = 0
        else:
            self.dir = [0, 0]

        super(FollowingEntity, self).update(time_diff)
        # Code for not getting stuck on terrain.
        if self.collided and not self.has_moved(update=False):
            last_coords = (self.x, self.y)
            moved = False
            if x_dist > 0:
                self.x -= 1
                moved = True
            elif x_dist < 0:
                self.x += 1
                moved = True

            if y_dist > 0:
                self.y -= 1
                moved = True
            elif y_dist < 0:
                self.y += 1
                moved = True
            if moved:
                self.collision_check()
                if last_coords == (self.x, self.y):
                    i, j = self.get_tile()
                    self.target_coords = [i*c.TILE_SIZE + (c.TILE_SIZE - self.width) / 2,
                                          j*c.TILE_SIZE + (c.TILE_SIZE - self.height) / 2]


class PathingEntity(FollowingEntity):
    """ An entity that finds the shortest way between two points without colliding wiht collision tiles.
    """
    def __init__(self, x, y, image, movement_speed, rotates=True,
                 collides=True, wall_collides=True, target_coords=None, custom_name=None):
        """ Initalizes the PathingEntity.
        """
        super(PathingEntity, self).__init__(x=x, y=y, image=image, movement_speed=movement_speed,
                                            attached_entity=None, pull_min=0, pull_max=c.TILE_SIZE*3,
                                            rotates=rotates, collides=collides, wall_collides=wall_collides,
                                            target_coords=target_coords, custom_name=custom_name)
        self.x += (c.TILE_SIZE - self.width) / 2
        self.y += (c.TILE_SIZE - self.height) / 2
        self.target_coords = target_coords
        self.target_tile = None
        self.came_from = []
        self.path = []
        self.paths_end_func = self.stop_moving
        self.home_tile = None
        self.deliver_tile = None
        self.number = None
        self.goods = None
        self.deliver_timer = -1
        self.come_home_timer = None

    def _heuristic_cost_estimate(self, start, end):
        return 10 * (abs(start[0] - end[0]) + abs(start[1] - end[1]))

    def pathfind(self, end):
        """ Finds a path from start to end tiles using A* algorithm
            "start" and "end" are tuples with x and y coordinates of a tile

            returns True if it succeded and False if it couldn't find a path
        """
        start = self.get_tile()
        # The open_dict and closed_dict both follow the format:
        # (key_x, key_y): [f, g, h, (came_from_x, came_from_y)]
        # F, G and H. G is the length to the start tile, H is the Heuristics
        # estimate of the distance to the end tile and F = G + H
        if type(start) != tuple or type(end) != tuple:
            raise Exception("Value passed to PathingEntity.pathfind() is not tuple")

        # The open dictionary is a dictionary keeping the currently checkable tiles
        # The starting tile is identified as not having a came_from-tuple.
        open_dict = {start: [self._heuristic_cost_estimate(start, end), 0,
                             self._heuristic_cost_estimate(start, end)]}
        # The closed dictionary is a dicionary keeping the currently checked tiles
        closed_dict = {}

        current = None
        while len(open_dict.keys()) > 0:
            lowest_value = None
            # Get the lowest value
            for key in open_dict.keys():
                value = open_dict[key][0]
                if lowest_value is None:
                    lowest_value = value
                    current = key
                else:
                    if value < lowest_value:
                        lowest_value = value
                        current = key
            # Move current from the open dictionary to the closed one
            closed_dict[current] = open_dict[current]
            del open_dict[current]

            # If we're done here
            deliver_tile = None
            if g.get_img(*end).collides and current != end:
                # Find a tile next to the target tile to stand on if it collides
                if (g.in_map(current[0] + 1, current[1]) and
                        (current[0] + 1, current[1]) == end):
                    deliver_tile = (current[0] + 1, current[1])
                elif (g.in_map(current[0] - 1, current[1]) and
                        (current[0] - 1, current[1]) == end):
                    deliver_tile = (current[0] - 1, current[1])
                elif (g.in_map(current[0], current[1] + 1) and
                        (current[0], current[1] + 1) == end):
                    deliver_tile = (current[0], current[1] + 1)
                elif (g.in_map(current[0], current[1] - 1) and
                        (current[0], current[1] - 1) == end):
                    deliver_tile = (current[0], current[1] - 1)
            elif current == end:
                deliver_tile = current

            if deliver_tile is not None:
                # closed_dict[current]
                full_path = []
                while current != start:
                    full_path.append(current)
                    current = closed_dict[current][3]
                full_path.reverse()
                self.deliver_tile = deliver_tile
                self.path = full_path
                self.next_target_tile()
                return True

                # # Old version
                # if done is True:
                #     full_path = []
                #     self.deliver_tile = deliver_tile
                #     while len(closed_dict[current]) > 1:
                #         full_path.append(current)
                #         current = closed_dict[current][1]
                #     full_path.reverse()
                #     self.path = full_path
                #     self.next_target_tile()
                #     self.home_tile = self.get_tile()
                #     return

            # Move through all neighbours
            for i in range(current[0]-1, current[0]+2):
                for j in range(current[1]-1, current[1]+2):
                    neighbour = (i, j)
                    if 0 <= neighbour[0] < len(g.map) and 0 <= neighbour[1] < len(g.map[0]):

                        # Get the G score, the cost to go back to the start
                        if neighbour[0] == current[0]:
                            if neighbour[1] == current[1]:
                                continue
                            else:
                                g_score = closed_dict[current][1] + 10
                        else:
                            if neighbour[1] == current[1]:
                                g_score = closed_dict[current][1] + 10
                            else:
                                # Make sure the pathfinding doesn't try to go through blocks diagonally.
                                if (g.get_img(neighbour[0], current[1]).collides and
                                        g.get_img(current[0], neighbour[1]).collides):
                                    # If the blocks on either side of the diagonal walk is collidable, skip this one
                                    closed_dict[neighbour] = None
                                    continue

                                # If it can travel diagonally, give it a cost of the square root of two.
                                g_score = closed_dict[current][1] + 14

                        if c.IMAGES[g.map[neighbour[0]][neighbour[1]].type].collides is False:
                            # Check if this neighbour can be added the the open_dict and do so if so
                            if neighbour not in closed_dict.keys():
                                if neighbour not in open_dict.keys() or g_score < open_dict[neighbour][1]:
                                    h_score = self._heuristic_cost_estimate(neighbour, end)
                                    f_score = g_score + h_score
                                    open_dict[neighbour] = [f_score, g_score, h_score, current]
                        else:
                            closed_dict[neighbour] = None
        self.path = []
        self.stop_moving()
        return False

    def goods_pathfind(self, target_goods):
        """ Finds a path from the start tile, (the current tile of the entity) to the nearest factory tile that
            can recieve the passed-in goods type.
            "goods" should be a string with the type of goods that the entity will be carrying.

            returns True if a suitable tile was found and False if no suitable tile was found
        """

        start = self.get_tile()
        # The open_dict and closed_dict both follow the format:
        # (key_x, key_y): [g, (came_from_x, came_from_y)]
        # This is a simplified version of the pathfind function. It doesn't use heuristics because it doesn't
        # know where to go yet. It only uses the G value, which is the distance to the tile it came from.
        if type(start) != tuple:
            raise Exception("Value given by self.get_tile() to PathingEntity.goods_pathfind() is not tuple")

        # The open dictionary is a dictionary keeping the currently checkable tiles
        # The starting tile is identified as not having a came_from-tuple.
        open_dict = {start: [0]}
        # The closed dictionary is a dicionary keeping the currently checked tiles
        closed_dict = {}

        current = None
        while len(open_dict.keys()) > 0:
            lowest_value = None
            # Get the lowest value
            for key in open_dict.keys():
                value = open_dict[key][0]
                if lowest_value is None:
                    lowest_value = value
                    current = key
                elif value < lowest_value:
                    lowest_value = value
                    current = key
            # Move current from the open dictionary to the closed one
            closed_dict[current] = open_dict[current]
            del open_dict[current]

            # If we're done here
            done = False
            deliver_tiles = []
            # This code block makes sure the items are delivered to the tile next to the tile instead of diagonally

            if (g.in_map(current[0]+1, current[1]) and
                    g.get_img(current[0]+1, current[1]).factory_input):
                deliver_tiles.append((current[0]+1, current[1]))
            elif (g.in_map(current[0]-1, current[1]) and
                    g.get_img(current[0]-1, current[1]).factory_input):
                deliver_tiles.append((current[0]-1, current[1]))
            elif (g.in_map(current[0], current[1]+1) and
                    g.get_img(current[0], current[1]+1).factory_input):
                deliver_tiles.append((current[0], current[1]+1))
            elif (g.in_map(current[0], current[1]-1) and
                    g.get_img(current[0], current[1]-1).factory_input):
                deliver_tiles.append((current[0], current[1]-1))
            if deliver_tiles:
                for deliver_tile in deliver_tiles:
                    try:
                        for good_name in list(g.map[deliver_tile[0]][deliver_tile[1]].requests.keys()):
                            if good_name == target_goods:
                                if g.map[deliver_tile[0]][deliver_tile[1]].requests[target_goods] > 0:
                                    done = True
                                    g.map[deliver_tile[0]][deliver_tile[1]].requests[target_goods] -= 1
                                    break  # Break out of the goods for loop, not the entire while loop
                        if done:
                            break
                    except AttributeError:
                        pass

            if done is True:
                full_path = []
                self.deliver_tile = deliver_tile
                try:
                    while current != start:
                        full_path.append(current)
                        current = closed_dict[current][1]
                except:
                    print(closed_dict)
                    print(full_path)
                    # Trying to understand the heisenbug! D:
                    import pdb, sys
                    e, m, tb = sys.exc_info()
                    pdb.post_mortem(tb)

                full_path.reverse()
                self.path = full_path
                self.next_target_tile()
                self.home_tile = self.get_tile()
                return True

            # Move through all neighbours
            for i in range(current[0]-1, current[0]+2):
                for j in range(current[1]-1, current[1]+2):
                    neighbour = (i, j)
                    if 0 <= neighbour[0] < len(g.map) and 0 <= neighbour[1] < len(g.map[0]):

                        # Get the G score, the cost to go back to the start
                        if neighbour[0] == current[0]:
                            if neighbour[1] == current[1]:
                                continue
                            else:
                                g_score = closed_dict[current][0] + 10
                        else:
                            if neighbour[1] == current[1]:
                                g_score = closed_dict[current][0] + 10
                            else:
                                # Make sure the pathfinding doesn't try to go through blocks diagonally.
                                if (g.get_img(neighbour[0], current[1]).collides and
                                        g.get_img(current[0], neighbour[1]).collides):
                                    # If the blocks on either side of the diagonal walk is collidable, skip this one
                                    if neighbour not in closed_dict:
                                        closed_dict[neighbour] = None
                                    continue

                                # If it can travel diagonally, give it a cost of the square root of two.
                                g_score = closed_dict[current][0] + 14

                        if c.IMAGES[g.map[neighbour[0]][neighbour[1]].type].collides is False or neighbour == start:
                        # Check if this neighbour can be added the the open_dict and do so if so
                            if neighbour not in closed_dict.keys():
                                if neighbour not in open_dict.keys() or g_score < open_dict[neighbour][0]:
                                    open_dict[neighbour] = [g_score, current]
                        else:
                            if neighbour not in closed_dict.keys() and neighbour not in open_dict.keys():
                                closed_dict[neighbour] = None
        self.path = []
        self.stop_moving()
        return False

    def update(self, time_diff):
        """ Calls the super update function as well as check for if the package should be turned into a tile.
        """
        if self.target_coords == [int(self.x), int(self.y)]:
            self.next_target_tile()
        if self.target_tile is not None:
            if (g.get_img(*self.target_tile).collides or
                    (g.get_img(self.get_tile()[0], self.target_tile[1]).collides and
                     g.get_img(self.target_tile[0], self.get_tile()[1]).collides)):
                if len(self.path) > 0:
                    if self.deliver_tile:
                        if not self.pathfind(self.deliver_tile):
                            # If all else fails, destroy the robot
                            if self.home_tile:
                                self.come_home()
                                self.return_request()
                    else:
                        self.pathfind(self.path[-1])
                else:
                    self.paths_end_func()
                    self.path = []
        super(PathingEntity, self).update(time_diff)

    def tick(self):
        return super(PathingEntity, self).tick()


    def stop_moving(self):
        self.target_coords = None
        self.target_tile = None
        g.force_update = True
        if self.rotates:
            self.angle = 0

    def set_target_tile(self, x, y):
        """ Sets the target coordinates this entity will move towards.
        """
        self.target_tile = (x, y)
        self.target_coords = [x * c.TILE_SIZE + (c.TILE_SIZE - self.width) / 2,
                              y * c.TILE_SIZE + (c.TILE_SIZE - self.height) / 2]

    def next_target_tile(self):
        """ Selects the next target tile in the self.path list. The part of pathfinding that actually does the moving.
        """
        if len(self.path) > 0:
            x, y = self.path.pop(0)
            self.set_target_tile(x, y)
        else:
            self.paths_end_func()

    def return_request(self):
        """ When the robot is destroyed under specific circumstances,
            make sure the tile it was travelling to requests new resources
        """
        if self.home_tile and self.deliver_tile != self.home_tile:
            g.map[self.deliver_tile[0]][self.deliver_tile[1]].requests[self.goods] += 1


def free_of_entities(tile):
    """ A function to check if any of the entities has any of its corners inside the specified tile.
    """
    # Loop through all normal entities.
    for entity in g.entity_list:
        if entity.corner_in_tile(tile):
            return False
    # Loop through all special entites
    for entity in list(g.special_entity_list.values()):
        if entity.corner_in_tile(tile):
            return False
    return True
#!/usr/bin/env python
# coding=utf-8
""" Module /src/tiles.py
    TileGame for Python 3
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Module containing the tile class.
    Tiles are the main building block of the game world.
    They have a texture associated, the type attribute 
    corresponds to the c.py IMAGES dictionary paths.
"""
import os, sys
from random import choice, randint

import pygame

sys.path.append(os.path.join(os.getcwd(), "sys"))
import globals as g
import constants as c
import entities

class AreaNotFreeException(Exception):
    """ Is thrown if a multitile is placed in a non-free spot. The spot should always be checked before
        make_tile() is called.
    """
    pass

class Tile(object):
    """ Tile object containing the type and location of the tile.
    """
    
    def __init__(self, type, x, y):
        """ Simple initalizer.
            "type" should be a string from the list of keys in the c.py IMAGES dictionary.
            "x" and "y" should be ints and can be used for finding out where a tile belongs if
                you copy the tile away from the map array in main.py. They are not normally used.
            "timer" should be the time until time_up() is called. If this is the base class
        """
        # Type of tile, for identification purposes.
        # Can be accessed directly, but not for image getting purposes
        # get_image() should be used instead
        self.type = type
        self.x = x
        self.y = y
        # If the tile evolves, get a random timer for that
        if c.IMAGES[type].evolve is not None:
            # Make sure it doesn't get added to tick_tiles twice
            if not c.IMAGES[type].factory_output:
                g.tick_tiles.append([x, y])
            if not c.IMAGES[type].factory_input:
                self.timer = randint(*c.IMAGES[type].evolve[:2])
            else:
                self.timer = None
        else:
            self.timer = None

        if c.IMAGES[type].random and not c.DEACTIVATE_RANDOM_TEXTURES:
            image_keys = []
            for image in list(c.IMAGES.keys()):
                if image.startswith(type) and (image[len(type):].isdigit() or len(image) == len(type)):
                    image_keys.append(image)
            self.image = choice(image_keys)
        else:
            self.image = self.type 
        
    def tick(self):
        """ Method for counting down the block replacement timer.
            Should only be called if the tile is a transforming tile (for example, sapling)
        """
        if self.timer is not None:
            if self.timer < 0:
                self.time_up()
            else:
                self.timer -= 1
    
    def rect(self):
        """ Returns a pygame.Rect object with the same dimensions and location as the tile
        """
        return pygame.Rect(self.x * c.TILE_SIZE, self.y * c.TILE_SIZE,
                           c.TILE_SIZE, c.TILE_SIZE)
    
    def get_image(self):
        """ Returns the random texture string or just the image
        """ 
        return self.image

    
    def time_up(self):
        """ The function that should be called when self.timer has reached 0
            Exchanges this tile for the appropriate tile specified in the c.IMAGES variable
        """
        # Check if the entity evolves
        if c.IMAGES[self.type].evolve is not None:
            has_entities = False
            # Check if any entity is on that tile
            if c.IMAGES[c.IMAGES[self.type].evolve[2]].collides:
                has_entities = not entities.free_of_entities(self)
            if not has_entities:
                make_tile(c.IMAGES[self.type].evolve[2], self.x, self.y)
                g.tick_tiles.remove([self.x, self.y])
                return
        else:
            g.tick_tiles.remove([self.x, self.y])
        
    def __str__(self):
        """ Returns tile type and location (all attributes)
        """
        template = "{id} tile of type {type} at x {x} y {y} with evolve timer {timer}"
        return template.format(id=self.type, x=self.x, y=self.y,
                               type=type(self), timer=self.timer)
    
    def __eq__(self, other):
        """ Compares the type attribute
        """
        return self.type == other.type
    
    def __ne__(self, other):
        """ Compares the type attribute
        """
        return self.type != other.type


class MultiTileHead(Tile):
    """ The top-left tile of any multi-tile. Paints the actual image
    """
    def __init__(self, type, x, y, width, height):
        super(MultiTileHead, self).__init__(type, x, y)
        self.width = width
        self.height = height


class MultiTilePointer(Tile):
    """ The other tiles that aren't the head in a multi-tile. Paints a single, empty pixel.
    """
    def __init__(self, type, x, y, head_x, head_y):
        super(MultiTilePointer, self).__init__(type, x, y)
        self.target = head_x, head_y
        
    def __str__(self):
        """ Returns the normal values and the coordinates of the head.
        """
        template = "{id} tile of type {type} at x {x} y {y} pointing at {target}"
        return template.format(id=self.type, x=self.x, y=self.y,
                               type=type(self), target=self.target)


class FactoryTile(Tile):
    """ A FactoryTile is a tile that gives out or takes in resources and might do something else.
    """
    def __init__(self, type, x, y):
        super(FactoryTile, self).__init__(type, x, y)
        self.goods_timer = -1
        self.inventory = {}
        self.robots = []
        if c.IMAGES[self.type].factory_output:
            g.tick_tiles.append([self.x, self.y])
        # print("Factory_tile of type " + self.type + " was created at " + str(self.x) + ", "+ str(self.y))

    def tick(self):
        """ Decreases the timer until this tile sends new goods. Sets the timer to -1 after it sends goods.
        """
        # If the timer's up, add a timer until the goods can be sent.
        if self.goods_timer == -1:
            can_start_timer = True
            if c.IMAGES[self.type].factory_input:
                for good in c.IMAGES[self.type].factory_input:
                    if good:
                        good_name, good_amount = good
                        # If the tile has the good
                        if good_name in self.inventory:
                            # If the entity has enough of said goods.
                            # If the goods in the inventory >= the amount of goods in the IMAGES list required
                            # start a timer to add the produced goods
                            if not self.inventory[good_name] >= good_amount:
                                can_start_timer = False
                                break
                        else:
                            can_start_timer = False
                            break

            if can_start_timer and c.IMAGES[self.type].factory_input:
                for good_name, good_amount in c.IMAGES[self.type].factory_input:
                    self.inventory[good_name] -= good_amount
                self.goods_timer = c.IMAGES[self.type].factory_timer
                # Set the image to the working image
                if c.IMAGES[self.type].factory_alt_image is not None and not c.IMAGES[self.type].random:
                    self.image = c.IMAGES[self.type].factory_alt_image
                    g.update_map = True

        if self.goods_timer == 0:
            if c.IMAGES[self.type].evolve is not None and self.timer is None:
                self.timer = randint(*c.IMAGES[self.type].evolve[:2])
            else:
                for good in c.IMAGES[self.type].factory_output:
                    if good:
                        good_name, good_amount = good
                        if good_name in self.inventory:
                            self.inventory[good_name] += good_amount
                        else:
                            self.inventory[good_name] = good_amount
            # Reset the image when the factory is done working
            if c.IMAGES[self.type].factory_alt_image is not None and not c.IMAGES[self.type].random:
                self.image = self.type
                g.update_map = True

        if self.goods_timer >= 0:
            self.goods_timer -= 1

        self.send_goods()

        super(FactoryTile, self).tick()

    def send_goods(self):
        """ Sends its goods with a pathfinding robot to the nearest applicable factory if the corresponding
            robot is "home", that is, not outside the building.
            Should be called about every tick
        """
        i = 0
        for good in c.IMAGES[self.type].factory_output:
            if good:
                good_name, good_amount = good
                if c.IMAGES[self.type].factory_input:
                    if not (good_name in self.inventory and self.inventory[good_name] > 0):
                        continue

                # Checks if the robot is at home. True if it is
                if len(self.robots) > i:
                    if type(self.robots[i]) is int and  self.robots[i] >= 0:
                        self.robots[i] -= 1
                    # If it's zero, all the below code happens.
                    if self.robots[i] != 0:
                        continue
                else:
                    self.robots.append(c.ROBOT_RETRY_TIME)
                robot = entities.Robot(self.x * c.TILE_SIZE, self.y * c.TILE_SIZE,
                                       c.GOODS[good_name],
                                       c.ROBOT_MOVEMENT_SPEED)
                if not robot.goods_pathfind(good_name):
                    robot.delete = True
                    self.robots[i] = c.ROBOT_RETRY_TIME
                else:
                    self.robots[i] = robot
                    robot.number = i
                    robot.goods = good_name
                    if c.IMAGES[self.type].factory_input:
                        self.inventory[good_name] -= 1
            i += 1

    def recieve_goods(self, goods_name):
        """ Adds the recieved goods to the inventory of this tile.
        """
        if goods_name in self.inventory:
            self.inventory[goods_name] += 1
        else:
            self.inventory[goods_name] = 1

    def robot_returned(self, number, time=c.ROBOT_LOAD_TIME):
        if len(self.robots) > number:
            self.robots[number] = time
        else:
            self.robots.append(time)


def area_is_free(x, y, width, height):
    """ Checks an area for if a multitile can be placed there
        "x" and "y" is the top left corner tile in the area.
        "width" and "height" is the width and height of the area
            to be checked.
    """
    is_free = True
#     for key in g.special_entity_list.keys():
#         if "areapackage" in key:
#             del g.special_entity_list[key]
    for i in range(x, x+width):
        for j in range(y, y+height):
            # If any of the tiles aren't placeable, it isn't free.
            if c.IMAGES[g.map[i][j].type].placeable is False:
                is_free = False
            else:
#                 units.Package(i * c.TILE_SIZE, j * c.TILE_SIZE, custom_name="areapackage" + str(i) + "." + str(j))
                pass
            if not entities.free_of_entities(g.map[i][j]):
                is_free = False
    return is_free

    
def make_tile(tile_type, x, y, target=None):
    """ Function to create a tile of the appropriate type (Standard, Random and multi-tile)
        Should be used instead of directly creating a specific tile unless it is certain which type
        is needed.
        
        "type" should be a string identifier from IMAGES.
            If it is a random tile, it should be the base form of the identifier
            (for example, "tree" and not "tree1"
        "x" and "y" are the indices of the tile in the "g.map" array
        "target" should be a tuple of coordinates in the tile array if the tile being created is
            a pointer. It should be left empty if the tile isn't a multi-tile pointer.
    """
  
    # Check if where you're placing the tile is subject to a special tile.
    if g.map[x][y]:
        if c.SPECIAL_PLACE_TILES.__contains__(tile_type + "+" + str(g.map[x][y].type)):
            return make_tile(c.SPECIAL_PLACE_TILES[tile_type + "+" + str(g.map[x][y].type)], x, y)

    # If it is a multi-tile
    if c.IMAGES[tile_type].multi_tile is not None:
        width, height = c.IMAGES[tile_type].multi_tile
        if not area_is_free(x, y, width, height):
            raise AreaNotFreeException("The area at x " + x + ", y " + y +
                                       ", with the width " + width + " and the height " +
                                       height + " was not placeable. Please check the area " +
                                       "before attempting to create a multi-tile.")
        # Create pointers
        for i in range(x, x + width):
            for j in range(y, y + height):
                # If it's the top-left tile, skip it
                if x == i and y == j:
                    continue
                # On all others, make pointers
                if c.IMAGES[tile_type].collides:
                    make_tile("collide_pointer", i, j, (x, y))
                else:
                    make_tile("pointer", i, j, (x, y))
        
        tile = MultiTileHead(tile_type, x, y, width, height)
    else:
        # Remove all robots if it's a robot sending factory tile.

        if g.map[x][y] is not None and g.get_img(x, y).factory_output:
            for robot in g.map[x][y].robots:
                if type(robot) is not int:
                    robot.delete = True

        # Check if target was specified. If so, this tile is a pointer.
        if target is not None:
            tile = MultiTilePointer(tile_type, x, y, *target)
        elif c.IMAGES[tile_type].factory_input or c.IMAGES[tile_type].factory_output:
            tile = FactoryTile(tile_type, x, y)
        else:
            tile = Tile(tile_type, x, y)
    # Change and update the map
    g.map[x][y] = tile
    g.update_map = True
    # Make sure the player doesn't have to move to remove a newly placed package
    if "player" in g.special_entity_list:
        if g.special_entity_list["player"].get_aim_tile() == (x, y):
            g.special_entity_list["player"].update_aim_tile = True
    return tile


def destroy_tile(x, y):
    # If the old tile was a multitile head or pointer
    if (g.map[x][y] and (type(g.map[x][y]) == MultiTileHead or
            type(g.map[x][y]) == MultiTilePointer)):
        # Get the destroy value
        if type(g.map[x][y]) == MultiTileHead:
            destroy_value = c.IMAGES[g.map[x][y].type].destroy
            multi_tile = {"x": x, "y": y,
                          "width": g.map[x][y].width,
                          "height": g.map[x][y].height} 
        else:
            target_x, target_y = g.map[x][y].target
            destroy_value = c.IMAGES[g.map[target_x][target_y].type].destroy
            try:
                multi_tile = {"x": target_x, "y": target_y,
                              "width": g.map[target_x][target_y].width,
                              "height": g.map[target_x][target_y].height}
            except:
                raise "Failed to destroy a multitile. Please implement a fix."

        for i in range(multi_tile["x"], multi_tile["x"] + multi_tile["width"]):
            for j in range(multi_tile["y"], multi_tile["y"] + multi_tile["height"]):
                if i == x and j == y:
                    continue
                if len(destroy_value) > 2:
                    make_tile(destroy_value[2], i, j)
                else:
                    make_tile(destroy_value[1], i, j)
        make_tile(destroy_value[1], x, y)
    else:
        make_tile(c.IMAGES[g.map[x][y].type].destroy[1], x, y)
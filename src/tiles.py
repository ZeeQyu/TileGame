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
from random import choice, randint

import pygame
from src.graphics import Graphics
from src import globals as g, units
from src import constants as c
from src import entities


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


class MicroTile(Tile):
    """ A kind of tile that uses four corner pieces to construct many different variations based on surrounding tiles.
        For detailed information, please see doc/microtiles.txt
    """
    def __init__(self, type, x, y):
        super(MicroTile, self).__init__(type, x, y)
        self.update_microtile = True

    def get_image(self):
        """ Returns the image unless microtiles need to be updated. If so, this checks surrounding tiles for
            the constellation of neighbours and either creates it from quarters or gets a cached one from
            the image list.

            Microtile combinations are named after the constellation of surrounding squares it represents,
            using a 8 character binary combination corresponding to neighbours in a clockwise rotational order
        """
        if not c.DEACTIVATE_MICROTILES:
            if g.update_microtiles or self.update_microtile:
                self.update_microtile = False
                # This is a list of 8 ones or zeros denoting which neighbour tiles are of the same type
                # It's a list because strings can't be easily modified
                shape_list = []

                # Add all neighbours in clockwise order, starting with top left corner
                for relative_x, relative_y in [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]:
                    shape_list.append(str(int(_compare_tile(self.type, self.x + relative_x, self.y + relative_y))))
                # Removes lonely corners (see doc/microtiles.txt)
                for i in range(0, 7, 2):
                    if shape_list[i - 1] == "0" or shape_list[i + 1] == "0":
                        shape_list[i] = "0"
                # Convert to a string
                shape = "".join(shape_list)
                if self.type + shape in g.images:
                    self.image = self.type + shape
                else:
                    # If the tile doesn't exist, create it
                    new_image = pygame.Surface((c.TILE_SIZE, c.TILE_SIZE))
                    # Defines which quartet is being manipulated, clockwise, starting with top left
                    pos = -1

                    for j in range(0, 7, 2):
                        pos += 1
                        corner = shape[j-1] + shape[j] + shape[j+1]
                        quartet_number, rotation, mirror = c.MICROTILE_LEGEND[corner]
                        # Find the corresponding quartet
                        quartet = g.images[c.IMAGES[self.type].microtiles[quartet_number]].get()
                        if mirror:
                            # Mirror the quartet horizontally
                            quartet = pygame.transform.flip(quartet, True, False)
                        if (rotation - pos*90) != 0:
                            quartet = pygame.transform.rotate(quartet, rotation - pos*90)
                        new_image.blit(quartet, (0, 0))

                    g.images[self.type + shape] = Graphics(new_image)
                    self.image = self.type + shape

        return self.image


def _compare_tile(type, x, y):
    """ Compares the type of the tile at the specified coordinate with the specified type.
        Assumes yes if out of bounds.
    """
    if 0 <= x < g.width and 0 <= y < g.height:
        return g.map[x][y].type == type
    else:
        return True


class FactoryTile(Tile):
    """ A FactoryTile is a tile that gives out or takes in resources and might do something else.
    """
    def __init__(self, tile_type, x, y):
        super(FactoryTile, self).__init__(tile_type, x, y)
        # print("Factory_tile of type " + self.type + " was created at " + str(self.x) + ", "+ str(self.y))

        self.goods_timer = -1
        self.robots = []
        if c.IMAGES[self.type].factory_output:
            g.tick_tiles.append([self.x, self.y])

        self.good_targets = {}
        # Contains the last paths for all robots by number. (ex: {1: [(1,5), (1,4), (1,3)], 2: [(65, 33), (66, 33)]}
        self.last_paths = {}
        # Contains last delivery tiles for all robots by number. (example: {1: (2,3), 2: (5,7)}  )
        self.last_delivery_tiles = {}

        self.inventory = {}
        self.requests = {}
        for item in c.IMAGES[self.type].factory_input:
            self.requests[item[0]] = item[1]

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

                if can_start_timer:
                    for good_name, good_amount in c.IMAGES[self.type].factory_input:
                        self.inventory[good_name] -= good_amount
                    self.goods_timer = c.IMAGES[self.type].factory_timer
                    # Make sure it can accept more items if it's not about to evolve.
                    if not c.IMAGES[self.type].evolve is not None:
                        for item in c.IMAGES[self.type].factory_input:
                            self.requests[item[0]] = item[1]
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
        i = -1
        for good in c.IMAGES[self.type].factory_output:
            i += 1
            if good:
                good_name, good_amount = good
                if c.IMAGES[self.type].factory_input:
                    if not (good_name in self.inventory and self.inventory[good_name] > 0):
                        continue

                # Is the robot home?
                if len(self.robots) > i:
                    if type(self.robots[i]) is int and self.robots[i] >= 0:
                        self.robots[i] -= 1
                    # If it's zero, all the below code happens.
                    if self.robots[i] != 0:
                        continue
                else:
                    self.robots.append(c.ROBOT_RETRY_TIME)
                robot = units.Robot(self.x * c.TILE_SIZE, self.y * c.TILE_SIZE,
                                    c.GOODS[good_name][0],
                                    c.ROBOT_MOVEMENT_SPEED)

                # used_last_path = False
                # # Use last path
                # if i in self.last_delivery_tiles and g.get_img(*self.last_delivery_tiles[i]).factory_input:
                #     if (good_name in self.good_targets and
                #             self.good_targets[good_name] == self.last_delivery_tiles[i]):
                #         # Check last path
                #         for tile in self.last_paths[i]:
                #             if g.get_img(*tile).collides:
                #                 used_last_path = True
                #                 break
                #         # Valid path
                #         else:
                #             robot.path = self.last_paths[i]
                #             robot.deliver_tile = self.last_delivery_tiles[i]
                #             robot.next_target_tile()
                #             print("Used last path")

                # if used_last_path is False:
                # Straight pathfind
                can_recieve = False
                if good_name in self.good_targets:
                    for reciever_good in g.get_img(*self.good_targets[good_name]).factory_input:
                        if reciever_good[0] == good_name:
                            can_recieve = True
                    if can_recieve:
                        if robot.pathfind(self.good_targets[good_name], good_name):
                            robot.home_tile = (self.x, self.y)
                        else:
                            can_recieve = False

                # Circular pathfind
                if not can_recieve and not robot.goods_pathfind(good_name):
                    robot.delete = True
                    self.robots[i] = c.ROBOT_RETRY_TIME
                    continue

                # Save the path
                self.last_paths[i] = robot.path
                self.last_delivery_tiles[i] = robot.deliver_tile

                # If any of the pathfindings work
                self.robots[i] = robot
                robot.number = i
                robot.goods = good_name
                if c.IMAGES[self.type].factory_input:
                    self.inventory[good_name] -= 1

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


class LauncherTile(FactoryTile):
    """ A class that is only intended to be used for one tile, the launcher tile.
        The purpose of it is to recieve goods just like a factory tile and then
    """
    def __init__(self, tile_type, x, y):
        super(LauncherTile, self).__init__(tile_type, x, y)
        g.tick_tiles.append([x, y])
        self.shoot_direction = (0, 0)
        self.shoot_timer = -1
        self.angle = 0
        self.last_angle = -1
        # self.inventory["rocket"] = 1

    def send_goods(self):
        """ This is called every tick and overwrites sending object functionality, which Launchers shouldn't have.
        """
        if "rocket" in self.inventory and self.inventory["rocket"] > 0 and self.shoot_timer == -1:
            self.shoot_timer = c.LAUNCHER_SHOOT_SPEED

        if self.shoot_timer == 0 and self.shoot_direction != (0, 0) and\
                "rocket" in self.inventory and self.inventory["rocket"] > 0:
            self.shoot()
        if self.shoot_timer > -1:
            self.shoot_timer -= 1

        # Rotational logic
        if self.shoot_direction == (1, 0):
            self.angle = 90
        elif self.shoot_direction == (-1, 0):
            self.angle = 270
        elif self.shoot_direction == (0, 1):
            self.angle = 0
        elif self.shoot_direction == (0, -1):
            self.angle = 180
        else:
            self.angle = 0

        if self.angle != self.last_angle:
            g.update_map = True
            self.last_angle = self.angle

            # Creating the rotated images
            key = self.type
            if self.angle != 0:
                key += str(self.angle)
            if key in g.images:
                self.image = key
            else:
                g.images[key] = Graphics(pygame.transform.rotate(g.images[self.type].get(), self.angle))
                self.image = key

    def shoot(self):
        if c.NORMAL_DEBUG:
            print("Bang bang, shooting in direction " + str(self.shoot_direction))
        self.inventory["rocket"] -= 1
        g.entity_list.append(units.LauncherRocket(self.x, self.y, self.shoot_direction))


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
    """ Function to create a tile of the appropriate type (Standard, Random, multi-tile and microtiles)
        Should be used instead of directly creating a specific tile unless it is certain which type
        is needed.
        
        "type" should be a string identifier from IMAGES.
            If it is a random tile, it should be the base form of the identifier
            (for example, "tree" and not "tree1"
        "x" and "y" are the indices of the tile in the "g.map" array
        "target" should be a tuple of coordinates in the tile array if the tile being created is
            a pointer. It should be left empty if the tile isn't a multi-tile pointer.
    """
    during_generation = False
    # Check if where you're placing the tile is subject to a special tile.
    if g.map[x][y]:
        if c.SPECIAL_PLACE_TILES.__contains__(tile_type + "+" + str(g.map[x][y].type)):
            return make_tile(c.SPECIAL_PLACE_TILES[tile_type + "+" + str(g.map[x][y].type)], x, y)
    else:
        # If the tile didn't exist before, the entire map is currently being generated
        during_generation = True

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
        if g.map[x][y] is not None and g.get_img(x, y).factory_output and type(g.map[x][y]) is not LauncherTile:
            for robot in g.map[x][y].robots:
                if type(robot) is not int:
                    robot.delete = True
                    robot.return_request()

        # Check if target was specified. If so, this tile is a pointer.
        if target is not None:
            tile = MultiTilePointer(tile_type, x, y, *target)
        elif tile_type == "launcher":
            tile = LauncherTile(tile_type, x, y)
        elif c.IMAGES[tile_type].factory_input or c.IMAGES[tile_type].factory_output:
            tile = FactoryTile(tile_type, x, y)
        elif c.IMAGES[tile_type].microtiles:
            tile = MicroTile(tile_type, x, y)
        else:
            tile = Tile(tile_type, x, y)
    # Change and update the map
    g.map[x][y] = tile
    g.update_map = True
    # Make sure the player doesn't have to move to update to remove a newly placed package
    if "player" in g.special_entity_list:
        if g.special_entity_list["player"].get_aim_tile() == (x, y):
            g.special_entity_list["player"].update_aim_tile = True

    if not during_generation:
        # Make sure microtiles update
        for relative_x in range(-1, 2):
            for relative_y in range(-1, 2):
                if type(g.map[x + relative_x][y + relative_y]) == MicroTile:
                    g.map[x + relative_x][y + relative_y].update_microtile = True

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
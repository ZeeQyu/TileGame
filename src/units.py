#!/usr/bin/env python
# coding=utf-8
""" Module /src/units.py
    TileGame for Python 3
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Units module, containing classes for all friendly and passive units.
"""
import os
import sys
import random
from pygame.rect import Rect

sys.path.append(os.path.join(os.getcwd(), "sys"))
from src import entities
import src.globals as g
import src.constants as c


class Animal(entities.Entity):
    """ Base class for harmless entites that randomly roam about
    """
    def __init__(self, x, y, image, movement_speed, max_travel, collides=True,
                 rotates=True, wall_collides=True):
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
                tick_max = int(float(self.max_travel) / float(self.movement_speed) / float(c.TICK_FREQ))
                # The amount of ticks until direction change, which is a random int
                # between half of tick_max and tick_max
                self.movement_timer = random.randint(int(tick_max / 2), tick_max)
                # Set a random direction
                self.dir = [random.uniform(-1, 1), random.uniform(-1, 1)]
            
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
        self.tile = "package"
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
            g.tile_maker_queue.insert(0, [self.tile, x, y])
            if self.attached_entity is not None:
                g.special_entity_list[self.attached_entity].following_entity = None
                del g.special_entity_list[self.attached_entity + "-" + self.image]
            elif self.custom_name:
                del g.special_entity_list[self.custom_name]
            else:
                del self

            return "deleted"
        super(Package, self).update(time_diff)


class Robot(entities.PathingEntity):
    """ Class for entities that carry goods from one tile to another.
    """
    def __init__(self, x, y, image, movement_speed, rotates=True,
                 collides=True, wall_collides=True, target_coords=None, custom_name=None):
        super(Robot, self).__init__(x=x, y=y, image=image, movement_speed=movement_speed, rotates=rotates,
                         collides=collides, wall_collides=wall_collides,
                         target_coords=target_coords, custom_name=custom_name)
        self.paths_end_func = self._set_deliver_timer

    def goods_pathfind(self, target_goods):
        if super(Robot, self).goods_pathfind(target_goods):
            self.goods = target_goods
            return True
        else:
            return False

    def _set_deliver_timer(self, i=c.ROBOT_DELIVER_TIME):
        self.stop_moving()
        self.deliver_timer = i

    def pathfind(self, end, target_goods=None):
        if target_goods is not None:
            if super(Robot, self).pathfind(end):
                self.goods = target_goods
                x, y = self.deliver_tile
                g.map[x][y].requests[self.goods] -= 1
                return True
            else:
                return False
        else:
            return super(Robot, self).pathfind(end)

    def tick(self):
        if self.deliver_timer == 5:
            self.image = "robot_empty"
            g.force_update = True
        if self.deliver_timer == 0:
            self.give_goods()
            self.image = "robot_empty"
            g.force_update = True
        if self.deliver_timer > -1:
            self.deliver_timer -= 1

        if self.come_home_timer is not None:
            self.come_home_timer -= 1
            if self.come_home_timer <= 0:
                self.come_home()

        return super(Robot, self).tick()

    def give_goods(self):
        try:
            g.map[self.deliver_tile[0]][self.deliver_tile[1]].recieve_goods(self.goods)
        except AttributeError:
            # If the factory tile was replaced, ignore it
            pass
        self.paths_end_func = self.come_home
        if super(Robot, self).pathfind(self.home_tile) is False:
            self.come_home(c.ROBOT_RECONSTRUCT_TIME)

    def come_home(self, time=c.ROBOT_COME_HOME_TIME):
        if self.come_home_timer is not None:
            if self.come_home_timer <= 0:
                self.delete = True
                try:
                    g.map[self.home_tile[0]][self.home_tile[1]].robot_returned(self.number, time)
                except AttributeError:
                    pass
        else:
            self.come_home_timer = c.ROBOT_COME_HOME_TIME


class LauncherRocket(entities.Entity):
    """ A projectile launched by tiles.LauncherTile which is supposed to destroy collidable blocks.
    """
    def __init__(self, tile_x, tile_y, direction):
        super(LauncherRocket, self).__init__(0, 0, "rocket",
                                             movement_speed=c.ROCKET_MOVEMENT_SPEED,
                                             rotates=True, collides=False, wall_collides=False)
        assert direction != (0, 0), "Rockets must have a direction when created"
        self.dir = list(direction)
        width, height = g.images[self.image].get_size()
        print(self.dir)
        if self.dir[1] != 0:
            self.x = tile_x*c.TILE_SIZE + (c.TILE_SIZE-width)/2
            self.y = tile_y*c.TILE_SIZE - height/2 + c.TILE_SIZE*int(bool(self.dir[1] == 1)) - 1*self.dir[1]
        elif self.dir[0] != 0:
            self.x = tile_x*c.TILE_SIZE - height/2 + c.TILE_SIZE*int(bool(self.dir[0] == 1)) - 1*self.dir[0]
            self.y = tile_y*c.TILE_SIZE + (c.TILE_SIZE-width)/2
        # self.x = (tile_x*c.TILE_SIZE + c.TILE_SIZE/2 -
        #           (width if self.dir[0] != 0 else height)/2 +
        #           # Add a halftile times the direction if it's going to the right or left
        #           c.TILE_SIZE*40 * self.dir[0])
        # self.y = (tile_y*c.TILE_SIZE + c.TILE_SIZE/2 -
        #           (height if self.dir[1] != 0 else width)/2 +
        #           # Add a halftile times the direction if it's going to the right or left
        #           c.TILE_SIZE*40 * self.dir[1])

        # self.x = (tile_x * c.TILE_SIZE + self.dir[0] * c.TILE_SIZE +
        #           # If it's travelling vertically, base the x offset off the width
        #           (c.TILE_SIZE-(self.width if self.dir[1] != 0 else self.height)/2))
        # self.y = (tile_y * c.TILE_SIZE + self.dir[1] * c.TILE_SIZE +
        #           # If it's travelling vertically, base the x offset off the width
        #           (c.TILE_SIZE-(self.height if self.dir[0] != 0 else self.width)/2))
        self.dir = direction
        self.tile = "dirt"

    def update(self, delta_remainder):
        if not self.delete:
            super(LauncherRocket, self).update(delta_remainder)
            x, y = self.get_tile()
            # If the tile it will next be in is collidable, destroy it.
            if g.in_map(x+self.dir[0], y+self.dir[1]) and g.get_img(x+self.dir[0], y+self.dir[1]).collides:
                g.tile_maker_queue.insert(0, ["dirt", self.get_tile()[0] + self.dir[0], self.get_tile()[1] + self.dir[1]])
                self.delete = True

    def collision_check(self):
        """ Destroy the rocket if it comes outside of the borders.
        """
        entity_rect = Rect(self.x, self.y, self.width,self.height)
        window_rect = Rect(0, 0, g.width * c.TILE_SIZE, g.height * c.TILE_SIZE)
        if not window_rect.contains(entity_rect):
            self.delete = True
        super(LauncherRocket, self).collision_check()
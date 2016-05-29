#!/usr/bin/env python
# coding=utf-8
""" Module /src/main.py
    TileGame for Python 3
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Main module, run this to start the program. Ties all the other modules together.
    
    TileGame is an experimental tile-based game which serves the purpose of
        letting me learn to use PyGame in a good way and evolving my programming capabilities,
        as well as teaching me how to manage own code in multiple modules properly.
    Features are added at an irregular basis. Check back now and then to the website written above.
    Ideas and goals can be found in the concept.txt file
"""

import time
import os

# Third party modules
import pygame

from src import key_input, tiles
from src import players
from src import maps
from src import graphics
# globals and constants are renamed because they are used very very often.
# This name change is constant through all modules that use them
from src import globals as g
from src import constants as c

    
def main():
    """ Main function, initializes various variables and contains the main program loop.
        Should not be called any other way than running the file or running launch.
        Takes no arguments and returns nothing.
    """
    # initialize pygame
    pygame.init()

    if not os.path.isdir(os.path.join(os.getcwd(), c.GEN_RES_FOLDER)):
        os.mkdir(os.path.join(os.getcwd(), c.GEN_RES_FOLDER))
    # Load graphics
    graphics.prepare_images()
    g.images = graphics.load_graphics()

    # Make map
    maps.load_map(maps.generate_map())
    # maps.load_map()

    # Initiate player
    g.special_entity_list["player"] = players.Player(g.player_start_x, g.player_start_y)
    # Creates a window just the size to fit all the tiles in the map file.
    pygame.display.set_icon(g.images["icon"].get())
    pygame.display.set_caption("TileGame by ZeeQyu", "TileGame")
    g.screen = pygame.display.set_mode((g.width * c.TILE_SIZE,
                                        g.height * c.TILE_SIZE))
    
    # A variable for skipping a single cycle after f.ex. accessing a menu, so that
    # the entities won't fly across the screen
    skip_cycle = False
    
    # Get time once initially and make time variables
    time_last_tick = time_prev = time.clock()
    time_start = time_cycles = time_updates = time_last_sleep = 0
    
    # Main loop
    while True:
        # Make the screen update every frame
        if c.FORCE_UPDATE:
            g.force_update = True
        # Event checker. Allows closing of the program and passes keypresses to the player instance
        key_input.event_check()
        # Tick: Make sure certain things happen on a more regular basis than every frame
        # time_big_diff is the time the cycle took.
        # time_diff (defined below) is the simulated time difference that
        # the entities move after before ticking again in case of a lag spike.
        time_now = time.clock()
        time_big_diff = (time_now - time_prev) * c.GAME_SPEED
        time_prev = time_now

        # Skip the rest of this cycle if a menu was accessed until now
        if skip_cycle:
            skip_cycle = False
            continue
        # FPS meter (shown in console).
        # checks the amount of times this code is run every second and prints that every second.
        time_cycles += 1
        if time_start + 1 < time_now:
            if time_updates == 1 and time_cycles == 1:
                time_updates = 1.0 / time_big_diff
            if c.NORMAL_DEBUG:
                print(time_start, "seconds from start,",  time_cycles, "cycles,", time_updates, "fps")
            time_cycles = 0
            time_updates = 0
            time_start = time_now

        # What happens every tick?
        while time_big_diff > 0:
            if time_big_diff >= c.TICK_FREQ:
                time_diff = c.TICK_FREQ
                time_big_diff -= time_diff
            else:
                time_diff = time_big_diff
                time_big_diff = 0

            if time_last_tick + c.TICK_FREQ <= time_now:
                time_last_tick = time_last_tick + c.TICK_FREQ
                # Tick all the entities (let them do whatever they do every tick
                for i in range(len(g.entity_list)-1, -1, -1):
                    entity = g.entity_list[i]
                    if entity.tick() == "delete":
                        del g.entity_list[i]
                        g.force_update = True
                for entity in list(g.special_entity_list.values()):
                    entity.tick()
                for tile in g.tick_tiles:
                    g.map[tile[0]][tile[1]].tick()
            # Make sure the loop doesn't go too quickly and bog the processor down
            if time_last_sleep < c.SLEEP_TIME:
                time.sleep(c.SLEEP_TIME - time_last_sleep)

            # update all entities
            entity_has_moved = False
            if g.entity_list:
                for i in range(len(g.entity_list)-1, -1, -1):
                    entity = g.entity_list[i]
                    entity.update(time_diff)
                    # Check if any of them have moved
                    if entity.has_moved():
                        entity_has_moved = True
            if g.special_entity_list:
                for entity in list(g.special_entity_list.values()):
                    # Update all entities and check for if any of them is a package that just finished moving.
                    # If so, skip the has_moved check for that entity.
                    if entity.update(time_diff) == "deleted":
                        continue
                    if entity.has_moved():
                        entity_has_moved = True
            if "tile_target" in g.special_entity_list:
                while g.tile_target_selection[0] >= g.width:
                    g.tile_target_selection[0] -= g.width
                while g.tile_target_selection[0] < 0:
                    g.tile_target_selection[0] += g.width

                while g.tile_target_selection[1] >= g.height:
                    g.tile_target_selection[1] -= g.height
                while g.tile_target_selection[1] < 0:
                    g.tile_target_selection[1] += g.height

                g.special_entity_list["tile_target"].x = g.tile_target_selection[0] * c.TILE_SIZE
                g.special_entity_list["tile_target"].y = g.tile_target_selection[1] * c.TILE_SIZE
            if g.non_entity_list:
                for item in list(g.non_entity_list.values()):
                    try:
                        if item.update(time_diff):
                            entity_has_moved = True
                    except AttributeError:
                        pass

            # Check if any tiles need to be updated.
            if g.tile_maker_queue:
                while g.tile_maker_queue:
                    tiles.make_tile(*g.tile_maker_queue.pop())

            # Update map buffer if needed
            if g.update_map:
                g.update_map = False
                g.force_update = True
                g.map_screen_buffer = maps.update_map()
                g.update_microtiles = False

        # If any entity moved, redraw the screen
        if entity_has_moved or g.force_update:
            g.force_update = False
            time_updates += 1
            g.screen.fill(c.BACKGROUND_COLOR)
            # Draw the map buffer on the screen
            g.screen.blit(g.map_screen_buffer, (0, 0))
            # Draw the objects
            for i in range(len(g.entity_list)-1, -1, -1):
                entity = g.entity_list[i]
                entity.paint()
            for i in range(len(list(g.special_entity_list.values()))-1, -1, -1):
                entity = list(g.special_entity_list.values())[i]
                entity.paint()
            for i in range(len(list(g.non_entity_list.values()))-1, -1, -1):
                list(g.non_entity_list.values())[i].paint()
            del entity

            # Update the display
            pygame.display.flip()

if __name__ == '__main__':
    main()
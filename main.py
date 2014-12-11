#!/usr/bin/env python
# coding=utf-8
""" Module /main.py
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

# import normal modules
import sys, os, time

# Third party modules
import pygame

# make sure the own modules in /src can be imported and import them.
sys.path.append(os.path.join(os.getcwd(), "src"))
import tiles, graphics, units, players, interface
import maps
# globals and constants are renamed because they are used very very often.
# This name change is constant through all modules that use them
import globals as g
import constants as c
import pygame.locals as pgl

    
def main():
    """ Main function, initializes various variables and contains the main program loop.
        Should not be called any other way than running the file.
        Takes no arguments and returns nothing.
    """
    # initialize pygame
    pygame.init()

    # Make map
    maps.load_map(maps.generate_map())
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
        for event in pygame.event.get():
            # Quit code
            if event.type == pgl.QUIT:
                sys.exit()
            if event.type == pgl.KEYDOWN or event.type == pgl.KEYUP:
                # Create beetle with (default) a
                if event.type == pgl.KEYDOWN and event.key == g.key_dict["spawn_beetle"][0]:
                    g.entity_list.append(units.Beetle(g.special_entity_list["player"].x,
                                                            g.special_entity_list["player"].y))
                # Duplicate all beetles with (default) D
                elif event.type == pgl.KEYDOWN and event.key == g.key_dict["duplicate_beetles"][0]:
                    # Make an empty list to temporarily store the added beetles, so no infinite loop appears
                    temp_entity_list = []
                    for entity in g.entity_list:
                        if type(entity) == units.Beetle:
                            temp_entity_list.append(units.Beetle(entity.x, entity.y))
                    g.entity_list.extend(temp_entity_list)
                # Remove all beetles
                elif event.type == pgl.KEYDOWN and event.key == g.key_dict["remove_beetles"][0]:
                    # Loop backwards through the g.entity_list
                    for i in range(len(g.entity_list)-1, -1, -1):
                        if type(g.entity_list[i]) == units.Beetle:
                            del g.entity_list[i]
                    g.force_update = True
                # Key configuration
                elif event.type == pgl.KEYDOWN and event.key == c.CONFIG_KEYS_KEY:
                    skip_cycle = g.force_update = True
                    interface.key_reconfig()
                # Otherwise, check for if the player should move
                g.special_entity_list["player"].event_check(event)
                
        # Tick: Make sure certain things happen on a more regular basis than every frame 
        time_now = time.clock()
        time_diff = time_now - time_prev
        # If the time has been more than two seconds, movement might jerk out, so a cycle should be skipped
        if time_prev + 2 < time_now:
            skip_cycle = True
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
                time_updates = 1.0 / time_diff
            if c.NORMAL_DEBUG:
                print(time_start, "seconds from start,",  time_cycles, "cycles,", time_updates, "fps")
            time_cycles = 0
            time_updates = 0
            time_start = time_now
        # What happens every tick?
        if time_last_tick + c.TICK_FREQ < time_now:
            time_last_tick = time_last_tick + c.TICK_FREQ
            # Tick all the entities (let them do whatever they do every tick
            for i in range(len(g.entity_list)-1, -1, -1):
                entity = g.entity_list[i]
                entity.tick()
            for entity in list(g.special_entity_list.values()):
                entity.tick()
            for tile in g.tick_tiles:
                g.map[tile[0]][tile[1]].tick()
        # Make sure the loop doesn't go too quickly and bog the processor down
        if time_last_sleep < c.SLEEP_TIME:
            time.sleep(c.SLEEP_TIME - time_last_sleep)

        # Update map buffer if needed
        if g.update_map:
            g.update_map = False
            g.force_update = True
            g.map_screen_buffer = maps.update_map()
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
                # If so, skip the has_moved check.
                if entity.update(time_diff) == "deleted":
                    continue
                if entity.has_moved():
                    entity_has_moved = True
        
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
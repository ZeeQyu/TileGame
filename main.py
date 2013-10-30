#!/usr/bin/env python
# coding=utf-8
''' Module /main.py
    TileGame
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Main module, run this to start the program. Ties all the other modules together.
    
    TileGame is an experimental tile-based game which serves the purpose of
        letting me learn to use PyGame in a good way and evolving my programming capabilities,
        as well as teaching me how to manage own code in multiple modules properly.
    Features are added at an irregular basis. Check back now and then to the website written above.
    Ideas and goals can be found in the concept.txt file
'''

# import normal modules
import sys, os, time

# Third party modules
import pygame

# make sure the own modules in /src can be imported and import them.
sys.path.append(os.getcwd() + "\\src")
import tiles, graphics, maps, units, globals, players, interface, constants
import pygame.locals as pgl

    
def main():
    ''' Main function, initalizes various variables and contains the main program loop.
        Should not be called any other way than running the file.
        Takes no parameters and returns nothing.
    '''
    # initialize pygame
    pygame.init()
    
    # Make map
    globals.map, globals.width, globals.height, globals.player_start_x, globals.player_start_y = maps.generate_map("map.png")
    # Initiaate player
    globals.entity_list.append(players.Player(globals.player_start_x, globals.player_start_y))

    # Creates a window just the size to fit all the tiles in the map file.
    pygame.display.set_icon(globals.images["icon"].get())
    pygame.display.set_caption("TileGame by ZeeQyu", "TileGame")
    globals.screen = pygame.display.set_mode((globals.width * constants.TILE_SIZE,
                                              globals.height * constants.TILE_SIZE))
    
    # A variable for skipping a single cycle after f.ex. accessing a menu, so that
    # the entities won't fly across the screen
    skip_cycle = False
    
    # Get time once initially and make time variables
    time_last_tick = time_start = time_prev = time.clock()
    time_start = time_cycles = time_updates = time_last_sleep = 0
    
    # Main loop
    while True:
        # Event checker. Allows closing of the program and passes keypresses to the player instance
        for event in pygame.event.get():
            # Quit code
            if event.type == pgl.QUIT:
                sys.exit()
            if event.type == pgl.KEYDOWN or event.type == pgl.KEYUP:
                # Create beetle with (default) space
                if event.type == pgl.KEYDOWN and event.key == globals.key_dict["spawn_beetle"][0]:
                    globals.entity_list.append(units.Beetle(globals.entity_list[0].x, globals.entity_list[0].y))
                # Duplicate all beetles with (default) D
                elif event.type == pgl.KEYDOWN and event.key == globals.key_dict["duplicate_beetles"][0]:
                    # Make an empty list to temporarily store the added beetles, so no infinite loop appears
                    temp_entity_list = []
                    for entity in globals.entity_list:
                        if type(entity) == units.Beetle:
                            temp_entity_list.append(units.Beetle(entity.x, entity.y))
                    globals.entity_list.extend(temp_entity_list)
                    temp_entity_list = []
                # Remove all beetles
                elif event.type == pgl.KEYDOWN and event.key == globals.key_dict["remove_beetles"][0]:
                    # Loop backwards through the globals.entity_list
                    for i in range(len(globals.entity_list)-1, -1, -1):
                        if type(globals.entity_list[i]) == units.Beetle:
                            del globals.entity_list[i]
                    globals.force_update = True
                # Key configuration
                elif event.type == pgl.KEYDOWN and event.key == constants.CONFIG_KEYS_KEY:
                    skip_cycle = globals.force_update = True
                    interface.key_reconfig()
                # Otherwise, check for if the player should move
                globals.entity_list[0].event_check(event)
                
        # Tick: Make sure certain things happen on a more regular basis than every frame 
        time_now = time.clock()
        time_diff = time_now - time_prev
        time_prev = time_now
        # If the time has been more than half an hour, the game has probably been paused
        # and a cycle should be skipped so that the game doesn't freeze
        if time_start + 1800 < time_now:
            skip_cycle = True 
        # Skip the rest of this cycle if a menu was accessed until now
        if skip_cycle:
            skip_cycle = False
            continue
        # FPS meter (shown in console), checks the amount of times this code is run every second and prints that every second.
        time_cycles += 1
        if time_start + 1 < time_now:
            if time_updates == 1 and time_cycles == 1:
                time_updates = 1.0 / (time_diff)
            print time_start, "seconds from start,",  time_cycles, "cycles,", time_updates, "fps"
            time_cycles = 0
            time_updates = 0
            time_start = time_now
        # What happens every tick?
        if time_last_tick + constants.TICK_FREQ < time_now:
            time_last_tick = time_last_tick + constants.TICK_FREQ
            # Tick all the entites (let them do whatever they do every tick
            for entity in globals.entity_list:
                entity.tick()
            globals.entity_list[0].tick()
            for tile in globals.tick_tiles:
                globals.map[tile[0]][tile[1]].tick()
        # Make sure the loop doesn't go too quickly and bog the processor down
        if time_last_sleep < constants.SLEEP_TIME:
            time.sleep(constants.SLEEP_TIME -  time_last_sleep)

        # Update map buffer if needed
        if globals.update_map:
            globals.update_map = False
            globals.force_update = True
            globals.map_screen_buffer = maps.update_map()
        # update all other entities
        entity_has_moved = False
        for entity in globals.entity_list:
            entity.update(time_diff)
            # Check if any of them have moved
            if entity.has_moved():
                entity_has_moved = True
        
        # If any entity moved, redraw the screen
        if entity_has_moved or globals.force_update:
            globals.force_update = False
            time_updates += 1
            globals.screen.fill(constants.BACKGROUND_COLOR)
            # Draw the map buffer on the screen
            globals.screen.blit(globals.map_screen_buffer, (0, 0))
            # Draw the entities
            for entity in globals.entity_list:
                entity.paint()
            # Update the display
            pygame.display.flip()
        
if __name__ == '__main__':
    main()
    
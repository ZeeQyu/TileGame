#!/usr/bin/env python
# coding=utf-8
''' Module /main.py
    TileGame by ZeeQyu
    https://github.com/ZeeQyu/TileGame
    
    Main module, run this to start the program. Ties all the other modules together.
    
    TileGame is an experimental tile-based game which serves the purpose of
        letting me learn to use PyGame in a good way and evolving my programming capabilities,
        as well as teaching me how to manage multiple modules properly.
    Features are added at an irregular basis. Check back now and then to the website written above.
    Ideas and goals can be found in the concept.txt file
'''

# import normal modules
import sys, os, time

# Third party modules
import pygame, Image

# make sure the own modules in /src can be imported and import them.
sys.path.append(os.getcwd() + "\\src")
import tiles, graphics, players, maps, units, globals, players, interface, constants
import pygame.locals as pgl

    
def main():
    ''' Main function, initalizes various variables and contains the main program loop.
        Should not be called any other way than running the file.
        Takes no parameters and returns nothing.
    '''
    # initialize pygame
    pygame.init()
    # Initiate player
    globals.player = players.Player(globals.player_start_x, globals.player_start_y)
    
    # Paint the screen once initially
    force_update = True
    # A variable for skipping a single cycle after f.ex. accessing a menu, so that
    # the entities won't fly across the screen
    skip_cycle = False
    
    # Get time once initially and make time variables
    time_last_tick = time_count = time_prev = time.clock()
    time_count = time_frames = time_updates = time_last_sleep = 0
    
    # Main loop
    while True:
        # Event checker. Allows closing of the program and passes keypresses to the player instance
        for event in pygame.event.get():
            # Quit code
            if event.type == pgl.QUIT:
                sys.exit()
            if event.type == pgl.KEYDOWN or event.type == pgl.KEYUP:
                # Create beetle with (default) space
                if event.type == pgl.KEYDOWN and event.key == globals.key_config["spawn_beetle"]:
                    globals.entity_list.append(units.Beetle(globals.player.x, globals.player.y))
                # Duplicate all beetles with (default) D
                elif event.type == pgl.KEYDOWN and event.key == globals.key_config["duplicate_beetles"]:
                    # Make an empty list to temporarily store the added beetles, so no infinite loop appears
                    temp_entity_list = []
                    for entity in globals.entity_list:
                        if type(entity) == units.Beetle:
                            temp_entity_list.append(units.Beetle(entity.x, entity.y))
                    globals.entity_list.extend(temp_entity_list)
                    temp_entity_list = []
                # Key configuration
                elif event.type == pgl.KEYDOWN and event.key == constants.CHANGE_KEYS_KEY:
                    interface.key_config()
                    time.prev = time.clock()
                # Otherwise, check for if the player should move
                else:
                    globals.player.event_check(event)
                
        # Tick: Make sure certain things happen on a more regular basis than every frame 
        time_now = time.clock()
        time_diff = time_now - time_prev
        time_prev = time_now
        
        # FPS meter (shown in console), checks the amount of times this code is run every second and prints that every second.
        time_frames += 1
        if time_count + 1 < time_now:
            print time_count, "seconds from start,",  time_frames, "cycles,", time_updates, "fps"
            time_frames = 0
            time_updates = 0
            time_count = time_now
            
        # What happens every tick?
        if time_last_tick + constants.TICK_FREQ < time_now:
            time_last_tick = time_last_tick + constants.TICK_FREQ
            # Tick all the entites (let them do whatever they do every tick
            for entity in globals.entity_list:
                entity.tick()
            globals.player.tick()
            
        # Make sure the loop doesn't go too quickly and bog the processor down
        if time_last_sleep < constants.SLEEP_TIME:
            time.sleep(constants.SLEEP_TIME -  time_last_sleep)

        # update (move) the player
        globals.player.update(time_diff)
        
        # update all other entities
        entity_has_moved = False
        for entity in globals.entity_list:
            entity.update(time_diff)
            # Check if any of them have moved
            if entity.has_moved():
                entity_has_moved = True
        
        # If any entity moved, redraw the screen
        if globals.player.has_moved() or entity_has_moved or force_update:
            time_updates += 1
            globals.screen.fill(constants.BLACK)
            # Draw the map buffer on the screen
            globals.screen.blit(globals.map_screen_buffer, (0, 0))
            # Draw the entities
            for entity in globals.entity_list:
                entity.paint()
            globals.player.paint()
            # Update the display
            pygame.display.flip()
        
if __name__ == '__main__':
    main()
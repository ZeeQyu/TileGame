#!/usr/bin/env python
# coding=utf-8
''' Module /main.py
    TileGame by ZeeQyu
    https://github.com/ZeeQyu/TileGame
    
    Main module, run this to start the program. Ties all the other modules together.
    
    TileGame is an experimental tile-based game which serves the purpose of letting me learn to use PyGame in a good way.
    Features are added at an irregular basis. Check back now and then to the website written above.
'''

# import normal modules
import pygame, sys, os, Image, time
from pygame.locals import *

# make sure the own modules in /src can be imported and import them.
sys.path.append(os.getcwd() + "\\src")
import tiles, graphics, players, maps, units, globals
from constants import *

    
def main():
    ''' Main function, initalizes various variables and contains the main program loop.
        Should not be called any other way than running the file.
        Takes no parameters and returns nothing.
    '''
    # initialize pygame
    pygame.init()
    # Initiate player
    player = players.Player(globals.player_start_x, globals.player_start_y)
    
    for i in range(2500):
        globals.entity_list.append(units.Beetle(200, 200, collides=False))
    
    # Paint the screen once initally
    map_screen_buffer = maps.update_map()
    globals.screen.blit(map_screen_buffer, (0, 0))
    player.paint()
    pygame.display.flip()
    
    # Get time once initially and make time variables
    time_last_tick = time_count = time_prev = time.clock()
    time_count = time_frames = time_updates = time_last_sleep = 0
    
    # Main loop
    while True:
        # Event checker. Allows closing of the program and passes keypresses to the player instance
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN or event.type == KEYUP:
                if event.type == KEYDOWN and event.key == K_SPACE:
                    globals.entity_list.append(units.Beetle(player.x, player.y))
                else:
                    player.event_check(event)
                
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
        if time_last_tick + TICK_FREQ < time_now:
            time_last_tick = time_last_tick + TICK_FREQ
            # Tick all the entites (let them do whatever they do every tick
            for entity in globals.entity_list:
                entity.tick()
            player.tick()
            
        # Make sure the loop doesn't go too quickly and bog the processor down
        if time_last_sleep < SLEEP_TIME:
            time.sleep(SLEEP_TIME -  time_last_sleep)

        # update (move) the player
        player.update(time_diff)
        
        # update all other entities
        entity_has_moved = False
        for entity in globals.entity_list:
            entity.update(time_diff)
            # Check if any of them have moved
            if entity.has_moved():
                entity_has_moved = True
        
        # If any entity moved, redraw the screen
        if player.has_moved() or entity_has_moved:
            time_updates += 1
            globals.screen.fill(BLACK)
            # Draw the map buffer on the screen
            globals.screen.blit(map_screen_buffer, (0, 0))
            # Draw the entities
            for entity in globals.entity_list:
                entity.paint()
            player.paint()
            # Update the display
            pygame.display.flip()
        
if __name__ == '__main__':
    main()
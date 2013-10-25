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
import tiles, graphics, players, maps, units
from constants import *

    
def main():
    ''' Main function, initalizes various variables and contains the main program loop.
        Should not be called any other way than running the file.
        Takes no parameters and returns nothing.
    '''
    # initialize pygame and load graphics
    pygame.init()
    images = graphics.load_graphics()
    
    # Load map using functions from maps.py and store into the map variable
    # Get the size of the image as well as the player start point from the map.png file.
    map, width, height, player_start_x, player_start_y = maps.generate_map("map.png")
    
    # Creates a windows just the size to fit all the tiles in the map file.
    screen = pygame.display.set_mode((width * 16, height * 16))
    
    # Initiate player
    player = players.Player(player_start_x, player_start_y, "player", images["player"].get_size())

    # Initiate an entity list. Order of this list does not matter
    entity_list = []
    # Manually add a bunch of beetles
    for i in range(50):
        entity_list.append(units.Beetle(30 * 16, 25 * 16, images["beetle"].get_size()))
    
    # Paint the screen once initally
    map_screen_buffer = maps.update_map(map, images)
    screen.blit(map_screen_buffer, (0, 0))
    player.paint(screen, images["player"].get())
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
            for entity in entity_list:
                entity.tick()
            
        # Make sure the loop doesn't go too quickly and bog the processor down
        if time_last_sleep < SLEEP_TIME:
            time.sleep(SLEEP_TIME -  time_last_sleep)

        # update (move) the player
        player.update(time_diff)
        
        # update all other entities
        entity_has_moved = False
        for entity in entity_list:
            entity.update(time_diff)
            # Check if any of them have moved
            if entity.has_moved():
                entity_has_moved = True
        
        # If any entity moved, redraw the screen
        if player.has_moved() or entity_has_moved:
            time_updates += 1
            screen.fill(BLACK)
            # Draw the map buffer on the screen
            screen.blit(map_screen_buffer, (0, 0))
            # Draw the entities
            for entity in entity_list:
                entity.paint(screen, images[entity.image].get())
            player.paint(screen, images["player"].get())
                
            pygame.display.flip()
        
if __name__ == '__main__':
    main()
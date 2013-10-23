''' Module /main.py
    TileGame by ZeeQyu
    https://github.com/ZeeQyu/TileGame
    
    Main module, run this to start the program. Ties all the other modules together.
    
    TileGame is an experimental tile-based game which serves the purpose of letting me learn to use PyGame in a good way.
    Features are added at an irregular basis. Check back now and then to the website written above.
'''

# import normal modules
import pygame, sys, os, Image, threading, time
from pygame.locals import *

# make sure the own modules in /src can be imported and import them.
sys.path.append(os.getcwd() + "\\src")
import tiles, graphics, players, maps
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
     
    player = players.Player(player_start_x, player_start_y, images["player"].get().get_width(), images["player"].get().get_height())
    
    # Paint the screen once initally
#     maps.paint_map(screen, map, images)
    map_screen_buffer = maps.update_map(map, images)
    screen.blit(map_screen_buffer, (0, 0))
    player.paint(screen, images["player"].get())
    pygame.display.flip()
    
    # Get time once initially and make time variables
    time_last_tick = time_count = time_prev = time.clock()
    time_count = time_frames = 0
    
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
        time_frames = time_frames + 1
        if time_count + 1 < time_now:
            print time_count, time_frames, "fps, frametime:", 1000.0/time_frames
            time_frames = 0
            time_count = time_now
            
        # What happens every tick?
        if time_last_tick + TICK_FREQ < time_now:
            time_last_tick = time_last_tick + TICK_FREQ

        # update (move) the player and only repaint the screen if the player changed which pixel it's painted at.
        player.update(time_diff)
        
        if player.has_moved():
            screen.fill(BLACK)
            screen.blit(map_screen_buffer, (0, 0))
            player.paint(screen, images["player"].get())
            pygame.display.flip()
        
if __name__ == '__main__':
    main()
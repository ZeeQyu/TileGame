import pygame, sys, os, Image, threading, time
from pygame.locals import *

sys.path.append(os.getcwd() + "\\src")

from tiles import *
from graphics import *
from constants import *
from player import *
from map import *
        

    
def main():
    pygame.init()
    images = {}
    for key in IMAGES.keys():
        images[key] = Graphics(key)
    
    map_image = get_map("map.png")
    map, width, height, player_start_x, player_start_y = generate_map(map_image)
        
    screen = pygame.display.set_mode((width * 16, height * 16))
    player = Player(player_start_x, player_start_y)
    
    paint_map(screen, map, images)
    player.paint(screen, images["player"].get())
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            print event
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN or event.type == KEYUP:
                player.event_check(event)
                
        player.update()
        if player.has_moved():
            paint_map(screen, map, images)
            player.paint(screen, images["player"].get())
            pygame.display.flip()
        
if __name__ == '__main__':
    main()
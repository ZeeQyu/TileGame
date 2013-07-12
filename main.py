import pygame, sys, os, Image, threading, time
from pygame.locals import *

sys.path.append(os.getcwd() + "\\src")

from tiles import *
from graphics import *
from constants import *
from player import *
from map import *
        
def update_player(screen, player, x_change, y_change, image):
    player.x = player.x + x_change
    player.y = player.y + y_change
    screen.blit(image, (player.x, player.y))
    
def main():
    pygame.init()
#     listener = EventListener()
#     listener.start()
    images = {}
    for key in IMAGES.keys():
        images[key] = Graphics(key)
    
    map_image = get_map("map.png")
    map, width, height, player_start_x, player_start_y = generate_map(map_image)
        
    screen = pygame.display.set_mode((width * 16, height * 16))
    paint_map(screen, map, images)
    
    player = Player(player_start_x, player_start_y)
    update_player(screen, player, 0, 0, images["player"].get())

    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

if __name__ == '__main__':
    main()
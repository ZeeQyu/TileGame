import pygame, sys, os
from pygame.locals import *
sys.path.append(os.getcwd() + "\\src")
import tiles, graphics


def main():
    pygame.init()
    images = {}
    for key in graphics.PATHS.keys():
        images[key] = graphics.Graphics(key)
    screen = pygame.display.set_mode((600, 600)) 
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()


if __name__ == '__main__':
    main()
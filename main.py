import pygame, sys, os, Image
from pygame.locals import *
sys.path.append(os.getcwd() + "\\src")
from tiles import *
from graphics import *
from constants import *

DEBUG = False

class InvalidColorException(Exception):
    pass

def get_map(map_name):
    return Image.open("res\\" + map_name)

def generate_map(map_image):
    pixels = map_image.load()
    map = []
    width, height = map_image.size
    for y in range(height):
        map.append([])
        
        if DEBUG: print y,
        
        for x in range(width):
            pixel = pixels[x, y]
            type = pixel_type(pixel, x, y)
            
            tile = Tile(type, x, y)
            
            if DEBUG: print x, pixel, "--",
        if DEBUG: print
    
def pixel_type(pixel, x, y):
    if pixel == WHITE:
        return "grass"
    elif pixel == BLACK:
        return "rock"
    elif pixel == YELLOW:
        return "ore"
    elif pixel == PURPLE:
        return "start_point"
    elif pixel == GRAY:
        return "tree"
    elif pixel == RED:
        return "package"
    elif pixel == ORANGE:
        return "hq"
    else:
        raise InvalidColorException("The pixel at x:", x, "y:", y, "in the map file is not a valid color. The RGB is", str(pixel))
    
def main():
    pygame.init()
    images = {}
    for key in PATHS.keys():
        images[key] = Graphics(key)
    map_image = get_map("map.png")
    generate_map(map_image)
    
    screen = pygame.display.set_mode((600, 600))
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()


if __name__ == '__main__':
    main()
import pygame, sys, os, Image
from pygame.locals import *
sys.path.append(os.getcwd() + "\\src")

from tiles import *
from graphics import *
from constants import *

# Debug = 1: debug messages. Debug = 0: no debug messages.
DEBUG = 1

class InvalidColorException(Exception):
    pass

def get_map(map_name):
    return Image.open("res\\" + map_name)

def generate_map(map_image):
    pixels = map_image.load()
    map = []
    width, height = map_image.size
    for x in range(width):
        map.append([])
        
        if DEBUG: print "x:", x,
        
        for y in range(height):
            pixel = pixels[x, y]
            type = pixel_type(pixel, x, y)
            
            tile = Tile(type, x, y)
            map[x].append(tile)
            
            if DEBUG: print "y:", y, pixel, type, "|",
        if DEBUG: print
    return map, width, height
    
def pixel_type(pixel, x, y):
    for key in TILES:
        # if the RGB value in TILES actually has a value
        if TILES[key][1] != 0:
            if pixel == TILES[key][1]:
                return key
    raise InvalidColorException("The pixel at x:", x, "y:", y, "in the map file is not a valid color. The RGB is", str(pixel))
    
def paint_map(screen, map, images):
    screen.fill(BLACK)
    for i in range(len(map)):
        for j in range(len(map[i])):
            image = images[map[i][j].type].get()
            screen.blit(image, (i*16, j*16))
    pygame.display.flip()
            
    
def main():
    pygame.init()
    images = {}
    for key in TILES.keys():
        images[key] = Graphics(key)
    map_image = get_map("map.png")
    map, width, height = generate_map(map_image)
    
    screen = pygame.display.set_mode((width * 16, height * 16))
    paint_map(screen, map, images)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()


if __name__ == '__main__':
    main()
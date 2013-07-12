from constants import *
from tiles import *
import Image

class InvalidMapColorException(Exception):
    pass

def get_map(map_name):
    return Image.open("res\\" + map_name)

def generate_map(map_image):
    pixels = map_image.load()
    map = []
    width, height = map_image.size
    for x in range(width):
        map.append([])
        
        for y in range(height):
            pixel = pixels[x, y]
            type = pixel_type(pixel, x, y)
            if type == "start_tile":
                player_start_x = x * 16
                player_start_y = y * 16
            
            tile = Tile(type, x, y)
            map[x].append(tile)
            
    return map, width, height, player_start_x, player_start_y
    
def pixel_type(pixel, x, y):
    for key in IMAGES:
        # if the RGB value in TILES actually has a value
        if IMAGES[key][1] != 0:
            if pixel == IMAGES[key][1]:
                return key
    raise InvalidMapColorException("The pixel at x:", x, "y:", y, "in the map file is not a valid color. The RGB is", str(pixel))
    
def paint_map(screen, map, images):
    screen.fill(BLACK)
    for i in range(len(map)):
        for j in range(len(map[i])):
            image = images[map[i][j].type].get()
            screen.blit(image, (i*16, j*16))

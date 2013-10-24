#!/usr/bin/python
# coding=utf-8
''' Module /src/graphics.py
    TileGame by ZeeQyu
    https://github.com/ZeeQyu/TileGame
    
    Module containing the Graphics class.
    Uses pygame image objects.
'''

import pygame
import Image
from constants import *
   
class Graphics(object):
    ''' Graphics object containing an image. Loads the image by itself.
    '''
 
    def __init__(self, name):
        ''' "name" should be one of the keys in the constants.py IMAGES dictionary
            Will load the corresponding image from the /res folder.
        '''
        self.image = pygame.image.load("res\\" + IMAGES[name][0])
    
    def get(self):
        ''' returns the contained image
        '''
        return self.image
    
    def get_size(self):
        ''' returns a tuple containing the width and height of the image 
        '''
        return (self.get().get_width(), self.get().get_height())
    
def load_graphics():
    ''' Creates a dictionary with the keys from the constants.py IMAGES dictionary keys
        and a Graphics object created using that key.
        
        returns that dictionary
    '''
    
    images = {}
    for key in IMAGES.keys():
        images[key] = Graphics(key)
    return images
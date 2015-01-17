#!/usr/bin/env python
# coding=utf-8
""" Module /src/graphics.py
    TileGame for Python 3
    Code and lead design by ZeeQyu
    Graphics by Pokemania00
    https://github.com/ZeeQyu/TileGame
    
    Module containing the Graphics class.
    Uses pygame image objects.
"""
import os
import sys

import pygame


sys.path.append(os.path.join(os.getcwd(), "sys"))
from src import constants as c


class Graphics(object):
    """ Graphics object containing an image. Loads the image by itself.
    """
 
    def __init__(self, name):
        """ "name" should be one of the keys in the constants.py IMAGES dictionary
            Will load the corresponding image from the /res folder.
        """
        if type(name) == str:
            # if c.NORMAL_DEBUG:
            #     print(os.path.join(os.getcwd(), c.RES_FOLDER, c.IMAGES[name].png))
            self.image = pygame.image.load(os.path.join(os.getcwd(), c.RES_FOLDER, c.IMAGES[name].png))
        elif type(name) == pygame.Surface:
            self.image = name 
    
    def get(self):
        """ returns the contained image
        """
        return self.image
    
    def get_size(self):
        """ returns a tuple containing the width and height of the image 
        """
        return (self.get().get_width(), self.get().get_height())
    
def load_graphics():
    """ Creates a dictionary with the keys from the constants.py IMAGES dictionary keys
        and a Graphics object created using that key.
        
        returns that dictionary
    """
    images = {}
    for key in list(c.IMAGES.keys()):
        images[key] = Graphics(key)
    return images
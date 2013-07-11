import pygame
import Image
from constants import *
   
class Graphics(object):
 
    def __init__(self, name):
        self.image = pygame.image.load("res\\" + TILES[name][0])
    
    def get(self):
        return self.image
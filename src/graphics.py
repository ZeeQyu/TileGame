import pygame
import Image
from constants import *
   
class Graphics():
 
    def __init__(self, name):
        self.image = pygame.image.load("res\\" + TILES[name][0])
    
    def get(self):
        return image
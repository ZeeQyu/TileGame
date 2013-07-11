import pygame
import Image
from constants import *
   
class Graphics():
 
    def __init__(self, name):
        self.image = Image.open("res\\" + PATHS[name][0])
    
    def get(self):
        return image
import pygame

class Tile():
    
    def __init__(self, type, x, y):
        
        self.type = type
        self.x = x
        self.y = y
        
    def __str__(self):
        return "{type} tile at x {x} y {y}".format(type=self.type, x=self.x, y=self.y)
    
    def __eq__(self, other):
        return self.type == other.type
    
    def __ne__(self, other):
        return self.type != other.type
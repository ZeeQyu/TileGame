import pygame
import Image
PATHS = {
         "grass1": "grassTile1.png",
         "grass2": "grassTile2.png",
         "grass3": "grassTile3.png",
         "grass4": "grassTile4.png",
         "grass5": "grassTile5.png",
         "grass6": "grassTile6.png",
         "grass7": "grassTile7.png",
         "grass8": "grassTile8.png",
         "grass9": "grassTile9.png",
         "grass10": "grassTile10.png",
         "grass11": "grassTile11.png",
         "grass12": "grassTile12.png",
         "grass13": "grassTile13.png",
         "grass14": "grassTile14.png",
         "grass15": "grassTile15.png",
         "grass16": "grassTile16.png",
         "dirt": "dirtTile.png"
                 }
   
class Graphics():
 
    def __init__(self, name):
        self.image = Image.open("res\\" + PATHS[name])
    
    def get(self):
        return image
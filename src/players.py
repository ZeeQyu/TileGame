''' Module /src/players.py
    TileGame by ZeeQyu
    https://github.com/ZeeQyu/TileGame
    
    Module containing the player class.
    Also handles key press events for movement of the player.
'''

from constants import *
from pygame.locals import *
from entities import Entity

class Player(Entity):
    ''' Player class. Uses the image from the "player" key from the IMAGES dictionary in constants.py
    '''
    
    def __init__(self, x, y, width, height, image):
        ''' "x" and "y" should be ints.
            "image" should be the string identifier in IMAGES that the player should use
        '''
        image = "player"
        super(Player, self).__init__(x, y, width, height, image)
        # Set movement speed
        self.movement_speed = PLAYER_MOVEMENT_SPEED
        
    def event_check(self, event):
        ''' Event checker. Checks if the event is a key press or release on the arrow keys.
        '''
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                self.x_plus = True
            elif event.key == K_LEFT:
                self.x_minus = True
            elif event.key == K_DOWN:
                self.y_plus = True
            elif event.key == K_UP:
                self.y_minus = True
                
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                self.x_plus = False
            elif event.key == K_LEFT:
                self.x_minus = False
            elif event.key == K_DOWN:
                self.y_plus = False
            elif event.key == K_UP:
                self.y_minus = False

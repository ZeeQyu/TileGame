''' Module /src/players.py
    TileGame by ZeeQyu
    https://github.com/ZeeQyu/TileGame
    
    Module containing the player class.
    Also handles key press events for movement of the player.
'''

from constants import *
from pygame.locals import *

class Player(object):
    ''' Player class. Uses the image from the "player" key from the IMAGES dictionary in constants.py
    '''
    
    def __init__(self, x, y):
        ''' "x" and "y" should be ints.
        '''
        self.x = x
        self.y = y
        # Variables for checking if the player should move.
        self.x_plus = False
        self.x_minus = False
        self.y_plus = False
        self.y_minus = False
        #Variables for checking if the player has moved.
        self.old_x = x
        self.old_y = y
        
    def update(self, delta):
        ''' Updates the player location if any of the plus and minus variables are set to True using arrow key events
            delta should be the time since the last update in seconds.
            
            returns the remainder of the delta in seconds if the delta is too large 
                (Larger than 1 / MOVEMENT_SPEED. if so, it subtracts 1 / MOVEMENT_SPEED and uses that as the delta, 
                because the player shouldn't move more than one pixel per update because of collision detection)
        '''
        # If the delta value (the time passed) is too large, make sure the player doesn't move more than one pixel.
        delta_remainder = 0
        if delta > 1 / MOVEMENT_SPEED:
            delta_remainder = delta - (1 / MOVEMENT_SPEED) 
            print "Delta:", delta, "Delta_remainder:", delta_remainder, 1/MOVEMENT_SPEED
            delta = 1 / MOVEMENT_SPEED
            
        # Move the player in the direction the arrow key is pressed in.
        if self.x_plus:
            self.x += MOVEMENT_SPEED * delta
        if self.x_minus:
            self.x -= MOVEMENT_SPEED * delta
        if self.y_plus:
            self.y += MOVEMENT_SPEED * delta
        if self.y_minus:
            self.y -= MOVEMENT_SPEED * delta
        
        return delta_remainder
            
    def paint(self, screen, image):
        ''' Paints the player on the specified screen.
            
            "screen" should be a pygame display
            "image" should be a pygame image object
        '''
        screen.blit(image, (int(self.x), int(self.y)))
    
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
                
    def has_moved(self):
        ''' Compares an old x and y value with the current one. 
            If the value has changed, the character has moved to another pixel and should be redrawn.
            
            returns True if the player has changed pixel and False if it hasn't
        '''
        if self.old_x != int(self.x) or self.old_y != int(self.y):
            self.old_x = int(self.x)
            self.old_y = int(self.y)
            return True
        else:
            return False

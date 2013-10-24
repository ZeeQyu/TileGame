''' Module /src/players.py
    TileGame by ZeeQyu
    https://github.com/ZeeQyu/TileGame
    
    Module containing the player class.
    Also handles key press events for movement of the player.
'''

from constants import *
from pygame.locals import *

class Entity(object):
    ''' Entity class. Uses the image from the "player" key from the IMAGES dictionary in constants.py
    '''
    
    def __init__(self, x, y, image):
        ''' "x" and "y" should be ints.
            "width" and "height" should be ints with the size of the sprite the entity is using 
        '''
        self.x = x
        self.y = y
        # Getting width and height from image file
        self.width = IMAGES[image].get().get_width()
        self.height = IMAGES[image].get().get_height()
        # Variables for checking if the entity should move.
        self.x_plus = False
        self.x_minus = False
        self.y_plus = False
        self.y_minus = False
        # Variables for checking if the entity has moved.
        self.old_x = x
        self.old_y = y
        # Set picture string
        self.image = image
        # Creates four rectangles for collision checking
        self.update_collision_rects()
        
    def update(self, delta_remainder):
        ''' Updates the player location if any of the plus and minus variables are set to True using arrow key events
            delta should be the time since the last update in seconds.
            
            returns the remainder of the delta in seconds if the delta is too large 
                (Larger than 1 / movement_speed. if so, it subtracts 1 / movement_speed and uses that as the delta, 
                because the player shouldn't move more than one pixel per update because of collision detection)
        '''
        # If the delta value (the time passed) is too large, make sure the player doesn't move more than one pixel.
        delta = 0
        while delta_remainder > 0:
            if delta > 1 / movement_speed:
                delta_remainder = delta - (1 / movement_speed) 
                print "Delta:", delta, "Delta_remainder:", delta_remainder, 1/movement_speed
                delta = 1 / movement_speed
                delta_remainder = delta_remainder - delta
            else:
                delta = delta_remainder
                delta_remainder = 0
            
            # Move the player in the direction the arrow key is pressed in.
            if self.x_plus:
               self.x += movement_speed * delta
            if self.x_minus:
                self.x -= movement_speed * delta
            if self.y_plus:
                self.y += movement_speed * delta
            if self.y_minus:
                self.y -= movement_speed * delta
                
            # TODO Collision to be put here and in the maps file
    def update_collision_rects(self):
        ''' Method for creating four pygame Rect object along the sides of the entity for use in collision detection 
        '''
        self.col_right = Rect(self.x + self.width - 1, 
                              self.y + 1,
                              1,
                              self.height - 2)
        
        self.col_left = Rect(self.x,
                             self.y + 1,
                             1,
                             self.height - 2)
        
        self.col_top = Rect(self.x + 1,
                            self.y,
                            self.width - 2,
                            1)
        
        self.col_bottom = Rect(self.x + 1,
                               self.y + self.height - 2,
                               self.width - 2,
                               1)
            
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
                
    def has_moved(self, update=1):
        ''' Compares an old x and y value with the current one. 
            If the value has changed, the unit has moved to another pixel and should be redrawn.
            update should be 1 if you want to update the checking to a new pixel and 0 if you don't
            
            returns True if the player has changed pixel and False if it hasn't
        '''
        if self.old_x != int(self.x) or self.old_y != int(self.y):
            if update:
                self.old_x = int(self.x)
                self.old_y = int(self.y)
            return True
        else:
            return False

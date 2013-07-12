from constants import *
from pygame.locals import *

class Player(object):
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_plus = False
        self.x_minus = False
        self.y_plus = False
        self.y_minus = False
        
    def update(self, screen, image):
        if self.x_plus:
            self.x += MOVEMENT_SPEED
        if self.x_minus:
            self.x -= MOVEMENT_SPEED
        if self.y_plus:
            self.y += MOVEMENT_SPEED
        if self.y_minus:
            self.y -= MOVEMENT_SPEED
            
        screen.blit(image, (int(self.x), int(self.y)))
        
    def event_check(self, event):
        print "In event_check"
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
# A class to manage bullet classes

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """
    A general class for a bullet
    """
    
    def __init__(self, ainv_game):
        """
        Initializes a bullet
        """
        
        # creates instance for parent class
        super().__init__()
        self.screen = ainv_game.screen
        self.settings = ainv_game.settings
        self.colour = self.settings.bullet_colour
        
        # create and set posn of bullet rect at (0, 0)
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, 
                                self.settings.bullet_height)
        self.rect.midtop = ainv_game.ship.rect.midtop
        self.y = float(self.rect.y)
        
    def update(self):
        """
        Move bullet up the screen
        """
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
        
    def draw_bullet(self):
        """
        Draw bullet to screen
        """     
        pygame.draw.rect(self.screen, self.colour, self.rect)
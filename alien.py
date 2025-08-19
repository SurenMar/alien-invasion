# A file to manage alien classes

import pygame
from pygame.sprite import Sprite

ALIENS_PER_ROW = 9

class Alien(Sprite):
    """
    Class to represent a single alien
    """
    
    def __init__(self, ainv_game):
        """
        Initializes alien class
        """
        
        super().__init__()
        self.settings = ainv_game.settings
        self.screen_rect = ainv_game.screen_rect
        
        # load alien image
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        
        # start each alien at top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
    def update(self):
        """
        Move alien to the right or left
        """
        self.x += self.settings.alien_speed * self.settings.fleet_dir
        self.rect.x = self.x
        
    def check_edges(self):
        """
        Return True if alien hits screen edge
        """
        return self.rect.right >= self.screen_rect.right or self.rect.left <= 0
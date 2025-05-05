# A file to manage the ships lives remaining

import pygame
from pygame.sprite import Sprite

class ShipLifes(Sprite):
    """
    A class to manage and display remaining lifes
    """
    
    def __init__(self, ainv_game):
        super().__init__()
        
        self.screen = ainv_game.screen
        self.screen_rect = ainv_game.screen_rect
        self.settings = ainv_game.settings
        
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        
        self.rect.topleft = self.screen_rect.topleft
        self.rect.y += 10
        
    def position_life(self, ship_num):
        """
        Positions the ship image depending on what life it represents
        """
        self.rect.x += 15 + (self.rect.width + 5) * ship_num
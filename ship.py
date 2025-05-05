# A class to manage the ship that the user controls

import pygame

class Ship:
    """
    A class to manage the ship
    """
    
    def __init__(self, ainv_game):
        """
        Initializes ship and sets starting position
        """
        # set settings and screen for easy access in this module
        self.screen  = ainv_game.screen
        self.settings = ainv_game.settings
        
        # allows us to place ship at correct location on screen
        self.screen_rect = ainv_game.screen_rect 
        
        # load image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        
        # starting position at mid bottom
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= 20
        
        self.x = float(self.rect.x)
        
        # movement flags
        self.moving_right = False
        self.moving_left = False
        
    def update(self):
        """
        Updates the position of the ship as the user moves right or left
        """
        if self.moving_right and \
            self.rect.right + self.settings.ship_speed <= self.screen_rect.right - 20:
            self.x += self.settings.ship_speed
        elif self.moving_left and \
            self.rect.left - self.settings.ship_speed >= 20:
            self.x -= self.settings.ship_speed
            
        # This is done to work with floats
        self.rect.x = self.x
        
    def blitme(self):
        """
        Draw image at its current location
        """
        self.screen.blit(self.image, self.rect)
        
    
    def centre_ship(self):
        """
        Centers the ship, whenever the ship loses a life
        """
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= 20
        self.x = float(self.rect.x)
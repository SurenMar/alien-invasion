# A file to manage the play button on the game screen

import pygame.font

class PlayButton:
    """
    A class to manage the play button
    """
    
    def __init__(self, ainv_game, msg):
        self.screen = ainv_game.screen
        self.screen_rect = ainv_game.screen_rect
        self.settings = ainv_game.settings
        
        # position button rect
        self.rect = pygame.Rect(0, 0, self.settings.button_width,
                                self.settings.button_height)
        self.rect.center = self.screen_rect.center
        
        # create button text
        self.font = pygame.font.SysFont(self.settings.text_style, 
                                   self.settings.text_size)
        self._prep_msg(msg)
        
    def _prep_msg(self, msg):
        """
        Turn msg into rendered image and position text
        """
        self.text_img = self.font.render(msg, True, self.settings.text_colour,
                                    self.settings.button_colour)
        self.text_rect = self.text_img.get_rect()
        self.text_rect.center = self.rect.center
        
    def draw_button(self):
        """
        Displays button to the screen
        """
        self.screen.fill(self.settings.button_colour, self.rect)
        self.screen.blit(self.text_img, self.text_rect)
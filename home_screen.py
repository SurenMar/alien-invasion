# A file to manage whats displayed in the background of the home screen

import pygame

class HomeScreen:
    """
    A class to manage the homescreen
    """
    
    def __init__(self, ainv_game):
        self.screen = ainv_game.screen
        self.screen_rect = ainv_game.screen_rect
        self.settings = ainv_game.settings
        
    def fill_home_screen(self):
        """
        Fills home screen and adds text
        """
        self.screen.fill(self.settings.hs_colour)
        self._display_welcome_text()
       
    def _display_welcome_text(self):
        """
        Displays and centres welcome text
        """
        self.font = pygame.font.SysFont(self.settings.hs_text_style,
                                        self.settings.hs_text_size)
        self.text_img = self.font.render(self.settings.hs_text, True,
                                         self.settings.hs_text_colour, None)
        self.text_rect = self.text_img.get_rect()
        self.text_rect.center = self.screen_rect.center
        self.text_rect.y -= 130
        
        self.screen.blit(self.text_img, self.text_rect)
        
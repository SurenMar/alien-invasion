# A file to keep track of login buttons

import pygame

class LoginButton:
    """
    A class to manage the two login buttons used on the home screen
    """
    
    def __init__(self, ainv_game, text):
        self.screen = ainv_game.screen
        self.screen_rect = ainv_game.screen_rect
        self.settings = ainv_game.settings
        
        self.font = pygame.font.SysFont(self.settings.login_style,
                                        self.settings.login_size)
        self.text_img = self.font.render(text, True, 
                                         self.settings.login_text_colour)
        self.text_rect = self.text_img.get_rect()
        
        self._create_rect(text)
        self.text_rect.center = self.rect.center
        
    def _create_rect(self, text):
        """
        Creates a Rect for a button with size depending on the button text
        """
        self.rect = pygame.Rect(0, 0, self.text_rect.width + 20,
                                self.settings.login_height)
        self.rect.center = self.screen_rect.center
        self.rect.y += 167
        if text == self.settings.sign_in_text:
            self.rect.x += self.settings.sign_in_adjustment
        elif text == self.settings.sign_up_text:
            self.rect.x += self.settings.sign_up_adjustment
        
    def display_button(self):
        """
        Displays button to the screen
        """
        self.screen.fill(self.settings.login_colour, self.rect)
        self.screen.blit(self.text_img, self.text_rect)
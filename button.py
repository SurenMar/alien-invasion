# A file to manage all buttons classes

import pygame

class Button:
    """
    A class to manage a general button
    """
    
    def __init__(self, ainv_game):
        self.screen = ainv_game.screen
        self.screen_rect = ainv_game.screen_rect
        self.settings = ainv_game.settings
        
    def create_text(self, text, font, size, text_colour):
        font = pygame.font.SysFont(font, size)
        self.text_img = font.render(text, True, text_colour)
        self.text_rect = self.text_img.get_rect()
        
    def create_rect(self, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        
    def position(self, x_adjust, y_adjust):
        self.rect.center = self.screen_rect.center
        self.rect.x += x_adjust
        self.rect.y += y_adjust
        self.text_rect.center = self.rect.center
        
    def display_button(self, colour):
        self.screen.fill(colour, self.rect)
        self.screen.blit(self.text_img, self.text_rect)
        
        
class PlayButton(Button):
    """
    A class for the play button
    """
    
    def __init__(self, ainv_game):
        super().__init__(ainv_game)
        self.create_text(self.settings.start_text, self.settings.play_text_style,
                         self.settings.play_text_size, 
                         self.settings.play_text_colour)
        self.create_rect(self.settings.play_width, self.settings.play_height)
        self.position(self.settings.play_x, self.settings.play_y)
        
    def display_play_button(self):
        self.display_button(self.settings.play_colour)
        
        
class SignInButton(Button):
    """
    A class for the sign in button
    """
    
    def __init__(self, ainv_game):
        super().__init__(ainv_game)
        self.create_text(self.settings.sign_in_text, self.settings.login_style,
                         self.settings.login_size, 
                         self.settings.login_text_colour)
        self.create_rect(self.text_rect.width + 20, self.settings.login_height)
        self.position(self.settings.sign_in_x, self.settings.login_y)
        
    def display_signin_button(self):
        self.display_button(self.settings.login_colour)
        
        
class SignUpButton(Button):
    """
    A class for the sign up button
    """
    
    def __init__(self, ainv_game):
        super().__init__(ainv_game)
        self.create_text(self.settings.sign_up_text, self.settings.login_style,
                         self.settings.login_size, 
                         self.settings.login_text_colour)
        self.create_rect(self.text_rect.width + 20, self.settings.login_height)
        self.position(self.settings.sign_up_x, self.settings.login_y)
        
    def display_signup_button(self):
        self.display_button(self.settings.login_colour)
        
        
    
        
        
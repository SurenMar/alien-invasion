# A class to manage anything to do with the homescreen textbox

import pygame

class Textbox:
    """
    Class to structure a textbox
    """
    
    def __init__(self, ainv_game):
        self.screen = ainv_game.screen
        self.screen_rect = ainv_game.screen_rect
        self.settings = ainv_game.settings
        
        # used to flash the cursor blinker
        self.last_blink = pygame.time.get_ticks()
        
        self.rect = pygame.Rect(0, 0, self.settings.tb_width,
                                self.settings.tb_height)
        self.rect.center = self.screen_rect.center
        self.rect.y += 100
        
        self.font = pygame.font.SysFont(self.settings.tb_font_style,
                                        self.settings.tb_font_size)
        
        self.blinker_rect = pygame.Rect(0, 0, self.settings.blinker_width,
                                        self.settings.blinker_height)
        
    def empty_text(self):
        """
        Creates the textbox text for when the user hasnt typed anything in
        """
        self.text_img = self.font.render(self.settings.empty_text, True,
                                          self.settings.empty_text_colour,
                                          self.settings.tb_bg_colour)
        self.text_rect = self.text_img.get_rect()
        self.text_rect.midleft = self.rect.midleft
        self.text_rect.x += 5
        self._display_text()
        
    def prep_user_text(self, user_text):
        """
        Creates
        """
        self.text_img = self.font.render(user_text, False,
                                          self.settings.user_text_colour)
        self.text_rect = self.text_img.get_rect()
        self.text_rect.midleft = self.rect.midleft
        self.text_rect.x += 5
        self._display_text()
         
    def _display_text(self):
        self.screen.fill(self.settings.tb_bg_colour, self.rect)
        self.screen.blit(self.text_img, self.text_rect)
        
    def display_blinker(self):
        current_time = pygame.time.get_ticks()
            
        if current_time - self.last_blink >= 2 * self.settings.blink_duration:
            self.last_blink = current_time
        elif current_time - self.last_blink >= self.settings.blink_duration:
            None
        else:
            self.blinker_rect.midright = self.text_rect.midright
            self.blinker_rect.x += 4
            self.screen.fill(self.settings.blinker_colour, self.blinker_rect)
        
class TextboxError:
    """
    A class to manage possible user errors when using the textbox
    """
        
    def __init__(self, ainv_game, error_text):
        self.screen = ainv_game.screen
        self.screen_rect = ainv_game.screen_rect
        self.settings = ainv_game.settings
        
        self.error_font = pygame.font.SysFont(self.settings.error_font_style,
                                              self.settings.error_font_size)
        self.error_text_img = self.error_font.render(error_text, False,
                                                self.settings.error_text_colour)
        self.error_text_rect = self.error_text_img.get_rect()
        
        self.error_rect = pygame.Rect(0, 0, self.error_text_rect.width + 50,
                                      self.settings.error_height)
        
        self.error_rect.center = self.screen_rect.center
        self.error_rect.y += 254
        self.error_text_rect.center = self.error_rect.center
        
    def display_error(self):
        self.screen.fill(self.settings.error_colour, self.error_rect)
        self.screen.blit(self.error_text_img, self.error_text_rect)
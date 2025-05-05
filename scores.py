# A file to manage the users current score and level

import pygame.font, pygame.time

class LevelCounter:
    """
    Class to manage the level display
    """
    
    def __init__(self, ainv_game, sb_text):
        self.screen = ainv_game.screen
        self.screen_rect = ainv_game.screen_rect
        self.settings = ainv_game.settings
        self.stats = ainv_game.stats
        
        self.font = pygame.font.SysFont(self.settings.sb_style,
                                        self.settings.sb_size)
        
        self.prep_text(sb_text)
        self.position()
    
    def prep_text(self, text):
        """
        Renders the text of the level or score the player is on/has
        """
        self.sb_img = self.font.render(text, False, 
                                        self.settings.sb_colour, None) 
        self.sb_rect = self.sb_img.get_rect()
        
    def position(self):
        """
        Positions the only level text
        """
        self.sb_rect.topright = self.screen_rect.topright
        self.sb_rect.x -= 20
        self.sb_rect.y += 10
        
    def display_text(self):
        """
        Displays the score or level text
        """
        self.screen.blit(self.sb_img, self.sb_rect)
        
        
class Score(LevelCounter):
    
    def __init__(self, ainv_game, ):
        super().__init__(ainv_game, str(ainv_game.stats.score))
        highscore_text_font = self.font
        self.highscore_text_img = highscore_text_font.render("NEW HIGHSCORE!", True,
                                            self.settings.highscore_text_colour)
        self.highscore_text_rect = self.highscore_text_img.get_rect()
        
        self.last_blink = pygame.time.get_ticks()
        self.position()
        
    def position(self):
        """
        Positions only the score text
        """
        self.sb_rect.midtop = self.screen_rect.midtop
        self.sb_rect.y += 10
        
    def new_highscore(self):
        """
        Displays the message that the user has reached a new highscore
        """
        self.screen.blit(self.highscore_text_img, self.highscore_text_rect)
        
    def display_highscore(self):
        """
        Displays the users current highscore at the start of the game
        """
        highscore_font = pygame.font.SysFont(self.settings.highscore_style,
                                             self.settings.highscore_size)
        self.highscore_img = highscore_font.render(
            "Highscore: " + str(self.stats.highscore), True,
            self.settings.highscore_colour)
        
        self.highscore_rect = self.highscore_img.get_rect()
        self.highscore_rect.center = self.screen_rect.center
        self.highscore_rect.y += 200
        
        self.screen.blit(self.highscore_img, self.highscore_rect)
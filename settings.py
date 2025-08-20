class Settings: 
    """
    Stores all game settings
    """
    
    def __init__(self):
        """
        Initializes static game settings
        """
        
        # play screen settings:
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230, 230, 230)
        
        # home screen settings:
        self.hs_colour = (0, 0, 25)
        self.hs_text_colour = (255, 255, 255)
        self.hs_text_style = None
        self.hs_text_size = 140
        self.hs_text = "Alien Invasion"
        
        # textbox settings:
        self.tb_width = 250
        self.tb_height = 56
        self.tb_font_style = None
        self.tb_font_size = 36
        self.tb_bg_colour = (255, 255, 255)
        self.empty_text = "Enter Username"
        self.empty_text_colour = (180, 180, 180)
        self.user_text_colour = (0, 0, 0)
        
        # textbox blinker settings:
        self.blinker_width = 3
        self.blinker_height = 30
        self.blinker_colour = (0, 0, 0)
        self.blink_duration = 450
        
        # textbox error settings:
        self.error_height = 45
        self.error_font_style = None
        self.error_font_size = 30
        self.error_colour = (255, 0, 0)
        self.error_text_colour = (255, 255, 255)
        
        
        # ship settings:
        self.ship_lifes = 3
        
        # bullet settings:
        self.bullet_width = 3
        self.bullet_height = 8
        self.bullet_colour = (60, 60, 60)
        self.bullets_allowed = 3
        
        # alien settings:
        self.alien_drop_speed = 50
        
        # play button settings:
        self.play_width = 150
        self.play_height = 64
        self.play_x = 0
        self.play_y = 0
        self.play_colour = (50, 50, 50)
        self.play_text_colour = (255, 255, 255)
        self.play_text_style = None
        self.play_text_size = 48
        self.start_text = "Play"
        
        # login buttons settings:
        self.login_height = 40
        self.login_style = None
        self.login_size = 32
        self.login_colour = (0, 0, 255)
        self.login_text_colour = (255, 255, 255)
        self.sign_in_x = -57
        self.sign_up_x = 49
        self.login_y = 167
        self.sign_in_text = "Login"
        self.sign_up_text = "Sign up"
        
        # scoreboard settings:
        self.sb_colour = (30, 30, 30)
        self.sb_size = 48
        self.sb_style = None
        self.lvl_points = 1000
        
        self.highscore_text_colour = (0, 200, 0)
        self.highscore_text_duration = 2000
        self.highscore_colour = (0, 0, 0)
        self.highscore_style = None
        self.highscore_size = 100
        
        # game speed up
        self.speedup_scale = 1.1
        self.current_speed = self.speedup_scale
        
        self.init_dynamic_settings()
        
    def init_dynamic_settings(self):
        # ship settings:
        self.ship_speed = 3.0
        
        # bullet settings:
        self.bullet_speed = 2.5
        
        # alien settings:
        self.alien_speed = 1.0
        # direction 1 = right; direction -1 = left
        self.fleet_dir = 1
        
        # score settings:
        self.alien_points = 50
        
    def increase_speed(self):
        """
        Increases the speed of several settings as game progresses
        """
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points *= self.speedup_scale
        self.current_speed *= self.speedup_scale

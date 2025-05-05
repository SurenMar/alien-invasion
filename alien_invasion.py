import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats 
from play_button import PlayButton
from scores import LevelCounter, Score
from ship_lifes import ShipLifes
from textbox import Textbox, TextboxError
from home_screen import HomeScreen
from login_buttons import LoginButton

import errors
import database_tools as db_tools


class AlienInvasion:
    """
    Overall class to manage game assets and behaviours
    """
    
    def __init__(self):
        """
        Initializes the game and creates resources
        """
        
        pygame.init()
        self.settings = Settings()
        self._create_screen()
        
        self.clock = pygame.time.Clock()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stats = GameStats(self)
        self.ship_lifes = pygame.sprite.Group()
        
        pygame.display.set_caption("Alien Invasion")
        self.play_button = PlayButton(self, "Play")
        self.game_active = False
        
        self.ship = Ship(self)
        self._create_fleet()
        
        self.lvl_counter = LevelCounter(self, "Level: " + str(self.stats.level))
        self.score = Score(self)
        self.highscore_active = False
        self.highscore_reached = False
        
        self.textbox = Textbox(self)
        # holds user inputted username
        self.user_text = ""
        self.tb_active = False # textbox flag
        
        # states the current eror to be displayed
        self.current_error = None
        # dictionary that keeps track of all possible errors
        self.errors_dict = {
            "no_username": TextboxError(self, errors.NO_USERNAME),
            "username_taken": TextboxError(self, errors.USERNAME_TAKEN),
            "invalid_username": TextboxError(self, errors.INVALID_USERNAME)
        }
        
        self.home_screen = HomeScreen(self)
        self.hs_active = True # home screen flag
        self.gs_active = False # game screen flag
        
        self.sign_in = LoginButton(self, self.settings.sign_in_text)
        self.sign_up = LoginButton(self, self.settings.sign_up_text)
        
    def _create_screen(self):
        """
        Creates scaled screen for different devices
        """
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        
    def run_game(self):
        """
        Start main loop for the game
        """
        while True:
            
            if self.tb_active:
                # runs while textbox is clicked
                self._update_home_screen()
                self._check_textbox_events()
                self.textbox.prep_user_text(self.user_text)
                self.textbox.display_blinker()
            else:
                self._check_events()
                
                if self.hs_active == True:
                    # runs while user is in the home screen
                    self._update_home_screen()
                
                    if self.user_text == "":
                        self.textbox.empty_text()
                    else:
                        self.textbox.prep_user_text(self.user_text)
                else:
                    # runs while user is in the game screen
                    if self.game_active == True:
                        self._check_life_lost()
                        self.ship.update()
                        self._update_bullets()
                        self._update_aliens()
                    self._update_screen()
            
            # displays an error if any
            if not self.current_error == None:
                self.errors_dict[self.current_error].display_error()
                
            pygame.display.flip()
            self.clock.tick(60)
            
    def _check_events(self):
        # checks for a quit event (action) performed by user via
        #   looping through the list returned by pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._update_highscore
                exit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_textbox(mouse_pos)
                self._check_sign_in(mouse_pos)
                self._check_sign_up(mouse_pos)
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)  
        
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
                self._fire_bullet()
        elif event.key == pygame.K_q:
            self._update_highscore()
            exit_game()
        elif event.key == pygame.K_p and not self.hs_active:
            self._start_game()
            
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _check_textbox(self, mouse_pos):
        """
        Allow user to enter text if they click the textbox
        """
        button_clicked = self.textbox.rect.collidepoint(mouse_pos)
        if button_clicked and self.hs_active:
            self.tb_active = True
            
    def _check_textbox_events(self):
        """
        Recieve user input from textbox (username)
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._update_highscore()
                exit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not self.textbox.rect.collidepoint(mouse_pos):
                    self.tb_active = False
                    self._check_sign_in(mouse_pos)
                    self._check_sign_up(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isprintable() and not self._check_maxlen() \
                    and event.unicode != ' ':
                    self.user_text += event.unicode
                    self.current_error = None
                elif event.key == pygame.K_BACKSPACE and \
                    len(self.user_text) > 0:
                    self.user_text = (self.user_text)[:-1]
                    self.current_error = None
                       
    def _textbox_cursor(self):
        """
        Changes cursor to Ibeam if user hovers over textbox
        """
        if pygame.mouse.get_cursor != pygame.SYSTEM_CURSOR_IBEAM and \
            self.textbox.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                    
    def _check_maxlen(self):
        """
        Checks whether the user will write beyong the textbox
        """
        if self.textbox.text_rect.width > self.settings.tb_width - 30:
            return True
        else:
            return False
                
    def _check_play_button(self, mouse_pos):
        """
        Start game if player clicks 'Play'
        """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active and not self.hs_active:
            self._start_game()
            
    def _check_sign_up(self, mouse_pos):
        """
        Responds accordingly if user clicks 'Sign up' button
        """
        button_clicked = self.sign_up.rect.collidepoint(mouse_pos)
        if button_clicked and self.hs_active:
            self._user_enter(self.settings.sign_up_text)
            
    def _check_sign_in(self, mouse_pos):
        """
        Responds accordingly if user clicks 'Sign in' button
        """
        button_clicked = self.sign_in.rect.collidepoint(mouse_pos)
        if button_clicked and self.hs_active:
            self._user_enter(self.settings.sign_in_text)    
            
    def _login_button_cursor(self):
        """
        Changes cursor to a hand if user hovers over either login button
        """
        if pygame.mouse.get_cursor != pygame.SYSTEM_CURSOR_HAND and \
            self.sign_in.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif pygame.mouse.get_cursor != pygame.SYSTEM_CURSOR_HAND and \
            self.sign_up.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
    def _user_enter(self, button):
        """
        Performs all actions needed to be performed once user hits either login button
        """
        if len(self.user_text) == 0:
            self.current_error = "no_username"
        elif button == self.settings.sign_up_text and \
            db_tools.user_exists(self.user_text):
            self.current_error = "username_taken"
        elif button == self.settings.sign_in_text and \
            not db_tools.user_exists(self.user_text):
            self.current_error = "invalid_username"
        else:
            self.current_error = None
            self.tb_active = False
            self.hs_active = False
            self.gs_active = True
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
            if button == self.settings.sign_up_text:
                db_tools.add_user(self.user_text)
            self.stats.highscore = db_tools.get_highscore(self.user_text)
        
    def _update_home_screen(self):
        """
        Updates home screen every frame
        """
        self.home_screen.fill_home_screen()
        self.sign_in.display_button()
        self.sign_up.display_button()
        self._login_button_cursor()
        self._textbox_cursor()
    
    def _start_game(self):
        self.game_active = True
        self.gs_active = False
        self.highscore_reached = False
        self.bullets.empty()
        self.stats.reset_stats()
        self.lvl_counter.prep_text("Level: " + str(self.stats.level))
        self.lvl_counter.position()
        self.settings.init_dynamic_settings()
        pygame.mouse.set_visible(False)
        self._create_lifes()
    
    def _update_screen(self):
        """
        Updates game screen every frame
        """
        self.screen.fill(self.settings.bg_colour)
        self.ship.blitme()
        
        # draw every bullet in the bullets group
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
            
        # draw every alien in aliens group
        self.aliens.draw(self.screen)
        
        self._check_highscore()
        self._update_scores()
        self.ship_lifes.draw(self.screen)
        
        if self.gs_active:
            self.score.display_highscore()
        
        if not self.game_active:
            # Changes cursor to a hand if user hovers over 'Play' button
            self.play_button.draw_button()
            if pygame.mouse.get_cursor != pygame.SYSTEM_CURSOR_HAND and \
                self.play_button.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    def _fire_bullet(self):
        """
        Creates new bullet and adds to group to be fired
        """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    def _update_bullets(self):
        """
        Updates and manages the bullets fired
        """
        self.bullets.update()
        
        # Gets rid of dissapeared bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                
        self._check_bullet_alien_collisions()
                
    def _create_alien(self, x_posn, y_posn):
        """
        Create alien at the given x position
        """
        new_alien = Alien(self)
        new_alien.x = x_posn
        new_alien.rect.x = x_posn
        new_alien.rect.y = y_posn
        self.aliens.add(new_alien)
                
    def _create_fleet(self):
        """
        Creates fleet of aliens that fill the screen
        """
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        
        screen_width = self.settings.screen_width
        screen_height = self.settings.screen_height
        
        width_adjustment = alien_width / 2
        
        current_x = alien_width + width_adjustment
        current_y = alien_height
        
        while current_y < screen_height - 5 * alien_height:
            while current_x < screen_width - 2 * alien_width:
                # add alien to aliens group and position correspondingly
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # reset x position
            current_x = alien_width + width_adjustment
            current_y += 2 * alien_height
            
    def _update_aliens(self):
        """
        Updates the current alien fleet
        """
        self._check_fleet_edges()
        self.aliens.update()
        
    def _check_fleet_edges(self):
        """
        Check if an alien has reached the edge
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_dir()
                break
            
    def _change_fleet_dir(self):
        """
        Drop entire fleet and change direction
        """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed
        self.settings.fleet_dir *= -1
        
    def _check_bullet_alien_collisions(self):
        """
        Checks collisions, increases the points if needed, and
        if there are no more aliens left in the round
        """
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        num_pairs = len(collisions)
        self.stats.score += num_pairs * self.settings.alien_points
        
        # reset fleet and active bullets
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            
            self.stats.level += 1
            self.lvl_counter.prep_text("Level: " + str(self.stats.level))
            self.lvl_counter.position()
            self.stats.score += self.settings.lvl_points 
        
    def _ship_hit(self):
        """
        Decreases lives and checks if the user has lost all lives
        """
        self.stats.ships_left -= 1
        if self.stats.ships_left == 0:
            self.game_active = False
            self.gs_active = True
            if self.stats.highscore < self.stats.score:
                self.stats.highscore = self.stats.score
                db_tools.update_highscore(self.user_text, self.stats.highscore)
            pygame.mouse.set_visible(True)
        
        life = list(self.ship_lifes)[-1]
        self.ship_lifes.remove(life)
        
        # remove any active bullets and aliens
        self.bullets.empty()
        self.aliens.empty()
        
        # reset screen
        self._create_fleet()
        self.ship.centre_ship()
        
        # pause game
        sleep(0.7)
    
    def _check_alien_bottom(self):
        """
        Checks if an alien has reached the bottom of the screen
        """
        for alien in self.aliens.sprites():
            if alien.rect.bottom > self.screen_rect.bottom - alien.rect.width:
                self._ship_hit()
                break
        
    def _check_life_lost(self):
        """
        Checks whether the ship was hit, or alien reached bottom
        """
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_alien_bottom()
        
    def _update_scores(self):
        """
        Updates the score and level counts at the top of the screen
        """
        self.lvl_counter.display_text()
        
        if self.highscore_active:
            self._flash_highscore()
        else:
            # runtime score updates
            self.score.prep_text(str(int(self.stats.score)))
            self.score.position()
            self.score.display_text()
            
    def _update_highscore(self):
        if self.stats.highscore < self.stats.score:
            self.stats.highscore = self.stats.score
            db_tools.update_highscore(self.user_text, self.stats.highscore)
            
    def _check_highscore(self):
        """
        Checks if the user has reached their highscore
        """
        if not self.highscore_reached and \
           self.stats.highscore < self.stats.score and \
           self.stats.highscore != 0:
            self.highscore_active = True
            self.highscore_reached = True
            self.score.last_blink = pygame.time.get_ticks()
        
    def _flash_highscore(self):
        """
        Flashes 'NEW HIGHSCORE!' if user surpasses their highscore
        """
        current_time = pygame.time.get_ticks()
        
        if current_time - self.score.last_blink >= \
        self.settings.highscore_text_duration:
            self.highscore_active = False
        elif current_time - self.score.last_blink >= 0:
            self.score.highscore_text_rect.center = self.score.sb_rect.center
            self.score.new_highscore()
        
    def _create_lifes(self):
        """
        Creates a new ship which represents a life
        """
        for life in range(self.settings.ship_lifes):
            new_life = ShipLifes(self)
            new_life.position_life(life)
            self.ship_lifes.add(new_life)
            
    
def exit_game():
    """
    Exits game by first updating the database in case of new scores and players
    """
    db_tools.upload_user_data()
    sys.exit()
            
            
# checks if this file is being run directly
if __name__ == '__main__':
    flag = False
    if flag:
        db_tools.database_dict.clear()
    # makes AlienInvasion instance and runs game
    ainv = AlienInvasion()
    ainv.run_game()
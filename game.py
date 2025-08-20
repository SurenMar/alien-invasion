"""A file solely for the AI to train"""

import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from ship_lifes import ShipLifes

from alien import ALIENS_PER_ROW

class AlienInvasionAI:
    """
    Overall class to manage game assets and behaviours
    """
    
    def __init__(self):
        """
        Initializes the game and creates resources
        """
        
        pygame.init()
        self.settings = Settings()
        
        self.clock = pygame.time.Clock()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stats = GameStats(self)
        self.ship_lifes = pygame.sprite.Group()
        self.lowest_alien = None
        
        self.ship = Ship(self)
        self._create_fleet()

        self.reset()

    def reset(self):
        self.lifes_remaining = 3
        self.frame_iteration = 0

    def play_step(self, action):
        reward = 0
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Move
        self._move(action)
        self._update_state()

        # Check if life is lost
        if self._check_life_lost():
            if self.stats.ships_left == 0:
                # Big punishment
                pass
            else:
                # Big punishment
                pass
        # Check if alien is hit
        elif self._check_bullet_alien_collisions():
            if self._check_lvl_cleared():
                # Big reward
                pass
            elif self._check_row_cleared():
                # Medium reward
                pass
            else:
                # Small reward
                pass
        elif self._check_bullet_missed():
            # Small punishment
            pass

    def _move(self, action):
        if action[0]:
            self.ship.moving_left = False
            self.ship.moving_right = True
        elif action[1]:
            self.ship.moving_right = False
            self.ship.moving_left = True
        elif action[2]:
            self._fire_bullet()

    def _update_state(self):
        self.ship.update()
        self.bullets.update()
        self._update_aliens()
    
    def _start_game(self):
        self.bullets.empty()
        self.stats.reset_stats()
        self.settings.init_dynamic_settings()
        self._create_lifes()
        
    def _fire_bullet(self):
        """
        Creates new bullet and adds to group to be fired
        """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _check_bullet_missed(self):
        return_val = False
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                return_val = True
        return return_val
                
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

    def find_alien_coords(self):
        """
        Returns a list of coords for each column of aliens
        """
        alien_coords = []
        for i, alien in enumerate(self.aliens.sprites()):
            if i > ALIENS_PER_ROW:
                break
            alien_coords.append(alien.rect.x)
        return alien_coords
    
    def _find_lowest_alien(self):
        """
        Return the y_coord of the lowest alien on screen
        """
        return max(self.aliens.sprites(), key=lambda alien: alien.rect.y)

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
        return True if num_pairs > 0 else False
    
    def _check_row_cleared(self):
        new_lowest_alien = self._find_lowest_alien()
        if new_lowest_alien < self.lowest_alien:
            self.lowest_alien = new_lowest_alien
            return True
        return False

    def _check_lvl_cleared(self):
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            
            self.stats.level += 1
            self.stats.score += self.settings.lvl_points
            return True
        return False
        
    def _ship_hit(self):
        """
        Decreases lives and reset positions
        """
        self.stats.ships_left -= 1
        
        life = list(self.ship_lifes)[-1]
        self.ship_lifes.remove(life)
        
        # remove any active bullets and aliens
        self.bullets.empty()
        self.aliens.empty()
        
        # reset screen
        self._create_fleet()
        
    def _check_life_lost(self):
        """
        Checks if an alien has reached the bottom of the screen
        """
        for alien in self.aliens.sprites():
            if alien.rect.bottom > self.screen_rect.bottom - alien.rect.width:
                self._ship_hit()
                return True
        return False
        
    def _create_lifes(self):
        """
        Creates a new ship which represents a life
        """
        for life in range(self.settings.ship_lifes):
            new_life = ShipLifes(self)
            new_life.position_life(life)
            self.ship_lifes.add(new_life)
    
    def _update_highscore(self):
        if self.stats.highscore < self.stats.score:
            self.stats.highscore = self.stats.score
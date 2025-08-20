"""A file solely for the AI to train"""

import pygame
import numpy as np

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from ship_lifes import ShipLifes

from alien import ALIENS_PER_ROW
MAX_LEVEL = 50

pygame.init()

class AlienInvasionAI:
    """
    Overall class to manage game assets and behaviours
    """
    
    def __init__(self):
        """
        Initializes the game and creates resources
        """
        self.settings = Settings()
        self.screen = pygame.Surface(
            (self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stats = GameStats(self)
        self.ship_lifes = pygame.sprite.Group()
        self.ship = Ship(self)
        self.reset()

    def reset(self):
        """Reset the game for a new episode."""
        self.stats.reset_stats()
        self.frame_iteration = 0
        self.settings.init_dynamic_settings()

        # Reset ship lives and position
        self.ship_lifes.empty()
        self._create_lifes()
        self.ship.centre_ship()

        # Clear bullets and aliens
        self.bullets.empty()
        self.aliens.empty()

        # Recreate alien fleet
        self._create_fleet()
        self.lowest_alien = self._find_lowest_alien()

        # Return the initial game state for RL
        return self.get_state()

    def get_state(self):
        # Compute game speeds
        current_speed = self.settings.current_speed
        max_speed = self.settings.speedup_scale ** MAX_LEVEL

        # Get alien coords
        alien_coords = [alien_coord / self.settings.screen_width \
            for alien_coord in self.find_alien_coords()]
        alien_coords += [0.0] * (ALIENS_PER_ROW - len(alien_coords))

        state = [
            # Current game speed
            np.log(current_speed) / np.log(max_speed),

            # Number of bullets on screen
            len(self.bullets) / self.settings.bullets_allowed,

            # Ship position
            self.ship.x / self.settings.screen_width,

            # Alien positions (x values)
            *alien_coords,

            # Lowest alien position (y value)
            self.lowest_alien / self.settings.screen_width,

            # Number of lifes remaining
            self.stats.ships_left / self.settings.ship_lifes
        ]
        return np.array(state, dtype=float)

    def play_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Move
        self._move(action)
        self._update_state()

        reward = 0
        game_over = False
        # Check if life is lost
        if self._check_life_lost():
            if self.stats.ships_left == 0:
                # Very big punishment
                reward = -20.0
                game_over = True
            else:
                # Medium punishment
                reward = -5.0
        # Check if alien is hit
        elif self._check_bullet_alien_collisions():
            if self._check_lvl_cleared():
                # Big reward
                reward = 10.0
            elif self._check_row_cleared():
                # Medium reward
                reward = 3.0
            else:
                # Small reward
                reward = 1.0
        elif self._check_bullet_missed():
            # Very small punishment
            reward = -0.2
        
        return reward, game_over, self.stats.score

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
        return [alien.rect.x for alien in self.aliens.sprites()[:ALIENS_PER_ROW]]
    
    def _find_lowest_alien(self):
        """
        Return the y_coord of the lowest alien on screen
        """
        return max(alien.rect.y for alien in self.aliens.sprites())

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
    
    # TODO
    def _update_highscore(self):
        if self.stats.highscore < self.stats.score:
            self.stats.highscore = self.stats.score
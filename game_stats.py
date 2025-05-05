# A file to manage anything about game stats

class GameStats:
    """
    Track game stats
    """
    
    def __init__(self, ainv_game):
        self.settings = ainv_game.settings
        self.highscore = 0
        self.reset_stats()
        
    def reset_stats(self):
        """
        Resets current game stats
        """
        self.ships_left = self.settings.ship_lifes
        self.level = 0
        self.score = 0
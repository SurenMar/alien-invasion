"""A file for the AI agent"""

import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction, Point
# from model import Linear_QNet, QTrainer
# from helper import plot

MAX_LEVEL = 50
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        # self.model = Linear_QNet(11, 256, 3)
        # self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, ainv_game):

        # Compute game speeds
        current_speed = ainv_game.settings.current_speed
        max_speed = ainv_game.settings.speedup_scale ** MAX_LEVEL

        state = [
            # Current game speed
            np.log(current_speed) / np.log(max_speed),

            # Number of bullets on screen
            len(ainv_game.bullets) / ainv_game.settings.bullets_allowed,

            # Ship position
            ainv_game.ship.x / ainv_game.scaled_width,

            # Alien positions (x values)
            ainv_game.alien_x_coords() / ainv_game.scaled_width,

            # Lowest alien position (y value)
            ainv_game.lowest_alien() / ainv_game.scaled_height,
        ]
        return np.array(state, dtype=float)
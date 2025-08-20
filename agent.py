"""A file for the AI agent"""

import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction, Point
# from model import Linear_QNet, QTrainer
# from helper import plot

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
        state = [
            # Current game speed
            ainv_game.settings.current_speed,

            # Number of bullets on screen
            len(ainv_game.bullets),

            # Ship position
            ainv_game.ship.x,

            # Alien positions (x values)
            ainv_game.alien_coords(),
        ]
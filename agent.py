"""A file for the AI agent"""

import torch
import random
import numpy as np
from collections import deque
from game import AlienInvasionAI
from model import Linear_QNet, QTrainer
from helper import plot

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
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

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

            # Number of lifes remaining
            ainv_game.stats.ships_left / ainv_game.settings.ship_lifes
        ]
        return np.array(state, dtype=float)
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]    # Move right, move left, or fire bullet
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


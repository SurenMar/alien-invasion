"""A file for viewing the AI play"""

import torch
import numpy as np
from agent import Agent
from game import AlienInvasionAI

def play():
    # Load the game
    game = AlienInvasionAI(render=True)
    agent = Agent()

    # Load trained model
    agent.model.load_state_dict(torch.load("model/model.pth"))
    agent.model.eval()  # set to evaluation mode

    done = False
    state = game.reset()

    while not done:
        # Get action from model
        state_tensor = torch.tensor(np.array(state), dtype=torch.float32)
        prediction = agent.model(state_tensor)
        action_idx = torch.argmax(prediction).item()

        # Apply action to game
        final_action = [0, 0, 0]
        final_action[action_idx] = 1
        reward, done, score = game.play_step(final_action)

        # Update state
        state = game.get_state()

        # Render on screen so you can watch it
        game.render()

    print("Final score:", score)

if __name__ == "__main__":
    play()

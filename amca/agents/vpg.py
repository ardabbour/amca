# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
    Amca: The RL-Based Backgammon Agent
    https://github.com/ardabbour/amca/

    Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu
    Cognitive Robotics Laboratory
    Faculty of Engineering and Natural Sciences
    Sabanci University

    The Vanilla Policy Gradient agent is an on-policy algorithm that attempts to
    maximize the probabilities of actions that yield higher returns, and
    minimize probabilities that yield lower returns.
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras

class VanillaPolicyGradientAgent:
    """An on-policy agents"""

    def __init__(self, model, observation_space, action_space):
        self.__parameters = model
        self.__observation_space = observation_space
        self.__action_space = action_space

    def act(self, observation, valid_actions):
        """Returns an action depending on the observation, reward, and whether
        the episode is finished or not using a policy."""

        sampled_action = self.__action_space.sample()
        while sampled_action not in valid_actions:
            sampled_action = self.__action_space.sample()

        return sampled_action


# def learn_from_random_agent():
#     """"""

#     episodes = 100
#     value_table = [0, 0, 0, 0, 0, 0, 0, 0, 0]

#     for i in range(episodes):
#         eps = 0.1
#         env = Env(random_play=1)
#         total_reward = 0

#         done = 0
#         agent_value = "X"   # it must be X for random play
#         state = env.state
#         old_a = [0, 0]
#         alfa = 0.99

#         while not done:
#             empty_spaces = []
#             values_of_empty_spaces = []

#             for i in range(3):
#                 for j in range(3):
#                     if state[i][j] == 0:
#                         empty_spaces.append([i, j])
#                         values_of_empty_spaces.append(value_table[i * 3 + j])

#             if np.random.random() < eps or np.sum(value_table) == 0:
#                 a = empty_spaces[random.choice(
#                     list(enumerate(values_of_empty_spaces)))[0]]
#             else:
#                 # select the action with largest q value in state s
#                 a = empty_spaces[np.argmax(values_of_empty_spaces)]

#             new_s, reward, done, winner = env.step(a, agent_value)
#             total_reward = reward + total_reward

#             if (state != [[0, 0, 0], [0, 0, 0], [0, 0, 0]]):
#                 value_table[old_a[0] * 3+old_a[1]] = value_table[old_a[0] * 3 +
#                                                                  old_a[1]] + alfa*(reward - value_table[old_a[0] * 3 + old_a[1]])
#             else:
#                 value_table[a[0] * 3 + a[1]] = alfa * reward

#             old_a = a
#             state = new_s

#             if(done == 1):
#                 print("Winner is  :" + str(winner))
#                 print(value_table)

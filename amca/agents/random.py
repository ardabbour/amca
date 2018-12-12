# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
    Amca: The RL-Based Backgammon Agent
    https://github.com/ardabbour/amca/

    Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu
    Cognitive Robotics Laboratory
    Faculty of Engineering and Natural Sciences
    Sabanci University

    The Random agent takes an action randomly.
"""

import numpy as np


class RandomAgent:
    def __init__(self):
        self.__action_history = []

    def act(self, valid_actions):
        """Returns a random action from a list of valid actions."""

        action = np.random.choice(valid_actions)
        self.__action_history.append(action)

        return action

    def get_action_history(self):
        """Returns the action history of the agent."""

        return self.__action_history

# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
    Amca: The RL-Based Backgammon Agent
    https://github.com/ardabbour/amca/

    Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu
    Cognitive Robotics Laboratory
    Faculty of Engineering and Natural Sciences
    Sabanci University

    The Simple agent uses a basic DNN model to take an action. Can be trained.
"""


class Agent:
    def __init__(self, policy):
        self.__policy = policy
        self.__action_history = []

    def act(self, observation, valid_actions):
        """Returns the action that is closest to the predicted output.
        Might work with continuous algorithms."""

        prediction = self.__policy.predict(observation, valid_actions)

        return min(valid_actions, key=lambda x: abs(x-prediction))

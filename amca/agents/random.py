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

import random

class RandomAgent:
    def __init__(self, action_space):
        self.__action_space = action_space

    def make_decision(self, _):
        """Returns a random action from a list of valid actions."""

        return self.__action_space.sample()


class RandomSarsaAgent:
    def __init__(self, name):

        self.name = name

    def chooseAction(self, _, actions):
        if len(actions) < 1:
            actions = [("Nomove", 0, 0)]
            return ("Nomove", 0, 0), 0

        i = random.choice(range(0, len(actions)))   # q.index(maxQ)

        action = actions[i]
        return action, i

    def chooseAction2(self, actions):
        action = random.choice(actions)
        return action
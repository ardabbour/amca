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


class RandomAgent:
    def __init__(self, action_space):
        self.__action_space = action_space

    def make_decision(self, _):
        """Returns a random action from a list of valid actions."""

        return self.__action_space.sample()

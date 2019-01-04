# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
    Amca: The RL-Based Backgammon Agent
    https://github.com/ardabbour/amca/

    Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu
    Cognitive Robotics Laboratory
    Faculty of Engineering and Natural Sciences
    Sabanci University

    All elements related to the player's functionality are defined here.
"""

import random


class Player:
    """A player can be a human or an AI. If it is a human, the human will have
    to throw the dice and get a list of possible moves from the game."""

    def __init__(self, name, is_human=True, policy=None):
        """Define a new player object."""

        self.__name = name

        self.__is_human = is_human
        if not is_human:
            assert policy
        self.__policy = policy

    def get_name(self):
        return self.__name

    def is_human(self):
        return self.__is_human

    def get_policy(self):
        return self.__policy

    def set_policy(self, policy):
        self.__policy = policy

    def make_decision(self, moves):
        """Returns a move based on the agent's policy or the human's input."""

        if not self.__is_human:
            return self.__policy(moves)

        print("You have the following possible moves.")

        for index, move in enumerate(moves):
            print('index: {}'.format(index), 'move: {}'.format(move))

        desired_move = input("Enter the index of the move desired.")

        return moves[desired_move]

#!/usr/bin/env python3
"""
    Amca: The RL-Based Backgammon Agent
    https://github.com/ardabbour/amca/

    Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu
    Cognitive Robotics Laboratory
    Faculty of Engineering and Natural Sciences
    Sabanci University

    This file contains the classes required to play backgammon.
"""

from .player import Player
from .board import Board

class Game():
    """Defines a backgammon game object."""

    def __init__(self, w_player, b_player):
        self.__w_player = w_player
        self.__b_player = b_player
        self.__board = Board()

    def get_player(self, color):
        """Returns the winning player based on the color."""

        assert color == 'w' or 'b'

        return self.__w_player if color == 'w' else self.__b_player

    # TODO
    # def get_actions(self, roll):
        # """Given a tuple of dice rolls, return the set of possible moves."""

    def is_over(self, board):
        """Returns a tuple of which the first element is a boolean of the game
        being over or not and the second element is the winner."""

        i = 0
        for color in ['w', 'b']:
            for point in board:
                checkers = point.get_checkers()
                if checkers[0] == color:
                    i += point.checkers[1]
            if i < 1:
                return (True, self.get_player(color))

        return (False, None)

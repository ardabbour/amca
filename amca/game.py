# -*- coding: utf-8 -*-
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


class Game:
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
    def get_actions(self, player, roll):
        """Given a tuple of dice rolls, return the set of possible moves.

        1) Move: move forward from one point to another, as long as the target
                 point is empty or having the same color as the source point.
        2) Hit: To move to a point occupied by an opposing blot and put the blot
                on the bar.
        3) Reenter: To move a checker from the bar to an open point in the
                    opponent's home board according to a roll of the dice. When
                    a player has a checker on the bar, this is his only legal
                    move.
        4) Bear off: To remove a checker from the board according to a roll of
                     the dice after all of your checkers have been brought into
                     your home board."""

        w_indices = []
        b_indices = []
        empty_indices = []
        for index, point in enumerate(self.__board):
            if point.get_color() == 'w':
                w_indices.append(index)
            if point.get_color() == 'b':
                b_indices.append(index)
            else:
                empty_indices.append(index)

        w_home_board = max(w_indices) < 6
        b_home_board = min(b_indices) < 18

        actions = []
        if player == self.__w_player:
            for index in w_indices:
                if index + roll in w_indices + empty_indices:
                    actions.append(('move', index, index + roll))
                if index + roll in b_indices:
                    if self.__board[b_indices[index + roll]].get_count() < 2:
                        actions.append(('hit', index, index + roll))

        return actions

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


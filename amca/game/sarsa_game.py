# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
    Amca: The RL-Based Backgammon Agent
    https://github.com/ardabbour/amca/

    Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu
    Cognitive Robotics Laboratory
    Faculty of Engineering and Natural Sciences
    Sabanci University

    This script contains the classes required to play backgammon.
"""

import random

from amca.game import Board


class SarsaGame:
    """Defines a backgammon game object."""

    def __init__(self, w_player, b_player):
        self.__w_player = w_player
        self.__b_player = b_player
        self.__gameboard = Board()
        self.__dice = []

        self.__w_hitted = 0
        self.__b_hitted = 0
        self.__w_bourne_off = 0
        self.__b_bourne_off = 0
        self.__w_canbearoff = False
        self.__b_canbearoff = False

    def get_player(self, color):
        """Returns the winning player based on the color."""

        assert color == 'w' or 'b'

        return self.__w_player if color == 'w' else self.__b_player

    def roll_dice(self):
        self.__dice = [random.randint(1, 6), random.randint(1, 6)]

    def get_dice(self, diceid):
        return self.__dice[diceid]

    def letterx(self, playerid, x):
        white_indices = ["0", "1", "2", "3", "4", "5", "6",
                         "7", "8", "9", "R", "U", "T", "V", "W", "Y", "Z"]
        black_indices = ["0", "A", "B", "C", "D", "E", "F",
                         "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q"]
        if playerid == "w":
            a = white_indices[x]
        elif playerid == "b":
            a = black_indices[x]
        return a

    def get_state(self):
        statevec = []

        for point in self.__gameboard.get_board():
            if point.get_color() == 'w':
                statevec.append(point.get_count())
            if point.get_color() == 'b':
                statevec.append(16+point.get_count())
            else:
                statevec.append(0)
        return statevec

    def get_state3(self, adice):
        statestr = str(adice)

        for point in self.__gameboard.get_board():
            if point.get_color() == 'w':
                statestr += self.letterx("w", point.get_count())
            if point.get_color() == 'b':
                statestr += self.letterx("b", point.get_count())
            else:
                statestr += "0"
        return statestr

    def update_board(self, player, action):
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

        if player == self.__w_player:
            if self.__w_hitted > 0:
                if (action[0] == "reenter"):
                    self.__w_hitted = self.__w_hitted - 1
                    (self.__gameboard).update_reenter("w", action[1])
                if (action[0] == "reenter_hit"):
                    self.__w_hitted = self.__w_hitted - 1
                    self.__b_hitted = self.__b_hitted + 1
                    (self.__gameboard).update_reenterhit("w", action[1])
            else:
                if (action[0] == "move"):
                    (self.__gameboard).update_move("w", action[1], action[2])
                if (action[0] == "hit"):
                    self.__b_hitted = self.__b_hitted + 1
                    (self.__gameboard).update_hit("w", action[1], action[2])
                if (action[0] == "bearoff"):
                    (self.__gameboard).update_bearoff("w", action[1])

        if player == self.__b_player:
            if self.__b_hitted > 0:
                if (action[0] == "reenter"):
                    self.__b_hitted = self.__b_hitted - 1
                    (self.__gameboard).update_reenter("b", action[1])
                if (action[0] == "reenter_hit"):
                    self.__w_hitted = self.__w_hitted + 1
                    self.__b_hitted = self.__b_hitted - 1
                    (self.__gameboard).update_reenterhit("b", action[1])
            else:
                if (action[0] == "move"):
                    (self.__gameboard).update_move("b", action[1], action[2])
                if (action[0] == "hit"):
                    self.__w_hitted = self.__w_hitted + 1
                    (self.__gameboard).update_hit("b", action[1], action[2])
                if (action[0] == "bearoff"):
                    (self.__gameboard).update_bearoff("b", action[1])

        self.__w_bourne_off = self.__gameboard.get_bourne_off()['w']
        self.__w_bourne_off = self.__gameboard.get_bourne_off()['b']

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

        points = self.__gameboard.get_board()

        w_indices = []
        b_indices = []
        empty_indices = []
        index = 0
        for point in points:
            if point.get_color() == 'w':
                w_indices.append(index)
            elif point.get_color() == 'b':
                b_indices.append(index)
            else:
                empty_indices.append(index)
            index = index+1

        w_home_board = max(w_indices) < 6
        b_home_board = min(b_indices) > 17
        if w_home_board and (self.__w_hitted == 0):
            self.__w_canbearoff = True
        if b_home_board and (self.__b_hitted == 0):
            self.__b_canbearoff = True

        actions = []
        rewards = []
        if player == self.__w_player:
            if self.__w_hitted > 0:
                if (24-roll) in empty_indices or w_indices:
                    actions.append(('reenter', 24-roll))
                    rewards.append(roll)
                elif ((24-roll) in b_indices) and ((points[24-roll]).get_count() < 2):
                    actions.append(('reenter_hit', 24-roll))
                    rewards.append(24)

                if len(actions) < 1:
                    return [("Nomove", 0, 0)], [0]
                return actions, rewards

            for index in w_indices:
                if (index-roll) in (w_indices + empty_indices):
                    actions.append(('move', index, index - roll))
                    rewards.append(roll)
                if ((index-roll) in b_indices) and ((points[index-roll]).get_count() < 2):
                    actions.append(('hit', index, index - roll))
                    rewards.append(index)
                if (self.__w_canbearoff) and (index < roll):
                    actions.append(('bearoff', index))
                    rewards.append(roll)

        if player == self.__b_player:
            if self.__b_hitted > 0:
                if (roll-1) in empty_indices or b_indices:
                    actions.append(('reenter', roll-1))
                    rewards.append(roll)
                elif ((roll-1) in w_indices) and ((points[roll-1]).get_count() < 2):
                    actions.append(('reenter_hit', roll-1))
                    rewards.append(24)
                return actions, rewards

            for index in b_indices:
                if (index+roll) in (b_indices + empty_indices):
                    actions.append(('move', index, index + roll))
                    rewards.append(roll)
                if ((index+roll) in w_indices) and ((points[index+roll]).get_count() < 2):
                    actions.append(('hit', index, index + roll))
                    rewards.append(24-index)
                if (self.__b_canbearoff) and ((23-index) < roll):
                    actions.append(('bearoff', index))
                    rewards.append(roll)

        if len(actions) < 1:
            return [("Nomove", 0, 0)], [0]
        return actions, rewards

    def is_over(self):
        """Returns a tuple of which the first element is a boolean of the game
        being over or not and the second element is the winner."""

        points = self.__gameboard.get_board()

        for color in ['w', 'b']:
            i = 0
            for point in points:
                checkers = point.get_count()
                if point.get_color() == color:
                    i += checkers
            if i < 1:
                return True

        return False

    def is_over2(self):
        """Returns a tuple of which the first element is a boolean of the game
        being over or not and the second element is the winner."""

        points = self.__gameboard.get_board()
        i = 0
        for color in ['w', 'b']:
            i = 0
            for point in points:
                checkers = point.get_count()
                if point.get_color() == color:
                    i += checkers
            if i < 1:
                return (True, self.get_player(color))

        return (False, None)

    def get_observation(self):
        statevec = []
        statevec.append(self.__dice[0])
        statevec.append(self.__dice[1])
        statevec.append(self.__w_hitted)
        statevec.append(self.__b_hitted)
        statevec.append(self.__w_bourne_off)
        statevec.append(self.__b_bourne_off)

        for point in self.__gameboard.get_board():
            if point.get_color() == 'w':
                statevec.append(1)
                statevec.append(point.get_count())
            elif point.get_color() == 'b':
                statevec.append(2)
                statevec.append(point.get_count())
            else:
                statevec.append(0)
                statevec.append(0)
        return statevec

    def render(self, mode='human'):
        """Represent the board in the terminal. In this representation, x is
        player1 and y is player 2."""

        if mode != 'human':
            return
        state = self.get_observation()
        max_picese_point = max(state)
        state = zip(state[::2], state[1::2])
        state = list(state)
        up_side = list()
        buttom_side = list()
        for i in range(3, int(3+(len(state)-3)/2)):
            buttom_side.append(state[i])
        for i in range(int(3+(len(state)-3)/2), len(state)):
            up_side.append(state[i])
        buttom_side.reverse()
        board = list()
        board.append(
            '  -------------------------------------------------------------- ')
        board.append(
            ' |12  13  14  15   16   17   |    | 18   19   20   21   22   23  | ')
        board.append(
            ' |---------------------------------------------------------------|')

        for i in range(0, max_picese_point):
            point = list()
            for item in up_side:
                if i < item[1]:
                    point.append('w' if item[0] == 1 else 'b')
                else:
                    point.append(' ')
            board.append(
                ' |{}   {}   {}   {}    {}    {}    |    | {}    {}    {}    {}    {}    {}   | '.format(*point))
        board.append(
            '  --------------------------------------------------------------- ')

        for i in range(0, max_picese_point):
            point = list()
            for item in buttom_side:
                if max_picese_point - item[1] <= i:
                    point.append('w' if item[0] == 1 else 'b')
                else:
                    point.append(' ')
            board.append(
                ' |{}   {}   {}    {}    {}    {}    |    | {}    {}    {}    {}    {}    {}  | '.format(*point))
        board.append(
            ' |---------------------------------------------------------------|')
        board.append(
            ' |11  10   9   8    7    6    |    | 5    4    3    2    1    0  | ')
        board.append(
            '  --------------------------------------------------------------- ')
        board.append('Dice 1: {}'.format(state[0][0]))
        board.append('Dice 2: {}'.format(state[0][1]))
        board.append('White hitted: {}'.format(state[1][0]))
        board.append('Black hitted: {}'.format(state[1][1]))
        board.append('white bourne off: {}'.format(state[2][0]))
        board.append('Black bourne off: {}'.format(state[2][1]))

        for line in board:
            print(line)

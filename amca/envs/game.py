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

import random
import copy

import numpy as np
from amca.envs.board import Board


def roll_dice():
    dice = [np.random.randint(1, 6), np.random.randint(1, 6)]
    if dice[0] == dice[1]:
        return [dice[0], ]*4
    return dice


def all_possible_actions():
    actions = []
    sources = list(range(0, 24))
    targets = list(range(0, 24))
    homes = list(range(0, 6)) + list(range(18, 24))

    # 'move's and 'hit's
    for i in sources:
        for j in targets:
            if (j - i) <= 6:
                actions.append(('move', i, j))
                actions.append(('move', j, i))
                actions.append(('hit', i, j))
                actions.append(('hit', j, i))

    # 'reenter's, 'reenter_hit's and 'bearoff's
    for j in homes:
        actions.append(('reenter', j))
        actions.append(('reenter_hit', j))
        actions.append(('bearoff', j))

    return actions


ALL_ACTIONS = all_possible_actions()


class Game:
    """Player 1 is the priveleged player here. Player 2 is the player who is
    the opponent. The opponent can either be a random agent, a human, or a
    policy agent."""

    def __init__(self, player1, player2):
        # Initialize game vars
        self.__gameboard = Board()
        self.__w_hitted = 0
        self.__b_hitted = 0
        self.__w_bourne_off = 0
        self.__b_bourne_off = 0
        self.__w_canbearoff = False
        self.__b_canbearoff = False
        self.__opponent = player2
        self.__dice = []

        # The higher dice roll starts
        w_toss = roll_dice()
        b_toss = roll_dice()
        while sum(w_toss) == sum(b_toss):
            w_toss = roll_dice()
            b_toss = roll_dice()

        self.__dice = roll_dice()
        if sum(w_toss) > sum(b_toss):
            self.__turn = 1
        else:
            self.__turn = 2
            self.opponent_turn()

    def player_turn(self, actionint):
        """Takes an actionint from the Backgammon Environment, converts it to an
        action, processes the result of the action and returns the reward."""

        # Case of playing out of turn

        if self.__turn != 1:
            raise ValueError('Agent playing out of turn!')

        # Case of no valid actions
        valid_actions, their_rewards = self.get_valid_actions()
        if not any(valid_actions):
            self.__turn = 2
            self.opponent_turn()
            reward = 0
            return reward

        action = self.get_action(actionint)

        # Case of choosing valid action
        action_is_valid = False
        for index, action_set in enumerate(valid_actions):
            if action in action_set:
                action_is_valid = True
                self.act(action)
                del self.__dice[index]
                if not self.__dice:
                    self.__turn = 2
                    self.opponent_turn()
                reward = their_rewards[index][action_set.index(action)]
                return reward

        # Case of choosing invalid action
        action = self.get_random_action(valid_actions)
        for index, action_set in enumerate(valid_actions):
            if action in action_set:
                self.act(action)
                del self.__dice[index]
                if not self.__dice:
                    self.__turn = 2
                    self.opponent_turn()
                reward = -10
                return reward

        raise ValueError('Unexpected error occured')

    def opponent_turn(self):
        """Manages the whole turn for the opponent."""

        self.__dice = roll_dice()
        while self.__dice:
            if self.get_done():
                break
            self.play_opponent()
        self.__turn = 1
        self.__dice = roll_dice()

        return

    def play_opponent(self):
        """Plays a single dice of the opponent."""

        # Case of playing out of turn
        if self.__turn != 2:
            raise ValueError('Opponent playing out of turn!')

        # Case of no valid actions
        valid_actions, _ = self.get_valid_actions()
        if not any(valid_actions):
            self.__turn = 1
            self.__dice = []
            return

        actionint = self.__opponent.make_decision(self.get_observation())
        action = self.get_action(actionint)

        # Case of valid action chosen
        action_is_valid = False
        for index, action_set in enumerate(valid_actions):
            if action in action_set:
                action_is_valid = True
                self.act(action)
                del self.__dice[index]
                return

        # Case of invalid action chosen
        action = self.get_random_action(valid_actions)
        for index, action_set in enumerate(valid_actions):
            if action in action_set:
                self.act(action)
                del self.__dice[index]
                return

    def get_action(self, actionint):
        """Returns the action tuple associated with the actionint."""

        return ALL_ACTIONS[actionint]

    def get_valid_actions(self):
        """Returns two NUMPY array of NUMPY arrays as such:

        For actions:
        [
            [Valid action 1, Valid action 2, ...], # Dice 1 valid actions
            [Valid action 1, Valid action 2, ...], # Dice 2 valid actions
            .
            .
        ]
        For rewards:
        [
            [Reward of valid action 1, Reward of valid action 2, ...],
            [Reward of valid action 1, Reward of valid action 2, ...],
            .
            .
        ]
        """
        acts = []
        rews = []
        points = self.__gameboard.get_board()
        for roll in self.__dice:
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
            if self.__turn == 1:
                if self.__w_hitted > 0:
                    if (24-roll) in (empty_indices + w_indices):
                        actions.append(('reenter', 24-roll))
                        rewards.append(roll)
                    elif ((24-roll) in b_indices) and ((points[24-roll]).get_count() < 2):
                        actions.append(('reenter_hit', 24-roll))
                        rewards.append(24)

                else:
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

            if self.__turn == 2:
                if self.__b_hitted > 0:
                    if (roll-1) in (empty_indices + b_indices):
                        actions.append(('reenter', roll-1))
                        rewards.append(roll)
                    elif ((roll-1) in w_indices) and ((points[roll-1]).get_count() < 2):
                        actions.append(('reenter_hit', roll-1))
                        rewards.append(24)

                else:
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

            acts.append(actions)
            rews.append(rewards)

        return acts, rews

    def act(self, action):
        """Takes an action and updates the board as neccessary, including the
        checkers hit and bourne off."""

        if self.__turn == 1:
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

        if self.__turn == 2:
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

    def get_random_action(self, valid_actions):
        first_choice = random.choice(valid_actions)
        while not first_choice:
            first_choice = random.choice(valid_actions)
        return random.choice(first_choice)

    def get_observation(self):
        statevec = []
        if len(self.__dice) < 1:
            statevec.append(0)
            statevec.append(0)
        elif len(self.__dice) < 2:
            statevec.append(self.__dice[0])
            statevec.append(0)
        else:
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

    def print_game(self):
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

    def get_done(self):
        """Returns if the game is over or not."""

        points = self.__gameboard.get_board()
        i = 0
        for color in ['w', 'b']:
            i = 0
            for point in points:
                checkers = point.get_count()
                if point.get_color() == color:
                    i += checkers
            if i < 1:
                return True
        return False

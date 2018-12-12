# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import time

import gym
from gym import error, spaces, utils
from gym.utils import seeding

import numpy as np


def roll_dice():
    """Returns the roll of two die as an ndarray."""

    return np.random.choice([1, 2, 3, 4, 5, 6], size=(2,))


class BackgammonEnv(gym.Env):
    """Defines a Backgammon environment to run the RL algorithm in. It is
    stochastic and fully-observable, with a bounded, discrete domain.

    The action space has the following structure:
        [Action type, Source index/None, Target index/None]

    # -------- For source and target indices, 0 is reserved for None. -------- #

    For example, [0, 3, 7] moves the first player (white) from the 2nd to the
    6th point.
                   --------------------------
                   |   Action   | Encoding  |
                   |------------------------|
                   |  Move      |     0     |
                   |  Hit       |     1     |
                   |  Bear-off  |     2     |
                   |  Enter     |     3     |
                   |  Hit-enter |     4     |
                   --------------------------

    The observation space has the following structure:
        [
            [Empty/White/Black, Number of checkers], # For point 0
            [Empty/White/Black, Number of checkers], # For point 1
                                .
                                .
                                .
            [Empty/White/Black, Number of checkers]  # For point 24
        ]
    For an example, check the initial board setting.
    """

    metadata = {'render.modes': ['human']}

    def __init__(self, player1, player2, higher_starts=True):
        self.action_space = spaces.MultiDiscrete([5, 25, 25])
        self.observation_space = spaces.MultiDiscrete([[3, 16], ]*24)
        self.board = np.array([[2, 2], [0, 0], [0, 0], [0, 0], [0, 0], [1, 5],
                               [0, 0], [1, 3], [0, 0], [0, 0], [0, 0], [2, 5],
                               [1, 5], [0, 0], [0, 0], [0, 0], [2, 3], [0, 0],
                               [2, 5], [0, 0], [0, 0], [0, 0], [0, 0], [1, 2]])

        self.player1 = player1
        self.player2 = player2
        self.higher_starts = higher_starts

        player1_roll = np.sum(roll_dice())
        player2_roll = np.sum(roll_dice())
        while player1_roll == player2_roll:
            player1_roll = np.sum(roll_dice())
            player2_roll = np.sum(roll_dice())

        if self.higher_starts:
            self.turn = 1 if player1_roll > player2_roll else 2
        else:
            self.turn = 1 if player1_roll < player2_roll else 2

        # For logging info, maybe helpful, reset per episode
        self.starter = self.turn
        self.player1_dice_history = []
        self.player1_action_history = []
        self.player2_dice_history = []
        self.player2_action_history = []
        self.start_time = time.time()

    # TODO
    def step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state. Accepts an action and returns a tuple
        (observation, reward, done, info).
        Args:
            action (object): an action provided by the environment
        Returns:
            observation (object): state of the current environment
            reward (float) : amount of reward returned after previous action
            done (boolean): whether the episode has ended, in which case further
            step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for
            debugging, and sometimes learning)
        """

        observation = self.board
        done = self.get_done()
        reward = self.get_reward(self.board, action)
        info = self.get_info()
        if done:
            self.reset()

        return (observation, reward, done, info)

    def reset(self):
        """Resets then returns the board."""

        self.board = np.array([[2, 2], [0, 0], [0, 0], [0, 0], [0, 0], [1, 5],
                               [0, 0], [1, 3], [0, 0], [0, 0], [0, 0], [2, 5],
                               [1, 5], [0, 0], [0, 0], [0, 0], [2, 3], [0, 0],
                               [2, 5], [0, 0], [0, 0], [0, 0], [0, 0], [1, 2]])
        player1_roll = np.sum(roll_dice())
        player2_roll = np.sum(roll_dice())
        while player1_roll == player2_roll:
            player1_roll = np.sum(roll_dice())
            player2_roll = np.sum(roll_dice())

        if self.higher_starts:
            self.turn = 1 if player1_roll > player2_roll else 2
        else:
            self.turn = 1 if player1_roll < player2_roll else 2

        # For logging info, maybe helpful, reset per episode
        self.starter = self.turn
        self.player1_dice_history = []
        self.player1_action_history = []
        self.player2_dice_history = []
        self.player2_action_history = []

        return self.board

    # TODO
    def render(self):
        """Represent the board in the terminal. In this representation, x is
        player1 and y is player 2."""

        # # For example, the initial board would be:
        # print("------|-|------")
        # print("o   o |-|o    x")
        # print("o   o |-|o    x")
        # print("o   o |-|o     ")
        # print("o     |-|o     ")
        # print("o     |-|o     ")
        # print("      |-|      ")
        # print("      |-|      ")
        # print("      |-|      ")
        # print("      |-|      ")
        # print("x     |-|x     ")
        # print("x     |-|x     ")
        # print("x   x |-|x     ")
        # print("x   x |-|x    o")
        # print("x   x |-|x    o")
        # print("------|-|------")

    # TODO
    def get_reward(self, action, state=None):
        """Basic implementation of pip counting. For detailed explaination and
        substitutes: http://www.bkgm.com/articles/Driver/GuideToCountingPips/.

        This will get the reward for the player1 by doing the following op:
        
        x = pip_count_player1_before_action - pip_count_player2_before_action
        y = pip_count_player1_after_action - pip_count_player2_after_action
        
        return x - y"""

        board = self.board if state is None else state

        # For player1
        before_pip_count1 = 0
        for index, point in enumerate(board):
            if point[0] == 1:
                before_pip_count1 += (point[1] * (24 - index))
        # For player2
        before_pip_count2 = 0
        for index, point in enumerate(board.flip(axis=0)):
            if point[0] == 2:
                before_pip_count2 += (point[1] * (24 - index))

        before = before_pip_count1 - before_pip_count2

        next_board = do_action(board, action)

        after_pip_count1 = 0
        for index, point in enumerate(next_board):
            if point[0] == 1:
                after_pip_count1 += (point[1] * (24 - index))
        # For player2
        after_pip_count2 = 0
        for index, point in enumerate(next_board.flip(axis=0)):
            if point[0] == 2:
                before_pip_count2 += (point[1] * (24 - index))

        after = after_pip_count1 - after_pip_count2

        return after - before

    def get_done(self):
        for player in [1, 2]:
            i = 0
            for point in self.board:
                if point[0] == player:
                    i += point[1]
            if i < 1:
                return True

    def get_info(self):
        """Returns useful info for debugging, etc."""

        return {'Starting player': self.starter,
                'Player 1 dice history': self.player1_dice_history,
                'Player 1 action history': self.player1_action_history,
                'Player 2 dice history': self.player2_dice_history,
                'Player 2 action history': self.player2_action_history}

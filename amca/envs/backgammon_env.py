# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import time

import gym
from gym import spaces

from amca.game import Game, roll_dice
from amca.player import Player


class BackgammonEnv(gym.Env):
    """Defines a Backgammon environment to run the RL algorithm in. It is
    stochastic and fully-observable, with a bounded, discrete domain.

    The action space has the following structure:
        [Action type, Source index/None, Target index/None]

    # -------- For source and target indices, 0 is reserved for None. -------- #

    For example, [0, 3, 7] moves the first player (white) from the 2nd to the
    6th point.
                   ---------------------------
                   |    Action    | Encoding |
                   |-------------------------|
                   |  Move        |    0     |
                   |  Hit         |    1     |
                   |  Bear-off    |    2     |
                   |  Reenter     |    3     |
                   |  Reenter-hit |    4     |
                   ---------------------------

    The observation space has the following structure:
        [
            [White checkers bourne off, Black checkers bourne off],
            [White checkers hit, Black checkers hit],
            [Empty/White/Black, Number of checkers], # For point 1
            [Empty/White/Black, Number of checkers], # For point 2
                                .
                                .
                                .
            [Empty/White/Black, Number of checkers]  # For point 24
        ]
    For an example, check the initial board setting.
    """

    metadata = {'render.modes': ['human']}

    def __init__(self, w_player=Player('w'), b_player=Player('b'), higher_starts=True):
        super(BackgammonEnv, self).__init__()

        # Environment-specific details; namely action and observation spaces.
        self.action_space = spaces.MultiDiscrete([5, 25, 25])
        self.observation_space = spaces.MultiDiscrete(
            [[16, 16],  # bourne off checkers for white/black
             [16, 16],  # hit checkers for white/black
             [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16],
             [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16],
             [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16],
             [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16]])

        # Gym users usually invoke reset before starting?
        # Game-specific details
        self.w_player = None
        self.b_player = None
        self.higher_starts = None
        self.game = None

        # For logging info, maybe helpful, gets reset per episode.
        self.starter = None
        self.w_player_dice_history = None
        self.w_player_action_history = None
        self.b_player_dice_history = None
        self.b_player_action_history = None
        self.start_time = None

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

        if self.turn == 1:
            reward = self.game.get_reward(self.w_player, action) # TODO
            self.game.update_board(self.w_player, action)
            self.turn = 2
        elif self.turn == 2:
            reward = self.game.get_reward(self.b_player, action) # TODO
            self.game.update_board(self.b_player, action)
            self.turn = 1

        observation = self.game.get_state4()
        done = self.game.is_over()
        info = self.get_info()
        if done:
            self.reset()

        return (observation, reward, done, info)

    def reset(self):
        """Resets then returns the board."""

        self.game = Game(self.w_player, self.b_player)
        player1_roll = sum(roll_dice())
        player2_roll = sum(roll_dice())
        while player1_roll == player2_roll:
            player1_roll = sum(roll_dice())
            player2_roll = sum(roll_dice())

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

        return self.game.get_state()

    # TODO
    def render(self):
        """Represent the board in the terminal. In this representation, x is
        player1 and y is player 2."""

        state = self.game.get_state()
        for index, info in enumerate(state):
            if index == 0:
                print('White player checkers bourne off: {}'.format(info[0]))
                print('Black player checkers bourne off: {}'.format(info[1]))
            elif index == 1:
                print('White player checkers hit: {}'.format(info[0]))
                print('Black player checkers hit: {}'.format(info[1]))
            else:
                break

        line1 = state[2][0]*state[2][1] + '   ' + ' '


    def get_info(self):
        """Returns useful info for debugging, etc."""

        return {'Starting player': self.starter,
                'Player 1 dice history': self.player1_dice_history,
                'Player 1 action history': self.player1_action_history,
                'Player 2 dice history': self.player2_dice_history,
                'Player 2 action history': self.player2_action_history}

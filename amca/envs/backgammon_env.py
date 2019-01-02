# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import time

import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

from amca.game import Game


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

    def __init__(self, game, higher_starts=True):

        # Environment-specific details; namely action and observation spaces.
        self.action_space = spaces.MultiDiscrete([5, 25, 25])
        self.observation_space = spaces.MultiDiscrete([[3, 16], ]*24)

        # Game-specific details
        self.higher_starts = higher_starts
        self.game = game
        w_player = self.game.get_player('w')
        b_player = self.game.get_player('b')

        # For logging info, maybe helpful, gets reset per episode.
        self.starter = self.turn
        self.w_player_dice_history = []
        self.w_player_action_history = []
        self.b_player_dice_history = []
        self.b_player_action_history = []
        self.start_time = time.time()

        # Determine first roll goes to which player.

        w_player_roll = np.sum(game.roll_dice())
        b_player_roll = np.sum(game.roll_dice())
        while w_player_roll == b_player_roll:
            w_player_roll = np.sum(game.roll_dice())
            b_player_roll = np.sum(game.roll_dice())

        if self.higher_starts:
            self.turn = 1 if w_player_roll > b_player_roll else 2
        else:
            self.turn = 2 if b_player_roll > w_player_roll else 2

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
            player = self.w_player
            self.turn = 2
        elif self.turn == 2:
            player = self.b_player
            self.turn = 1

        dice = self.game.get_dice()
        actions, rewards = self.get_actions(player, dice)
        action = player.make_decision(actions)
        reward = rewards[actions.index(action)]

        observation = self.game.get_state()  # TODO VERY CRITICAL
        info = self.get_info()
        done = self.game.is_over()
        if done:
            self.reset()

        return (observation, reward, done, info)

    def reset(self):
        """Resets then returns the board."""

        self.game = Game()
        player1_roll = np.sum(self.game.roll_dice())
        player2_roll = np.sum(self.game.roll_dice())
        while player1_roll == player2_roll:
            player1_roll = np.sum(self.game.roll_dice())
            player2_roll = np.sum(self.game.roll_dice())

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

    def get_info(self):
        """Returns useful info for debugging, etc."""

        return {'Starting player': self.starter,
                'Player 1 dice history': self.player1_dice_history,
                'Player 1 action history': self.player1_action_history,
                'Player 2 dice history': self.player2_dice_history,
                'Player 2 action history': self.player2_action_history}

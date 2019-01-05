# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import time

import gym
from gym import wrappers
import numpy as np
from gym import spaces

from amca.game import Game, roll_dice
from amca.player import Player


class BackgammonEnv(gym.Env):
    """
    Base class for the Backgammon environment. Defines a Backgammon environment
    to run the RL algorithm in. It is stochastic and fully-observable, with a
    bounded, discrete action domain.

    The action space is discrete, ranging from 0 to 2880 for each permutation
    of this tuple: <Action type, Source index, Target index>

    The observation space is a 54-D vector:
        [dice1,
         dice2,
         white hitted,
         black hitted,
         white bourne off,
         black bourne off,
         point1 color,
         point1 count,
         point2 color,
         point2 count,
               .
               .
               .
         point24 color,
         point24 count]
    """

    metadata = {'render.modes': ['human']}

    def __init__(self):
        # Environment-specific details; namely action and observation spaces.
        lower_bound = np.array([1, ]*2 + [0, ]*52)
        upper_bound = np.array([6, ]*2 + [15, ]*4 + [
            item for sublist in [[2, 15], ]*24 for item in sublist])
        self.observation_space = spaces.Box(low=lower_bound, high=upper_bound,
                                            dtype=np.float32)
        self.action_space = spaces.Discrete(5*24*24)

        self.__time_elapsed = time.time()
        self.__steps = 0

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
        print('NOWTHIS')
        print(action)
        reward, observation, done = self.game.play(action)
        info = self.get_info()
        if done:
            self.reset()
        self.steps += 1

        return (observation, reward, done, info)

    def render(self):
        """Represent the board in the terminal. In this representation, x is
        player1 and y is player 2."""

        self.game.print_observation()

    def get_info(self):
        """Returns useful info for debugging, etc."""

        return {'time elapsed': time.time() - self.__time_elapsed,
                'steps': self.__steps}


class BackgammonPolicyEnv(BackgammonEnv):
    """
        Uses a policy as the opponent for the Backgammon environment.
    """

    def __init__(self):
        BackgammonEnv.__init__(self)

    def reset(self):
        """Resets then returns the board."""

        self.game = Game()

        return self.game.get_observation()


class BackgammonHumanEnv(BackgammonEnv):
    """
        Uses a human as the opponent for the Backgammon environment.
    """

    def __init__(self):
        BackgammonEnv.__init__(self)

    def reset(self):
        """Resets then returns the board."""

        self.game = Game(agent='human')

        return self.game.get_observation()


class BackgammonPolicyContinuousEnv(BackgammonPolicyEnv):
    """
        Uses a continuous action space for the Backgammon Policy environment.
    """

    def __init__(self):
        BackgammonPolicyEnv.__init__(self)
        self.action_space = spaces.Box(low=np.array([-2880]),
                                       high=np.array([2880]),
                                       dtype=np.float32)


class BackgammonHumanContinuousEnv(BackgammonHumanEnv):
    """
        Uses a continuous action space for the Backgammon Human environment.
    """

    def __init__(self):
        BackgammonPolicyEnv.__init__(self)
        self.action_space = spaces.Box(low=np.array([-2880]),
                                       high=np.array([2880]),
                                       dtype=np.float32)

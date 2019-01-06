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
import time

import gym
from gym import spaces
import numpy as np

from amca.envs.board import Board
from amca.agents import RandomAgent, PolicyAgent, HumanAgent


def roll_dice():
    dice = [np.random.randint(1, 6), np.random.randint(1, 6)]
    if dice[0] == dice[1]:
        return [dice[0], ]*4


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

        # Debug info
        self.__invalid_actions_taken = 0
        self.__time_elapsed = 0

        # Initialize game vars
        self.__gameboard = Board()
        self.__w_hitted = 0
        self.__b_hitted = 0
        self.__w_bourne_off = 0
        self.__b_bourne_off = 0
        self.__w_canbearoff = False
        self.__b_canbearoff = False

        # The higher dice roll starts
        w_toss = roll_dice()
        b_toss = roll_dice()
        while sum(w_toss) == sum(b_toss):
            w_toss = roll_dice()
            b_toss = roll_dice()
        if sum(w_toss) > sum(b_toss):
            self.__turn = 1
        else:
            self.__turn = 2

        # Start game
        self.__dice = roll_dice()
        if self.__turn == 2:
            self.play_opponent()

    # TODO
    def get_valid_actions(self):
        """Returns a NUMPY array of NUMPY arrays as such:
        [
            [Valid action 1, Valid action 2, ...], # Dice 1 valid actions
            [Valid action 1, Valid action 2, ...], # Dice 2 valid actions
            .
            .
        ]
        """

    # TODO
    def act(self, action):
        """Takes an INTEGER as defined in the action space and modifies the
        board as neccessary, including the checkers hit and bourne off."""

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
        # Case of playing out of turn
        if self.__turn != 1:
            raise ValueError('Agent playing out of turn!')

        valid_actions = self.get_valid_actions()  # TODO
        action_is_valid = False

        # Case of no valid actions
        if not valid_actions:
            self.__turn = 2
            self.__dice = roll_dice()
            self.play_opponent()
            reward = 0
            observation = self.get_observation()
            done = self.get_done()
            info = self.get_info()
            if done:
                self.reset()
            return (observation, reward, done, info)

        # Else
        for index, action_set in enumerate(valid_actions):
            if action in action_set:
                action_is_valid = True
                reward = self.act(action)  # TODO
                del self.__dice[index]
                break
        if not action_is_valid:
            reward = -1000
            action = np.random.choice(valid_actions.flatten())
            for index, action_set in enumerate(valid_actions):
                if action in action_set:
                    self.act(action)
                    del self.__dice[index]
                    break
            observation = self.get_observation()
            done = self.get_done()
            info = self.get_info()
            if done:
                self.reset()

        if not self.__dice:
            self.__turn = 2
            self.__dice = roll_dice()
            self.play_opponent()

        observation = self.get_observation()
        done = self.get_done()
        info = self.get_info()
        if done:
            self.reset()

        return (observation, reward, done, info)

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
            ' |13  14  15  16   17   18   |    | 19   20   21   22   23   24  | ')
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
            ' |12  11  10   9    8    7    |    | 6    5    4    3    2    1  | ')
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

    def reset(self):
        # Initialize game vars
        self.__gameboard = Board()
        self.__w_hitted = 0
        self.__b_hitted = 0
        self.__w_bourne_off = 0
        self.__b_bourne_off = 0
        self.__w_canbearoff = False
        self.__b_canbearoff = False

        # The higher dice roll starts
        w_toss = roll_dice()
        b_toss = roll_dice()
        while sum(w_toss) == sum(b_toss):
            w_toss = roll_dice()
            b_toss = roll_dice()
        if sum(w_toss) > sum(b_toss):
            self.__turn = 1
        else:
            self.__turn = 2

        # Start game
        self.__dice = roll_dice()
        if self.__turn == 2:
            self.play_opponent()

        return self.get_observation()

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

    def play_opponent(self):
        # Case of playing out of turn
        if self.__turn != 2:
            raise ValueError('Opponent playing out of turn!')

        # Case of no valid actions
        valid_actions = self.get_valid_actions()  # TODO
        if not valid_actions:
            self.__turn = 1
            self.__dice = roll_dice()
            return

        # Else
        while self.__dice:
            action = self.__opponent.make_decision(self.get_observation())
            action_is_valid = False
            for index, action_set in enumerate(valid_actions):
                if action in action_set:
                    action_is_valid = True
                    self.act(action)  # TODO
                    del self.__dice[index]
                    break
            if not action_is_valid:
                action = np.random.choice(valid_actions.flatten())
                for index, action_set in enumerate(valid_actions):
                    if action in action_set:
                        self.act(action)
                        del self.__dice[index]
                        break

        self.__turn = 1
        self.__dice = roll_dice()

    def get_info(self):
        """Returns useful info for debugging, etc."""

        return {'time elapsed': time.time() - self.__time_elapsed,
                'invalid actions taken': self.__invalid_actions_taken}


class BackgammonRandomOpponentEnv(BackgammonEnv):
    """
        Uses a random agent as the opponent for the Backgammon environment.
    """

    def __init__(self):
        self.__opponent = RandomAgent(self.action_space)
        BackgammonEnv.__init__(self)


class BackgammonPolicyOpponentEnv(BackgammonEnv):
    """
        Uses a policy agent as the opponent for the Backgammon environment.
    """

    def __init__(self):
        self.__opponent = PolicyAgent(algorithm='dqn', model='amca.pkl')
        BackgammonEnv.__init__(self)


class BackgammonHumanOpponentEnv(BackgammonEnv):
    """
        Uses a human agent as the opponent for the Backgammon environment.
    """

    def __init__(self):
        self.__opponent = HumanAgent()
        BackgammonEnv.__init__(self)

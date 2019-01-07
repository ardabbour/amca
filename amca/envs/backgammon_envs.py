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
                actions.append(['move', i, j])
                actions.append(['move', j, i])
                actions.append(['hit', i, j])
                actions.append(['hit', j, i])

    # 'reenter's, 'reenter_hit's and 'bearoff's
    for j in homes:
        actions.append(['reenter', j])
        actions.append(['reenter_hit', j])
        actions.append(['bearoff', j])

    return actions


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
        self.__all_possible_actions = all_possible_actions()
        self.action_space = spaces.Discrete(len(self.__all_possible_actions))
        self.__opponent = RandomAgent(self.action_space)

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
        if self.__turn == 2:
            self.__dice = roll_dice()
            self.play_opponent()

    def get_action(self, actionint):
        return self.__all_possible_actions[actionint]

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

        return np.array(acts), np.array(rews)

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

    def step(self, actionint):
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

        action = self.get_action(actionint)  # TODO
        valid_actions, their_rewards = self.get_valid_actions()

        # Case of playing out of turn
        if self.__turn != 1:
            raise ValueError('Agent playing out of turn!')

        # Case of no valid actions
        if len(valid_actions.flatten()) < 1:
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

        # Case of choosing valid action
        action_is_valid = False
        for index, action_set in enumerate(valid_actions):
            if action in action_set:
                action_is_valid = True
                reward = their_rewards[index][np.where(action_set == action)]
                self.act(action)
                del self.__dice[index]
                break

        # Case of choosing invalid action
        if not action_is_valid:
            reward = -1000
            action = np.random.choice(valid_actions.flatten())
            for index, action_set in enumerate(valid_actions):
                if action in action_set:
                    self.act(action)
                    del self.__dice[index]
                    break

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
        valid_actions, _ = self.get_valid_actions()
        if len(valid_actions.flatten()) < 1:
            self.__turn = 1
            self.__dice = roll_dice()
            return

        # Else
        while self.__dice:
            actionint = self.__opponent.make_decision(self.get_observation())
            action = self.get_action(actionint)  # TODO
            action_is_valid = False
            for index, action_set in enumerate(valid_actions):
                if action in action_set:
                    action_is_valid = True
                    self.act(action)
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
                return (True, self.get_player(color))

        return False

    def get_info(self):
        """Returns useful info for debugging, etc."""

        return {'time elapsed': time.time() - self.__time_elapsed,
                'invalid actions taken': self.__invalid_actions_taken}


class BackgammonRandomOpponentEnv(BackgammonEnv):
    """
        Uses a random agent as the opponent for the Backgammon environment.
    """

    def __init__(self):
        BackgammonEnv.__init__(self)
        # BackgammonEnv.__opponent = RandomAgent(self.action_space)


# class BackgammonPolicyOpponentEnv(BackgammonEnv):
#     """
#         Uses a policy agent as the opponent for the Backgammon environment.
#     """

#     def __init__(self):
#         self.__opponent = PolicyAgent(algorithm='dqn', model='amca.pkl')
#         BackgammonEnv.__init__(self)


class BackgammonHumanOpponentEnv(BackgammonEnv):
    """
        Uses a human agent as the opponent for the Backgammon environment.
    """

    def __init__(self):
        BackgammonEnv.__init__(self)
        self.__opponent = HumanAgent()

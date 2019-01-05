# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
    Amca: The RL-Based Backgammon Agent
    https://github.com/ardabbour/amca/

    Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu
    Cognitive Robotics Laboratory
    Faculty of Engineering and Natural Sciences
    Sabanci University

    All elements related to the player's functionality are defined here.
"""

import random
from stable_baselines import A2C, ACER, ACKTR, DDPG, DQN, GAIL, PPO2, TRPO, SAC


class Player:
    """A player can be a human or an AI. If it is a human, the human will have
    to throw the dice and get a list of possible moves from the game."""

    def __init__(self, algorithm=None, policy='random'):
        """Define a new player object."""

        if policy == 'random':
            self.__policy = lambda x: (random.choice(x), None)
        elif policy == 'human':
            self.__policy = lambda x: (self.human_play(x), None)
        else:
            if algorithm.lower() == 'a2c':
                algorithm = A2C
            elif algorithm.lower() == 'acer':
                algorithm = ACER
            elif algorithm.lower() == 'acktr':
                algorithm = ACKTR
            elif algorithm.lower() == 'ddpg':
                algorithm = DDPG
            elif algorithm.lower() == 'dqn':
                algorithm = DQN
            elif algorithm.lower() == 'gail':
                algorithm = GAIL
            elif algorithm.lower() == 'ppo':
                algorithm = PPO2
            elif algorithm.lower() == 'sac':
                algorithm = SAC
            elif algorithm.lower() == 'trpo':
                algorithm = TRPO
            else:
                raise ValueError('Unidentified algorithm chosen')

            self.__policy = algorithm.load(policy).predict

    def get_policy(self):
        return self.__policy

    def set_policy(self, algorithm, policy):
        if policy == 'random':
            self.__policy = lambda x: random.choice(x)
        elif policy == 'human':
            self.__policy = self.human_play
        else:
            if algorithm.lower() == 'a2c':
                algorithm = A2C
            elif algorithm.lower() == 'acer':
                algorithm = ACER
            elif algorithm.lower() == 'acktr':
                algorithm = ACKTR
            elif algorithm.lower() == 'ddpg':
                algorithm = DDPG
            elif algorithm.lower() == 'dqn':
                algorithm = DQN
            elif algorithm.lower() == 'gail':
                algorithm = GAIL
            elif algorithm.lower() == 'ppo':
                algorithm = PPO2
            elif algorithm.lower() == 'sac':
                algorithm = SAC
            elif algorithm.lower() == 'trpo':
                algorithm = TRPO
            else:
                raise ValueError('Unidentified algorithm chosen')

            self.__policy = algorithm.load(policy)

    def human_play(self, observation, valid_actions):
        # print(observation)  # TODO
        print(valid_actions)
        action = input('What action would you like to do?')
        return action

    def play(self, observation, valid_actions):

        if self.__policy == self.human_play:
            return self.human_play(observation, valid_actions)

        action, _ = self.__policy(observation)
        return action

# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
    Amca: The RL-Based Backgammon Agent
    https://github.com/ardabbour/amca/

    Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu
    Cognitive Robotics Laboratory
    Faculty of Engineering and Natural Sciences
    Sabanci University

    The Policy agent takes an action according to a DNN.
"""

from stable_baselines import A2C, ACER, ACKTR, DDPG, DQN, GAIL, PPO2, TRPO, SAC


class PolicyAgent:
    def __init__(self, algorithm, model):
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

        self.__policy = algorithm.load(model)

    def make_decision(self, observation):
        """Returns the action according to the policy and observation."""

        action, _ = self.__policy.predict(observation)

        return action

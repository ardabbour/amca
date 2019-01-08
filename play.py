# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
    Amca: The RL-Based Backgammon Agent
    https://github.com/ardabbour/amca/

    Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu
    Cognitive Robotics Laboratory
    Faculty of Engineering and Natural Sciences
    Sabanci University

    This script allows us to play backgammon with the RL-trained agent, amca.
"""

import argparse

import gym
from stable_baselines import A2C, ACER, ACKTR, DDPG, DQN, GAIL, PPO2, TRPO, SAC

import amca

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Train an agent using RL')
    PARSER.add_argument('--algorithm', '-a',
                        help='Algorithm used to train the model.',
                        default='PPO',
                        type=str)
    PARSER.add_argument('--model', '-m',
                        help='Path to model',
                        default='amca/models/amca.pkl',
                        type=str)

    ARGS = PARSER.parse_args()

    if ARGS.algorithm.lower() == 'a2c':
        algorithm = A2C
    elif ARGS.algorithm.lower() == 'acer':
        algorithm = ACER
    elif ARGS.algorithm.lower() == 'acktr':
        algorithm = ACKTR
    elif ARGS.algorithm.lower() == 'ddpg':
        algorithm = DDPG
    elif ARGS.algorithm.lower() == 'dqn':
        algorithm = DQN
    elif ARGS.algorithm.lower() == 'gail':
        algorithm = GAIL
    elif ARGS.algorithm.lower() == 'ppo':
        algorithm = PPO2
    elif ARGS.algorithm.lower() == 'sac':
        algorithm = SAC
    elif ARGS.algorithm.lower() == 'trpo':
        algorithm = TRPO
    else:
        raise ValueError('Unidentified algorithm chosen')

    if algorithm in [DDPG, GAIL, SAC]:
        env = gym.make('BackgammonHumanContinuousEnv-v0')
    else:
        env = gym.make('BackgammonHumanEnv-v0')
    model = algorithm.load(ARGS.model)

    obs = env.reset()
    while True:
        action, _ = model.predict(obs)
        obs, _, dones, _ = env.step(action)
        env.render()
        if dones:
            print('Done!')
            break

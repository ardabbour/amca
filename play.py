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
    PARSER.add_argument('algorithm',
                        help='RL algorithm used to develop the model.',
                        default='DQN',
                        type=str)
    PARSER.add_argument('model',
                        help='Model.',
                        default=1,
                        type=int)

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
        env = gym.make('BackgammonHumanContinuous-v0')
    else:
        env = gym.make('BackgammonHuman-v0')
    model = ARGS.algorithm.load(ARGS.model)

    obs = env.reset()
    while True:
        action, _states = model.predict(obs)
        obs, _, dones, _ = env.step(action)
        env.render()
        if dones:
            print('Done!')
            break

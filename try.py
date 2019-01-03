# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
    Amca: The RL-Based Backgammon Agent
    https://github.com/ardabbour/amca/

    Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu
    Cognitive Robotics Laboratory
    Faculty of Engineering and Natural Sciences
    Sabanci University

    This script allows us to train an RL agent using Gym and Stable Baselines.
    Saves a graph of the training process, showing mean reward vs. timesteps.
"""

# Standard imports
import os
import argparse

# Scientific Python imports
import numpy as np
import matplotlib.pyplot as plt

# Reinforcement Learning imports
import gym
from stable_baselines import A2C, ACER, ACKTR, DDPG, DQN, GAIL, PPO2, TRPO
from stable_baselines.bench import Monitor
from stable_baselines.common.policies import MlpPolicy, MlpLstmPolicy, MlpLnLstmPolicy, CnnPolicy, CnnLstmPolicy, CnnLnLstmPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.results_plotter import load_results, ts2xy


def movingAverage(values, window):
    """
    Smooth values by doing a moving average
    :param values: (numpy array)
    :param window: (int)
    :return: (numpy array)
    """

    weights = np.repeat(1.0, window) / window
    return np.convolve(values, weights, 'valid')


def plot_results(log_folder, title):
    """
    plot the results

    :param log_folder: (str) the save location of the results to plot
    :param title: (str) the title of the task to plot
    """
    x, y = ts2xy(load_results(log_folder), 'timesteps')
    y = movingAverage(y, window=50)
    # Truncate x
    x = x[len(x) - len(y):]

    plt.plot(x, y)
    plt.xlabel('Number of Timesteps')
    plt.ylabel('Rewards')
    plt.title(title + " Smoothed")
    plt.savefig('{}.pdf'.format(title))


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Train an agent using RL')
    PARSER.add_argument('env',
                        help='Environment ID. Must be registered.',
                        type=str)
    PARSER.add_argument('name',
                        help='Model name.',
                        type=str)
    PARSER.add_argument('--logdirectory', '-l',
                        help='Directory to store log files.',
                        default='logs/',
                        type=str)
    PARSER.add_argument('--policy', '-p',
                        help='Policy network type.',
                        default='MLP')
    PARSER.add_argument('--algorithm', '-a',
                        help='RL Algorithm.',
                        default='A2C',
                        type=str)
    PARSER.add_argument('--timesteps', '-t',
                        help='Number of timesteps to train.',
                        default=10000,
                        type=int)
    PARSER.add_argument('--verbose', '-v',
                        help='Verbosity.',
                        default=1,
                        type=int)

    ARGS = PARSER.parse_args()

    env = gym.make(ARGS.env)
    logdir = ARGS.logdirectory
    os.makedirs(logdir, exist_ok=True)
    env = Monitor(env, logdir, allow_early_resets=True)
    env = DummyVecEnv([lambda: env])

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
    elif ARGS.algorithm.lower() == 'trpo':
        algorithm = TRPO
    else:
        raise ValueError('Unidentified algorithm chosen')

    if ARGS.policy.lower() == 'mlp':
        policy = MlpPolicy
    elif ARGS.policy.lower() == 'mlplstm':
        policy = MlpLstmPolicy
    elif ARGS.policy.lower() == 'mlplnlstm':
        policy = MlpLnLstmPolicy
    elif ARGS.policy.lower() == 'cnn':
        policy = CnnPolicy
    elif ARGS.policy.lower() == 'cnnlstm':
        policy = CnnLstmPolicy
    elif ARGS.policy.lower() == 'cnnlnlstm':
        policy = CnnLnLstmPolicy
    else:
        raise ValueError('Unidentified policy chosen')

    model = algorithm(policy, env, verbose=ARGS.verbose)
    model.learn(total_timesteps=ARGS.timesteps)
    model.save('{}'.format(ARGS.name))

    # a2c_model = A2C(MlpPolicy, env, verbose=1)
    # a2c_model.learn(total_timesteps=100000)
    # a2c_model.save('a2c_model')

    # ppo_model = PPO2(MlpPolicy, env, verbose=1)
    # ppo_model.learn(total_timesteps=100000)
    # ppo_model.save('a2c_model')

    # ddpg_model = PPO2(MlpPolicy, env, verbose=1)
    # ddpg_model.learn(total_timesteps=100000)
    # ddpg_model.save('ddpg_model')


# obs = env.reset()
# for i in range(100000):
#     action, _ = model.predict(obs)
#     obs, _, _, _ = env.step(action)
#     time.sleep(0.01)
#     env.render()

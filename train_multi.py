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
    Uses the default hyperparameters of each algorithm. Saves a graph of the
    training process, showing mean reward vs. timesteps.
"""

# Standard imports
import os
import argparse

# Scientific Python imports
import numpy as np
import matplotlib.pyplot as plt

# Reinforcement Learning imports
import gym
from stable_baselines import A2C, ACER, ACKTR, DDPG, DQN, GAIL, PPO2, TRPO, SAC
from stable_baselines.bench import Monitor
from stable_baselines.common.policies import MlpPolicy, MlpLstmPolicy, MlpLnLstmPolicy, CnnPolicy, CnnLstmPolicy, CnnLnLstmPolicy
from stable_baselines.deepq import policies as dqn_policies
from stable_baselines.ddpg import policies as ddpg_policies
from stable_baselines.sac import policies as sac_policies
from stable_baselines.common import set_global_seeds
from stable_baselines.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines.results_plotter import load_results, ts2xy

import amca


def movingAverage(values, window):
    """
    Smooth values by doing a moving average
    :param values: (numpy array)
    :param window: (int)
    :return: (numpy array)
    """

    weights = np.repeat(1.0, window) / window
    return np.convolve(values, weights, 'valid')


def plot_results(logdir, title, window):
    """
    plot the results

    :param log_folder: (str) the save location of the results to plot
    :param title: (str) the title of the task to plot
    """
    x, y = ts2xy(load_results(logdir), 'timesteps')
    y = movingAverage(y, window)
    # Truncate x
    x = x[len(x) - len(y):]
    print(np.array(x).shape, np.array(y).shape)
    plt.plot(x, y)
    plt.xlabel('Timesteps')
    plt.ylabel('Mean Reward per {} timestep'.format(window))
    plt.title('{} Training Performance'.format(title))
    plt.savefig('{}_training_performance.pdf'.format(title))


def make_env(algorithm, rank, seed=0):
    """
    Utility function for multiprocessed env.

    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environment you wish to have in subprocesses
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """

    def _init():
        if algorithm in [DDPG, GAIL, SAC]:
            env = gym.make('BackgammonRandomContinuous-v0')
        else:
            env = gym.make('BackgammonRandomEnv-v0')
        env.seed(seed + rank)

        os.makedirs(ARGS.log_directory, exist_ok=True)
        env = Monitor(env, ARGS.log_directory, allow_early_resets=True)
        return env
    set_global_seeds(seed)
    return _init


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Train an agent using RL')
    PARSER.add_argument('--name', '-n',
                        help='Name of the agent to be trained.',
                        default='new_amca',
                        type=str)
    PARSER.add_argument('--log_directory', '-l',
                        help='Directory to store log files.',
                        default='logs/',
                        type=str)
    PARSER.add_argument('--policy', '-p',
                        help='Policy network type.',
                        default='MLP')
    PARSER.add_argument('--algorithm', '-a',
                        help='RL Algorithm.',
                        default='DQN',
                        type=str)
    PARSER.add_argument('--timesteps', '-t',
                        help='Number of timesteps to train.',
                        default=100000,
                        type=int)
    PARSER.add_argument('--window', '-w',
                        help='Moving average window for mean reward plotting.',
                        default=50,
                        type=int)
    PARSER.add_argument('--verbose', '-v',
                        help='Verbosity.',
                        default=1,
                        type=int)
    PARSER.add_argument('--graph', '-g',
                        help='Plot a performance graph of the training.',
                        default=1,
                        type=int)
    PARSER.add_argument('--multiprocess', '-m',
                        help='How many multiprocesses to use.',
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
        MlpPolicy = ddpg_policies.MlpPolicy
        CnnPolicy = ddpg_policies.CnnPolicy
        LnMlpPolicy = ddpg_policies.LnMlpPolicy
        LnCnnPolicy = ddpg_policies.LnCnnPolicy
    elif ARGS.algorithm.lower() == 'dqn':
        algorithm = DQN
        MlpPolicy = dqn_policies.MlpPolicy
        CnnPolicy = dqn_policies.CnnPolicy
        LnMlpPolicy = dqn_policies.LnMlpPolicy
        LnCnnPolicy = dqn_policies.LnCnnPolicy
    elif ARGS.algorithm.lower() == 'gail':
        algorithm = GAIL
    elif ARGS.algorithm.lower() == 'ppo':
        algorithm = PPO2
    elif ARGS.algorithm.lower() == 'sac':
        algorithm = SAC
        MlpPolicy = sac_policies.MlpPolicy
        CnnPolicy = sac_policies.CnnPolicy
        LnMlpPolicy = sac_policies.LnMlpPolicy
        LnCnnPolicy = sac_policies.LnCnnPolicy
    elif ARGS.algorithm.lower() == 'trpo':
        algorithm = TRPO
    else:
        raise ValueError('Unidentified algorithm chosen')

    if ARGS.policy.lower() == 'mlp':
        policy = MlpPolicy
    elif ARGS.policy.lower() == 'lnmlp':
        policy = LnMlpPolicy
    elif ARGS.policy.lower() == 'mlplstm':
        policy = MlpLstmPolicy
    elif ARGS.policy.lower() == 'mlplnlstm':
        policy = MlpLnLstmPolicy
    elif ARGS.policy.lower() == 'cnn':
        policy = CnnPolicy
    elif ARGS.policy.lower() == 'lncnn':
        policy = LnCnnPolicy
    elif ARGS.policy.lower() == 'cnnlstm':
        policy = CnnLstmPolicy
    elif ARGS.policy.lower() == 'cnnlnlstm':
        policy = CnnLnLstmPolicy
    else:
        raise ValueError('Unidentified policy chosen')

    env = SubprocVecEnv([make_env(algorithm, i) for i in range(int(ARGS.multiprocess))])

    model = algorithm(policy, env, verbose=ARGS.verbose)

    model.learn(total_timesteps=ARGS.timesteps)
    model.save('{}'.format(ARGS.name))

    if ARGS.graph:
        plot_results(ARGS.log_directory, ARGS.algorithm, ARGS.window)

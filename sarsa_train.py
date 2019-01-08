# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
    Amca: The RL-Based Backgammon Agent
    https://github.com/ardabbour/amca/

    Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu
    Cognitive Robotics Laboratory
    Faculty of Engineering and Natural Sciences
    Sabanci University

    This script allows us to train a Backgammon agent using the SARSA algorithm.
"""

import argparse
import pickle

from amca.game import SarsaGame
from amca.agents import SarsaAgent, RandomSarsaAgent


def train(agent_train, opponent, maxmove):
    gamei = SarsaGame(agent_train, opponent)
    num_move = 0
    gamei.roll_dice()
    while (num_move < maxmove) and (not gamei.is_over()):

        # Agent turn
        if not gamei.is_over():
            curstate = gamei.get_state3(gamei.get_dice(0))
            possible_actions, their_rewards = gamei.get_actions(
                agent_train, gamei.get_dice(0))
            curaction, action_index = agent_train.chooseAction(
                curstate, possible_actions)
            gamei.update_board(agent_train, curaction)
            reward = their_rewards[action_index]
            nextstate = gamei.get_state3(gamei.get_dice(1))
        if not gamei.is_over():
            curstate = gamei.get_state3(gamei.get_dice(1))
            possible_actions, their_rewards = gamei.get_actions(
                agent_train, gamei.get_dice(1))
            nextaction, action_index = agent_train.chooseAction(
                curstate, possible_actions)
            gamei.update_board(agent_train, nextaction)
            agent_train.learn(curstate, curaction,
                              reward, nextstate, nextaction)
            reward = their_rewards[action_index]

            # Opponent turn
            gamei.roll_dice()
            for i in range(2):
                if not gamei.is_over():
                    nextstate = gamei.get_dice(i)
                    possible_actions, their_rewards = gamei.get_actions(
                        opponent, gamei.get_dice(i))
                    oppaction, action_index = opponent.chooseAction(
                        nextstate, possible_actions)
                    gamei.update_board(opponent, oppaction)
            gamei.roll_dice()
            nextstate = gamei.get_state3(gamei.get_dice(0))
            agent_train.learn(curstate, curaction,
                              reward, nextstate, nextaction)

        num_move += 1

    return agent_train


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Train an agent using RL')
    PARSER.add_argument('--name', '-n',
                        help='Name of the agent to be trained.',
                        default='amca/models/sarsa-vs_random-1M.pkl',
                        type=str)
    PARSER.add_argument('--maxmove', '-m',
                        help='Maximum number of moves per game.',
                        default=100)
    PARSER.add_argument('--games', '-g',
                        help='Number of games to play.',
                        default=1000000)
    PARSER.add_argument('--verbose', '-v',
                        help='Toggle verbosity',
                        default=1)
    PARSER.add_argument('--continued', '-c',
                        help='If the agent is saved, load it and continue training',
                        default=0)

    ARGS = PARSER.parse_args()

    if bool(int(ARGS.continued)):
        infilename = ARGS.name
        with open(infilename, 'rb') as f:
            agent = pickle.load(f)
    else:
        agent = SarsaAgent()

    for i in range(int(ARGS.games)):
        if int(ARGS.verbose):
            print('Completed {} games'.format(i))
        try:
            agent = train(agent, RandomSarsaAgent('opponent'), maxmove=int(ARGS.maxmove))
        except:
            pass

    if bool(int(ARGS.continued)):
        outfilename = '{}-updated.pkl'.format(ARGS.name)
    else:
        outfilename = ARGS.name
    with open(outfilename, 'wb') as f:
        pickle.dump(agent, f)

# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
    Amca: The RL-Based Backgammon Agent
    https://github.com/ardabbour/amca/

    Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu
    Cognitive Robotics Laboratory
    Faculty of Engineering and Natural Sciences
    Sabanci University

    This script allows us to play against a SARSA Backgammon agent.
"""

import argparse
import pickle

from amca.game import SarsaGame

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Train an agent using RL')
    PARSER.add_argument('--name', '-n',
                        help='Name of the agent to play againts.',
                        default='amca/models/sarsa-vs_random-1M.pkl',
                        type=str)
    PARSER.add_argument('--games', '-g',
                        help='Number of games to play.',
                        default=1)

    ARGS = PARSER.parse_args()

    filename = ARGS.name
    infile = open(filename, 'rb')
    agent = pickle.load(infile)
    infile.close()

    # TODO Make human player 1
    opponent = 'human'
    gamei = SarsaGame(agent, opponent)
    num_move = 0

    for _ in range(int(ARGS.games)):
        while (not gamei.is_over()):

            gamei.roll_dice()
            curstate = gamei.get_state3(gamei.get_dice(0))
            possible_actions, their_rewards = gamei.get_actions(
                agent, gamei.get_dice(0))
            curaction = agent.playAction(curstate, possible_actions)
            gamei.update_board(agent, curaction)
            print("Computer Turn, dices: " + str(gamei.get_dice(0)) +
                  " " + str(gamei.get_dice(1)))
            print("Computer played: ")
            print(curaction)

            if not gamei.is_over():
                nextstate = gamei.get_state3(gamei.get_dice(1))
                possible_actions, their_rewards = gamei.get_actions(
                    agent, gamei.get_dice(1))
                nextaction = agent.playAction(curstate, possible_actions)
                gamei.update_board(agent, nextaction)
                print("Computer played: ")
                print(nextaction)
            if not gamei.is_over():
                gamei.roll_dice()
                print("Human Turn, dices: " + str(gamei.get_dice(0)) +
                      " " + str(gamei.get_dice(1)))
                gamei.render()
                move_type = input(
                    'input your action type from {move,hit,reenter,reenter_hit,bearoff}')
                if move_type == 'move' or 'hit':
                    source = int(input('input your source from {0,1,..,23}'))
                    target = int(input('input your target from {0,1,..,23}'))
                    human_action = (move_type, source, target)
                elif move_type == 'bearoff':
                    source = int(input('input your source from {0,1,..,23}'))
                    human_action = (move_type, source)
                elif move_type == 'reenter' or 'reenter_hit':
                    target = int(input('input your target from {0,1,..,23}'))
                    human_action = (move_type, target)
                gamei.update_board(opponent, human_action)
            if not gamei.is_over():
                gamei.render()
                move_type = input(
                    'input your action type from {move,hit,reenter,reenter_hit,bearoff}')
                if move_type == 'move' or 'hit':
                    source = int(input('input your source from {0,1,..,23}'))
                    target = int(input('input your target from {0,1,..,23}'))
                    human_action = (move_type, source, target)
                elif move_type == 'bearoff':
                    source = int(input('input your source from {0,1,..,23}'))
                    human_action = (move_type, source)
                elif move_type == 'reenter' or 'reenter_hit':
                    target = int(input('input your target from {0,1,..,23}'))
                    human_action = (move_type, target)

                gamei.update_board(opponent, human_action)

            num_move = num_move+1

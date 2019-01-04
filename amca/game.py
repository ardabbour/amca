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

from amca.player import Player
from amca.board import Board
import random


def roll_dice():
    return [random.randint(1, 6), random.randint(1, 6)]


class Game:
    """Defines a backgammon game object."""

    def __init__(self, w_player, b_player):
        self.__w_player = w_player
        self.__b_player = b_player
        self.__gameboard = Board()
        self.__dice = []

        self.__w_bourne_off = 0
        self.__b_bourne_off = 0
        self.__w_hitted = 0
        self.__b_hitted = 0
        self.__w_canbearoff = False
        self.__b_canbearoff = False

    def get_player(self, color):
        """Returns the winning player based on the color."""

        assert color == 'w' or 'b'

        return self.__w_player if color == 'w' else self.__b_player

    def roll_dice(self):
        self.__dice = [random.randint(1, 6), random.randint(1, 6)]

    def get_dice(self):
        return self.__dice

    def letter(self, playerid, x):
        white_indices = ["0", "1", "2", "3", "4", "5", "6",
                         "7", "8", "9", "R", "U", "T", "V", "W", "Y", "Z"]
        black_indices = ["0", "A", "B", "C", "D", "E", "F",
                         "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q"]
        if playerid == "w":
            a = white_indices[x]
        elif playerid == "b":
            a = black_indices[x]
        return a

    def get_state(self):
        statevec = []

        for point in self.__gameboard.get_board():
            if point.get_color() == 'w':
                statevec.append(point.get_count())
            if point.get_color() == 'b':
                statevec.append(16+point.get_count())
            else:
                statevec.append(0)
        return statevec

    def get_state2(self):
        statestr = str(self.__dice[0]) + str(self.__dice[1])

        for point in self.__gameboard.get_board():
            if point.get_color() == 'w':
                statestr += self.letter("w", point.get_count())
            if point.get_color() == 'b':
                statestr += self.letter("b", point.get_count())
            else:
                statestr += "0"
        return statestr

    def get_state3(self, adice):
        statestr = str(adice)

        for point in self.__gameboard.get_board():
            if point.get_color() == 'w':
                statestr += self.letter("w", point.get_count())
            if point.get_color() == 'b':
                statestr += self.letter("b", point.get_count())
            else:
                statestr += "0"
        return statestr

    def get_state4(self):
        state = [[self.__w_bourne_off, self.__b_bourne_off],
                 [self.__w_hitted, self.__b_hitted]]
        board = self.__gameboard.get_board()
        for point in board:
            if point.get_color() == None:
                color = 0
            elif point.get_color() == 'w':
                color = 1
            elif point.get_color() == 'b':
                color = 2
            state.append([color, point.get_count()])
        return state

    def update_board(self, player, action):
        """Given a tuple of dice rolls, return the set of possible moves.

        1) Move: move forward from one point to another, as long as the target
                 point is empty or having the same color as the source point.
        2) Hit: To move to a point occupied by an opposing blot and put the blot
                on the bar.
        3) Reenter: To move a checker from the bar to an open point in the
                    opponent's home board according to a roll of the dice. When
                    a player has a checker on the bar, this is his only legal
                    move.
        4) Bear off: To remove a checker from the board according to a roll of
                     the dice after all of your checkers have been brought into
                     your home board."""

        if player == self.__w_player:
            if self.__w_hitted > 0:
                if (action[0] == "reenter"):
                    self.__w_hitted = self.__w_hitted - 1
                    (self.__gameboard).update_reenter("w", action[1])
                if (action[0] == "reenter_hit"):
                    self.__w_hitted = self.__w_hitted - 1
                    self.__b_hitted = self.__b_hitted + 1
                    (self.__gameboard).update_reenterhit("w", action[1])
            else:  # elif self.__w_hitted == 0:
                if (action[0] == "move"):
                    (self.__gameboard).update_move("w", action[1], action[2])
                if (action[0] == "hit"):
                    self.__b_hitted = self.__b_hitted + 1
                    (self.__gameboard).update_hit("w", action[1], action[2])
                if (action[0] == "bearoff"):
                    (self.__gameboard).update_bearoff("w", action[1])
                    self.__w_bourne_off += 1

        if player == self.__b_player:
            if self.__b_hitted > 0:
                if (action[0] == "reenter"):
                    self.__b_hitted = self.__b_hitted - 1
                    (self.__gameboard).update_reenter("b", action[1])
                if (action[0] == "reenter_hit"):
                    self.__w_hitted = self.__w_hitted + 1
                    self.__b_hitted = self.__b_hitted - 1
                    (self.__gameboard).update_reenterhit("b", action[1])
            else:  # elif self.__w_hitted == 0:
                if (action[0] == "move"):
                    (self.__gameboard).update_move("b", action[1], action[2])
                if (action[0] == "hit"):
                    self.__w_hitted = self.__w_hitted + 1
                    (self.__gameboard).update_hit("b", action[1], action[2])
                if (action[0] == "bearoff"):
                    (self.__gameboard).update_bearoff("b", action[1])
                    self.__b_bourne_off += 1

    def get_actions(self, player, roll):
        """Given a tuple of dice rolls, return the set of possible moves.

        1) Move: move forward from one point to another, as long as the target
                 point is empty or having the same color as the source point.
        2) Hit: To move to a point occupied by an opposing blot and put the blot
                on the bar.
        3) Reenter: To move a checker from the bar to an open point in the
                    opponent's home board according to a roll of the dice. When
                    a player has a checker on the bar, this is his only legal
                    move.
        4) Bear off: To remove a checker from the board according to a roll of
                     the dice after all of your checkers have been brought into
                     your home board."""

        points = self.__gameboard.get_board()

        w_indices = []
        b_indices = []
        empty_indices = []
        for index, point in enumerate(points):
            if point.get_color() == 'w':
                w_indices.append(index)
            if point.get_color() == 'b':
                b_indices.append(index)
            else:
                empty_indices.append(index)

        w_home_board = max(w_indices) < 6
        b_home_board = min(b_indices) > 17
        if w_home_board and (self.__w_hitted == 0):
            self.__w_canbearoff = True
        if b_home_board and (self.__b_hitted == 0):
            self.__b_canbearoff = True

        actions = []
        rewards = []
        if player == self.__w_player:
            if self.__w_hitted > 0:
                if (24-roll) in empty_indices:
                    actions.append(('reenter', 24-roll))
                    rewards.append(roll)
                elif ((24-roll) in b_indices) and ((points[24-roll]).get_count() < 2):
                    actions.append(('reenter_hit', 24-roll))
                    rewards.append(24)
                return actions, rewards

            #  case (self.__w_hitted == 0):
            for index in w_indices:
                if (index-roll) in (w_indices + empty_indices):
                    actions.append(('move', index, index - roll))
                    rewards.append(roll)
                if ((index-roll) in b_indices) and ((points[index-roll]).get_count() < 2):
                    actions.append(('hit', index, index - roll))
                    rewards.append(roll+index)
                if (self.__w_canbearoff) and (index < roll):
                    actions.append(('bearoff', index))
                    rewards.append(index+1)
                return actions, rewards

            # Black Player
        if player == self.__b_player:
            if self.__b_hitted > 0:
                if (roll-1) in empty_indices:
                    actions.append(('reenter', roll-1))
                    rewards.append(roll)
                elif ((roll-1) in w_indices) and ((points[roll-1]).get_count() < 2):
                    actions.append(('reenter_hit', roll-1))
                    rewards.append(24)
                return actions, rewards

            #  case (self.__b_hitted == 0):
            for index in b_indices:
                if (index+roll) in (b_indices + empty_indices):
                    actions.append(('move', index, index + roll))
                    rewards.append(roll)
                if ((index+roll) in w_indices) and ((points[index+roll]).get_count() < 2):
                    actions.append(('hit', index, index + roll))
                    rewards.append(roll+24-index)
                if (self.__b_canbearoff) and ((23-index) < roll):
                    actions.append(('bearoff', index))
                    rewards.append(24-index)
                return actions, rewards

        return actions, rewards

    def get_board(self):
        return self.__gameboard.get_board()

    # TODO: what is the use of this?
    # def is_over(self, board):
    #     """Returns a tuple of which the first element is a boolean of the game
    #     being over or not and the second element is the winner."""

    #     i = 0
    #     for color in ['w', 'b']:
    #         for point in board.get_board():
    #             checkers = point.get_checkers()
    #             if checkers[0] == color:
    #                 i += point.checkers[1]
    #         if i < 1:
    #             return (True, self.get_player(color))

    #     return (False, None)

    def get_done(self):
        """Returns a tuple of which the first element is a boolean of the game
        being over or not and the second element is the winner."""

        points = self.__gameboard.get_board()
        i = 0
        for color in ['w', 'b']:
            for point in points:
                checkers = point.get_color()
                if checkers[0] == color:
                    i += point.get_count()
            if i < 1:
                return (True, self.get_player(color))

        return (False, None)

    # TODO: what is the use of this?
    # def get_reward(self, action, state=None):
    #     """Unnecessary as reward computed inside get_actions"""

    #     board = self.board if state is None else state

    #     # For player1
    #     before_pip_count1 = 0
    #     for index, point in enumerate(board):
    #         if point[0] == 1:
    #             before_pip_count1 += (point[1] * (24 - index))
    #     # For player2
    #     before_pip_count2 = 0
    #     for index, point in enumerate(board.flip(axis=0)):
    #         if point[0] == 2:
    #             before_pip_count2 += (point[1] * (24 - index))

    #     before = before_pip_count1 - before_pip_count2

    #     next_board = do_action(board, action)

    #     after_pip_count1 = 0
    #     for index, point in enumerate(next_board):
    #         if point[0] == 1:
    #             after_pip_count1 += (point[1] * (24 - index))
    #     # For player2
    #     after_pip_count2 = 0
    #     for index, point in enumerate(next_board.flip(axis=0)):
    #         if point[0] == 2:
    #             before_pip_count2 += (point[1] * (24 - index))

    #     after = after_pip_count1 - after_pip_count2

    #     return after - before

# TODO: Is this supposed to be a method of the game object? Otherwise,
# it cannot work!
###
# Code for Sarsa Training
# def train(agent_train, opponent, maxmove=1000, numgames=100000):
#     """Trains a sarsa agent (white player) against a given opponent."""

#     #pretraining = 10000
#     for i in range(numgames):
#         if i % 1000 == 0:
#             print("Training Game: " + str(i))

#         gamei = Game(agent_train, opponent)
#         num_move = 0
#         while (num_move<maxmove) and (not gamei.is_over()):
#             gamei.roll_dice()
#             curstate = gamei.get_state3(self.__dice[0])

#             possible_actions, their_rewards = gamei.get_actions(agent_train, self.__dice[0])
#             curaction, action_index = agent_train.chooseAction(curstate, possible_actions)
#             gamei.update_board(agent_train, curaction)
#             reward1 = their_rewards[action_index]
#             agent_train.learn(curstate, curaction, reward, nextstate, nextaction)

#             if not gamei.is_over():
#                 nextstate = gamei.get_state3(self.__dice[1])
#                 possible_actions, their_rewards = gamei.get_actions(agent_train, self.__dice[1])
#                 nextaction, action_index = agent_train.chooseAction(curstate, possible_actions)
#                 gamei.update_board(agent_train, nextaction)
#                 reward2 = their_rewards[action_index]
#                 agent_train.learn(curstate, curaction, reward1+reward2, nextstate, nextaction)

#             if not gamei.is_over():
#                 gamei.roll_dice()
#                 possible_actions, their_rewards = gamei.get_actions(opponent, self.__dice[0])
#                 oppaction, action_index = opponent.chooseAction(possible_actions)
#                 gamei.update_board(opponent, oppaction)
#                 possible_actions, their_rewards = gamei.get_actions(opponent, self.__dice[1])
#                 oppaction, action_index = opponent.chooseAction(possible_actions)
#                 gamei.update_board(opponent, oppaction)

#             if not gamei.is_over():
#                 gamei.roll_dice()
#                 nextstate = gamei.get_state()
#                 possible_actions = gamei.get_actions(agent_train, roll)
#                 nextaction = agent_train.chooseAction(nextstate, possible_actions)
#                 board.update(agent_train, nextaction)
#                 agent_train.learn(curstate, curaction, reward, nextstate, nextaction)
#             if not gamei.is_over():
#                 gamei.roll_dice()
#                 # opponent play
#                 board.update(opponent, oppaction)

#             # num_move++

#                 # if gamei.is_over():


#     return agent_train

# TODO: We need to use a library such as pickle to store our agents
# #SarsaPlayer = player("sarsa", False, )
# sarsa_player = Sarsa()
# player2 = RandomPlayer("Opponent", False)
# trained_agent = train(sarsa_player, player2, 1000, 100000)

# # write coeeficients (q values of trained agent) to a file

# myGame = Game(1, 2)
# print(myGame.get_state())
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
import math


def roll_dice():
    return [random.randint(1, 6), random.randint(1, 6)]


class Game:
    """Defines a backgammon game object."""

    def __init__(self, b_player=Player(policy='random'), higher_starts=True):
        self.__w_player = "w"
        self.__b_player = b_player
        self.__gameboard = Board()

        self.__w_bourne_off = 0
        self.__b_bourne_off = 0
        self.__w_hitted = 0
        self.__b_hitted = 0
        self.__w_canbearoff = False
        self.__b_canbearoff = False

        w_toss = roll_dice()
        b_toss = roll_dice()
        while sum(w_toss) == sum(b_toss):
            w_toss = roll_dice()
            b_toss = roll_dice()
        if higher_starts:
            if sum(w_toss) > sum(b_toss):
                self.__turn = 1
            else:
                self.__turn = 2
        else:
            if sum(w_toss) < sum(b_toss):
                self.__turn = 1
            else:
                self.__turn = 2

        if self.__turn == 2:
            self.play_opponent()
        else:
            self.__dice = roll_dice()

    def play_opponent(self):
        self.__dice = roll_dice()
        while self.__turn == 2:
            self.play(self.__b_player.play(
                self.get_observation(),
                self.get_actions(self.__b_player, self.__dice)))
            # TODO check if turn is over and mark turn accordingly. For now,
            # just play one dice.

        self.__turn == 1
        self.__dice = roll_dice()

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

    def get_done(self):
        """Returns a tuple of which the first element is a boolean of the game
        being over or not and the second element is the winner."""

        points = self.__gameboard.get_board()
        i = 0
        for color in ['w', 'b']:
            for point in points:
                checkers = point.get_count()
                if point.get_color() == color:
                    i += checkers
            if i < 1:
                return (True, self.get_player(color))

        return (False, None)

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

    def play(self, actionint):
        """Given a tuple of dice rolls, return the set of possible moves.

        1) Move: move forward from one point to another, as long as the target
                 point is empty or having the same color as the source point.
        2) Hit: To move to a point occupied by an opposing blot and put the blot
                on the bar.
        3) Reenter: To move a checker from the bar to an open point in the
                    opponent's home board according to a roll of the dice. When
                    a player has a checker on the bar, this is his only legal
                    move.
        4) Reenter_hit: To move a checker from the bar to an open point in the
                    opponent's home board according to a roll of the dice. When
                    a player has a checker on the bar, this is his only legal
                    move.
        5) Bear off: To remove a checker from the board according to a roll of
                     the dice after all of your checkers have been brought into
                     your home board."""

        print('THIS')
        print(actionint)
        playerid = 1+int(actionint/2880)
        remainder = actionint % 2880  # actionint-2880*(playerid-1)
        actionid = 1+int(remainder/576)
        sourcedest = remainder % 576
        sourceid = int(sourcedest/24)
        destid = sourcedest % 24

        invalid_action = True

        #action = str(actionint)
        if playerid == "1":  # player == self.__w_player:
            assert self.__turn == 1  # sanity check
            if self.__w_hitted > 0:
                if (actionid == 3):   # "reenter"):
                    self.__w_hitted = self.__w_hitted - 1
                    (self.__gameboard).update_reenter("w", sourceid)
                    invalid_action = False
                    reward = 24-sourceid
                if (actionid == 4):  # "reenter_hit"):
                    self.__w_hitted = self.__w_hitted - 1
                    self.__b_hitted = self.__b_hitted + 1
                    (self.__gameboard).update_reenterhit("w", sourceid)
                    invalid_action = False
                    reward = 24
            else:  # elif self.__w_hitted == 0:
                if (actionid == 1):  # "move"):
                    (self.__gameboard).update_move("w", sourceid, destid)
                    invalid_action = False
                    reward = sourceid-destid  # absolute value
                if (actionid == 2):  # "hit"):
                    self.__b_hitted = self.__b_hitted + 1
                    (self.__gameboard).update_hit("w", sourceid, destid)
                    invalid_action = False
                    reward = sourceid + 1
                if (actionid == 5):  # "bearoff"):
                    (self.__gameboard).update_bearoff("w", sourceid)
                    self.__w_bourne_off += 1
                    invalid_action = False
                    reward = sourceid + 1

        elif playerid == "2":  # player == self.__b_player:
            assert self.__turn == 2  # sanity check
            if self.__b_hitted > 0:
                if (actionid == 3):   # "reenter"):
                    self.__b_hitted = self.__b_hitted - 1
                    (self.__gameboard).update_reenter("b", sourceid)
                    invalid_action = False
                    reward = sourceid+1
                if (actionid == 4):  # "reenter_hit"):
                    self.__w_hitted = self.__w_hitted + 1
                    self.__b_hitted = self.__b_hitted - 1
                    (self.__gameboard).update_reenterhit("b", sourceid)
                    invalid_action = False
                    reward = 24
            else:  # elif self.__w_hitted == 0:
                if (actionid == 1):  # "move"):
                    (self.__gameboard).update_move("b", sourceid, destid)
                    invalid_action = False
                    reward = destid-sourceid  # absolute value
                if (actionid == 2):  # "hit"):
                    self.__w_hitted = self.__w_hitted + 1
                    (self.__gameboard).update_hit("b", sourceid, destid)
                    invalid_action = False
                    reward = 24-sourceid
                if (actionid == 5):  # "bearoff"):
                    (self.__gameboard).update_bearoff("b", sourceid)
                    self.__b_bourne_off += 1
                    invalid_action = False
                    reward = 24-sourceid

        if invalid_action == 1:
            reward = -1000
            all_actions = self.get_actions("w", self.__dice[0])
            action = random.choice(all_actions)
            print('NOWNOWTHIS')
            print(action)
            self.play(action)

        # TODO check if turn is over and mark turn accordingly. For now,
        # just play one dice.
        self.__turn == 2
        self.play_opponent()

        return reward, self.get_observation(), self.get_done()

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
        4) Reenter_hit: To move a checker from the bar to an open point in the
                    opponent's home board according to a roll of the dice. When
                    a player has a checker on the bar, this is his only legal
                    move.
        5) Bear off: To remove a checker from the board according to a roll of
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
        enumerate actions as a number: XABCDE  where X player type 1 for white 2 for black 
        A: action type BC source DE destination
        eg  1903911 means move from point 3 to point 11
        for reenter and reenterhit last 2 digits unimportant

        1) Move: move forward from one point to another, as long as the target
                 point is empty or having the same color as the source point.
        2) Hit: To move to a point occupied by an opposing blot and put the blot
                on the bar.
        3) Reenter: To move a checker from the bar to an open point in the
                    opponent's home board according to a roll of the dice. When
                    a player has a checker on the bar, this is his only legal
                    move.
        4) Reenter_hit: To remove a checker from the board according to a roll of
                     the dice after all of your checkers have been brought into
                     your home board.
        5) Bear off: To remove a checker from the board according to a roll of
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
        if player == "w":
            if self.__w_hitted > 0:
                if (24-roll) in empty_indices:
                    actionstr = 576*2 + (24-roll)*24
                    actions.append(actionstr)
                    #actions.append(('reenter', 24-roll))
                    rewards.append(roll)
                elif ((24-roll) in b_indices) and ((points[24-roll]).get_count() < 2):
                    actionstr = 576*3 + (24-roll)*24
                    actions.append(actionstr)
                    #actions.append(('reenter_hit', 24-roll))
                    rewards.append(24)
                return actions, rewards

            #  case (self.__w_hitted == 0):
            for index in w_indices:
                if (index-roll) in (w_indices + empty_indices):
                    actionstr = index*24 + (index-roll)
                    actions.append(actionstr)
                    #actions.append(('move', index, index - roll))
                    rewards.append(roll)
                if ((index-roll) in b_indices) and ((points[index-roll]).get_count() < 2):
                    actionstr = 576*1 + index*24 + (index-roll)
                    actions.append(actionstr)
                    #actions.append(('hit', index, index - roll))
                    rewards.append(roll+index)
                if (self.__w_canbearoff) and (index < roll):
                    actionstr = 576*4 + index*24
                    actions.append(actionstr)
                    #actions.append(('bearoff', index))
                    rewards.append(index+1)
                return actions, rewards

            # Black Player
        if player == "b":  # self.__b_player:
            if self.__b_hitted > 0:
                if (roll-1) in empty_indices:
                    actionstr = 2880 + 576*2 + (roll-1)*24
                    actions.append(actionstr)
                    #actions.append(('reenter', roll-1))
                    rewards.append(roll)
                elif ((roll-1) in w_indices) and ((points[roll-1]).get_count() < 2):
                    actionstr = 2880 + 576*3 + (roll-1)*24
                    actions.append(actionstr)
                    #actions.append(('reenter_hit', roll-1))
                    rewards.append(24)
                return actions, rewards

            #  case (self.__b_hitted == 0):
            for index in b_indices:
                if (index+roll) in (b_indices + empty_indices):
                    actionstr = 2880 + index*24 + (index+roll)
                    actions.append(actionstr)
                    #actions.append(('move', index, index + roll))
                    rewards.append(roll)
                if ((index+roll) in w_indices) and ((points[index+roll]).get_count() < 2):
                    actionstr = 2880 + 576*1 + index*24 + (index+roll)
                    actions.append(actionstr)
                    #actions.append(('hit', index, index + roll))
                    rewards.append(roll+24-index)
                if (self.__b_canbearoff) and ((23-index) < roll):
                    actionstr = 2880 + 576*4 + index*24
                    actions.append(actionstr)
                    #actions.append(('bearoff', index))
                    rewards.append(24-index)
                return actions, rewards

        return actions, rewards

    def get_actions2(self, player, roll):
        """Given a tuple of dice rolls, return the set of possible moves.
        enumerate actions as a number: XABCDE  where X player type 1 for white 2 for black 
        A: action type BC source DE destination
        eg  1903911 means move from point 3 to point 11
        for reenter and reenterhit last 2 digits unimportant

        1) Move: move forward from one point to another, as long as the target
                 point is empty or having the same color as the source point.
        2) Hit: To move to a point occupied by an opposing blot and put the blot
                on the bar.
        3) Reenter: To move a checker from the bar to an open point in the
                    opponent's home board according to a roll of the dice. When
                    a player has a checker on the bar, this is his only legal
                    move.
        4) Reenter_hit: To remove a checker from the board according to a roll of
                     the dice after all of your checkers have been brought into
                     your home board.
        5) Bear off: To remove a checker from the board according to a roll of
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
                    actionstr = 30000 + (24-roll)*100
                    actions.append(actionstr)
                    #actions.append(('reenter', 24-roll))
                    rewards.append(roll)
                elif ((24-roll) in b_indices) and ((points[24-roll]).get_count() < 2):
                    actionstr = 40000 + (24-roll)*100
                    actions.append(actionstr)
                    #actions.append(('reenter_hit', 24-roll))
                    rewards.append(24)
                return actions, rewards

            #  case (self.__w_hitted == 0):
            for index in w_indices:
                if (index-roll) in (w_indices + empty_indices):
                    actionstr = 10000 + index*100 + (index-roll)
                    actions.append(actionstr)
                    #actions.append(('move', index, index - roll))
                    rewards.append(roll)
                if ((index-roll) in b_indices) and ((points[index-roll]).get_count() < 2):
                    actionstr = 20000 + index*100 + (index-roll)
                    actions.append(actionstr)
                    #actions.append(('hit', index, index - roll))
                    rewards.append(roll+index)
                if (self.__w_canbearoff) and (index < roll):
                    actionstr = 50000 + index*100
                    actions.append(actionstr)
                    #actions.append(('bearoff', index))
                    rewards.append(index+1)
                return actions, rewards

            # Black Player
        if player == self.__b_player:
            if self.__b_hitted > 0:
                if (roll-1) in empty_indices:
                    actionstr = 30000 + (roll-1)*100
                    actions.append(actionstr)
                    #actions.append(('reenter', roll-1))
                    rewards.append(roll)
                elif ((roll-1) in w_indices) and ((points[roll-1]).get_count() < 2):
                    actionstr = 40000 + (roll-1)*100
                    actions.append(actionstr)
                    #actions.append(('reenter_hit', roll-1))
                    rewards.append(24)
                return actions, rewards

            #  case (self.__b_hitted == 0):
            for index in b_indices:
                if (index+roll) in (b_indices + empty_indices):
                    actionstr = 10000 + index*100 + (index+roll)
                    actions.append(actionstr)
                    #actions.append(('move', index, index + roll))
                    rewards.append(roll)
                if ((index+roll) in w_indices) and ((points[index+roll]).get_count() < 2):
                    actionstr = 20000 + index*100 + (index+roll)
                    actions.append(actionstr)
                    #actions.append(('hit', index, index + roll))
                    rewards.append(roll+24-index)
                if (self.__b_canbearoff) and ((23-index) < roll):
                    actionstr = 50000 + index*100
                    actions.append(actionstr)
                    #actions.append(('bearoff', index))
                    rewards.append(24-index)
                return actions, rewards

        return actions, rewards

    def print_observation(self):
        # point1 color, point1 count, point2 color, point2 count, . . . point24 color, point24 count]
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

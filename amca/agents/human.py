# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
    Amca: The RL-Based Backgammon Agent
    https://github.com/ardabbour/amca/

    Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu
    Cognitive Robotics Laboratory
    Faculty of Engineering and Natural Sciences
    Sabanci University

    The Human agent takes an action according to a human decision.
"""


class HumanAgent:
    def __init__(self):
        self.__actions = self.all_possible_actions()

    def make_decision(self, observation):
        """Returns the action that is closest to the predicted output."""

        self.print_observation(observation)
        # print('Available actions:')
        # acts = self.get_valid_actions(observation)
        # actints = [self.__actions.index(x) for x in acts]
        # for actint, act in actints, acts:
        #     print('{} - {}'.format(actint, act))

        # actint = int(input('Type action ID'))
        # while actint not in actints:
        #     print('Invalid action ID chosen')
        #     for actint, act in actints, acts:
        #         print('{} - {}'.format(actint, act))
        #     actint = int(input('Type action ID'))

        action_type = input(
            'enter action type {move,hit,reenter,reenter_hit,bearoff}')
        if action_type in ['move', 'hit']:
            source = int(input('input source {0,1,..,23}'))
            target = int(input('input target {0,1,..,23}'))
            action = (action_type, source, target)
        elif action_type in ['reenter', 'reenter_hit']:
            target = int(input('input target {0,1,..,23}'))
            action = (action_type, target)
        elif action_type == 'bearoff':
            source = int(input('input source {0,1,..,23}'))
            action = (action_type, source)

        actionint = self.__actions.index(action)

        return actionint

    def all_possible_actions(self):
        actions = []
        sources = list(range(0, 24))
        targets = list(range(0, 24))
        homes = list(range(0, 6)) + list(range(18, 24))

        # 'move's and 'hit's
        for i in sources:
            for j in targets:
                if (j - i) <= 6:
                    actions.append(('move', i, j))
                    actions.append(('move', j, i))
                    actions.append(('hit', i, j))
                    actions.append(('hit', j, i))

        # 'reenter's, 'reenter_hit's and 'bearoff's
        for j in homes:
            actions.append(('reenter', j))
            actions.append(('reenter_hit', j))
            actions.append(('bearoff', j))

        return actions

    # def get_valid_actions(self, observation):
    #     """Returns all the possible actions. Assumes the player is b player."""

    #     acts = []
    #     dice, b_hit, points = self.get_state_from_observation(observation)
    #     for roll in dice:
    #         w_indices = []
    #         b_indices = []
    #         empty_indices = []
    #         index = 0
    #         for point in points:
    #             if point.get_color() == 'w':
    #                 w_indices.append(index)
    #             elif point.get_color() == 'b':
    #                 b_indices.append(index)
    #             else:
    #                 empty_indices.append(index)
    #             index = index+1

    #         b_home_board = min(b_indices) > 17
    #         if b_home_board and (b_hit == 0):
    #             b_canbearoff = True

    #         actions = []

    #         if b_hit > 0:
    #             if (roll-1) in (empty_indices + b_indices):
    #                 actions.append(('reenter', roll-1))
    #             elif ((roll-1) in w_indices) and ((points[roll-1]).get_count() < 2):
    #                 actions.append(('reenter_hit', roll-1))

    #         else:
    #             for index in b_indices:
    #                 if (index+roll) in (b_indices + empty_indices):
    #                     actions.append(('move', index, index + roll))
    #                 if ((index+roll) in w_indices) and ((points[index+roll]).get_count() < 2):
    #                     actions.append(('hit', index, index + roll))
    #                 if (b_canbearoff) and ((23-index) < roll):
    #                     actions.append(('bearoff', index))

    #         acts.append(actions)

    #     return acts

    # def get_state_from_observation(self, observation):
    #     if 


    def print_observation(self, observation):
        max_picese_point = max(observation)
        observation = zip(observation[::2], observation[1::2])
        observation = list(observation)
        up_side = list()
        buttom_side = list()
        for i in range(3, int(3+(len(observation)-3)/2)):
            buttom_side.append(observation[i])
        for i in range(int(3+(len(observation)-3)/2), len(observation)):
            up_side.append(observation[i])
        buttom_side.reverse()
        board = list()
        board.append(
            '  -------------------------------------------------------------- ')
        board.append(
            ' |12  13  14  15   16   17   |    | 18   19   20   21   22   23  | ')
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
            ' |11  10   9   8    7    6    |    | 5    4    3    2    1    0  | ')
        board.append(
            '  --------------------------------------------------------------- ')
        board.append('Dice 1: {}'.format(observation[0][0]))
        board.append('Dice 2: {}'.format(observation[0][1]))
        board.append('White hitted: {}'.format(observation[1][0]))
        board.append('Black hitted: {}'.format(observation[1][1]))
        board.append('white bourne off: {}'.format(observation[2][0]))
        board.append('Black bourne off: {}'.format(observation[2][1]))

        for line in board:
            print(line)

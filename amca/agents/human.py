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
        pass

    def make_decision(self, observation):
        """Returns the action that is closest to the predicted output."""

        self.print_observation(observation)
        self.print_valid_actions(observation)  # TODO DEFINE THIS
        action = input('Type the index of the action you would like to take')

        return action

    # TODO
    def print_valid_actions(self, observation):
        """Takes an observation vector and represents only the valid actions
        available to the player."""

    def print_observation(self, observation):
        observation
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
        board.append('Dice 1: {}'.format(observation[0][0]))
        board.append('Dice 2: {}'.format(observation[0][1]))
        board.append('White hitted: {}'.format(observation[1][0]))
        board.append('Black hitted: {}'.format(observation[1][1]))
        board.append('white bourne off: {}'.format(observation[2][0]))
        board.append('Black bourne off: {}'.format(observation[2][1]))

        for line in board:
            print(line)
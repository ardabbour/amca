#!/usr/bin/env python3
"""
    Amca: The RL-Based Backgammon Agent
    https://github.com/ardabbour/amca/

    Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu
    Cognitive Robotics Laboratory
    Faculty of Engineering and Natural Sciences
    Sabanci University

    The backgammon board data structure is defined here. It is a list made of 24
    Points, a class that is also defined here. A point can have a maximum of 15
    checkers in it. A point has two properties:
    1) 'checker_color', which must be either 'w', 'b', or None
    2) 'checker_count', which is an integer ranging from 0 to 15
"""


class Board():
    """Defines a board."""

    def __init__(self):
        self.__board = [Point('b', 2), Point(), Point(),
                        Point(), Point(), Point('w', 5),
                        Point(), Point('w', 3), Point(),
                        Point(), Point(), Point('b', 5),
                        Point('w', 5), Point(), Point(),
                        Point(), Point('b', 3), Point(),
                        Point('b', 5), Point(), Point(),
                        Point(), Point(), Point('w', 2)]

        self.__hit = {'w': 0, 'b': 0}

    def get_board(self):
        """Returns the current board's status."""

        return self.__board

    def move(self, source_index, target_index):
        """Moves a single checker from a point to another."""

        # There are only 24 points on the board
        assert 0 < source_index < 23
        assert 0 < target_index < 23
        # The source must not be the same as the target
        assert source_index != target_index

        source = self.__board[source_index].get_checkers()
        target = self.__board[source_index].get_checkers()

        # The source must have a color and count
        assert (source[0] is not None) and (source[1] > 0)
        # The source checker color must not have a hit checker
        assert self.__hit[source[0]] == 0
        # The source checker cannot move into a point occupied by more than 1
        # of the opponent's checkers
        assert (source[0] == target[1]) or (target[1] == 0)

        # Move to empty point
        if (target[1] == 0):
            target.set_checkers(source[0], 1)

        # Move to point already occupied
        elif (source[0] == target[0]):
            target.set_checkers(source[0], target[1]+1)

        # Hit opposing player and move in its place
        elif (source[0] != target[0]) and (target[1] == 1):
            target.set_checkers(source[0], 1)
            self.__hit[target[0]] += 1

        # After moving, must remove checker from source
        self.__board[source_index].remove_checker()


class Point():
    """Defines a point, which is a division of the board."""

    def __init__(self, checker_color=None, checker_count=0):
        if checker_count is 0:
            assert checker_color is None  # Sanity check

        self.__checker_count = checker_count
        self.__checker_color = checker_color

    def get_checkers(self):
        """Returns the count and color of the checkers in the point."""

        return (self.__checker_color, self.__checker_count)

    def set_checkers(self, checker_color, checker_count):
        """Sets the checkers in the point."""

        self.__checker_count = checker_count
        self.__checker_color = checker_color
    
    def remove_checker(self):
        """Removes a single checker."""

        assert self.__checker_count > 0

        self.__checker_count -= 1
        if self.__checker_count == 0:
            self.__checker_color = None

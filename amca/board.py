# -*- coding: utf-8 -*-
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
    1) 'color', which must be either 'w', 'b', or None
    2) 'count', which is an integer ranging from 0 to 15
"""

import warnings


class Board:
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
        self.__bourne_off = {'w': 0, 'b': 0}

    ######################### GET/SET METHODS ########################
    def get_board(self):
        """Get method for the board."""

        return self.__board

    def set_board(self, board):
        """Set method for the board."""

        self.__board = board

    def get_hit(self):
        """Get method for the checkers hit."""

        return self.__hit

    def set_hit(self, hit):
        """Set method for the checkers hit."""

        self.__hit = hit

    def get_bourne_off(self):
        """Get method for the checkers bourne off."""

        return self.__hit

    def set_bourne_off(self, hit):
        """Set method for the checkers bourne off."""

        self.__hit = hit
    ######################### GET/SET METHODS ########################

    ############################ ACTIONS ############################
    def basic_validity(self, source_point_index, target_point_index=None):
        """Base sanity checks for all actions."""

        if not 0 <= source_point_index <= 23:
            raise ValueError('Source index is not within bounds.')
        if target_point_index is not None:
            if not 0 <= target_point_index <= 23:
                raise ValueError('Target index is not within bounds.')
            if not source_point_index != target_point_index:
                raise ValueError('Source and target indices are the same.')

        source = self.__board[source_point_index]
        if target_point_index is not None:
            target = self.__board[target_point_index]

        if source.get_count() < 1:
            raise ValueError('No checkers in source point.')
        if self.__hit[source.get_color()] > 0:
            raise ValueError('Cannot act while having a hit checker.')

        return True

    def move(self, source_point_index, target_point_index):
        """Moves a single checker from one point to another. This action is only
        valid for moving to an empty point or a point already occupied by the
        player."""

        if self.basic_validity(source_point_index, target_point_index):
            source = self.__board[source_point_index]
            target = self.__board[target_point_index]

        if target.get_color() not in [None, source.get_color()]:
            raise ValueError('Cannot move into a point occupied by opponent.')

        # Set empty point's color if applicable.
        if target.get_count() == 0:
            target.set_color(source.get_color())

        # Move checker from source point to target point.
        source.remove_checker()
        target.add_checker()

    def hit(self, source_point_index, target_point_index):
        """Hits an opponent's checker. This action is only valid for hitting an
        opponent checker that is alone in a point."""

        if self.basic_validity(source_point_index, target_point_index):
            source = self.__board[source_point_index]
            target = self.__board[target_point_index]

        if source.get_color() == target.get_color():
            raise ValueError('Cannot hit self.')

        if target.get_color() is None:
            raise ValueError('Cannot hit an empty point.')

        if target.get_count() > 1:
            raise ValueError('Cannot hit more than a single checker.')

        target.remove_checker()
        self.__hit[target.get_color()] += 1
        source.remove_checker()
        target.add_checker()

    def bear_off(self, source_point_index):
        """Bears a checker off the board."""

        if self.basic_validity(source_point_index):
            source = self.__board[source_point_index]

        count = 0
        if source.get_color() == 'w':
            for i in range(6, 24):
                count += self.__board[i].get_count()
        else:
            for i in range(18, -1):
                count += self.__board[i].get_count()
        if count > 0:
            raise ValueError(
                'Cannot bear off; not all checkers in home board.')

        source.remove_checker()
        self.__bourne_off[source.get_color()] += 1

    #TODO
    def reenter(self, color, target_point_index):

        if self.__hit[color] < 1:
            raise ValueError('Cannot reenter; no checkers on bar.')

        target = self.__board[target_point_index]

        if target.get_color() not in [None, color]:
            raise ValueError('Cannot move into a point occupied by opponent.')


    ############################ ACTIONS ############################


class Point:
    """Defines a point, which is a division of the board."""

    def __init__(self, color=None, count=0):
        if count is 0:
            assert color is None

        self.__count = count
        self.__color = color

    def get_count(self):
        """Gets the number of checkers in the point."""

        return self.__count

    def set_count(self, count):
        """Sets the number of checkers in the point."""

        warnings.warn('Setting count of point directly. Convention is to use\
        add or remove method of point.')

        self.__count = count

    def get_color(self):
        """Gets the color of the checkers in the point."""

        return self.__color

    def set_color(self, color):
        """Sets the color of the checkers in the point."""

        self.__color = color

    def add_checker(self):
        """Adds a single checker."""

        if self.__color is None:
            warnings.warn('Adding checker to colorless point. Convention is to\
            add checker after setting the color.')

        self.__count += 1

    def remove_checker(self):
        """Removes a single checker."""

        assert self.__count > 0

        self.__count -= 1
        if self.__count == 0:
            self.__color = None

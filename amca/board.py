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

        #self.__whome = [0,1,2,3,4,5]
        #self.__bhome = [18,19,20,21,22,23]

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
            # TODO What is the point of this?
            target = self.__board[target_point_index]

        if source.get_count() < 1:
            raise ValueError('No checkers in source point.')
        if self.__hit[source.get_color()] > 0:
            raise ValueError('Cannot act while having a hit checker.')

        return True

    def update_move(self, color, source_point_index, target_point_index):
        """Moves a single checker from one point to another. This action is only
        valid for moving to an empty point or a point already occupied by the
        player."""

        source = self.__board[source_point_index]
        target = self.__board[target_point_index]

        if target.get_count() == 0:
            target.add_firstchecker(color)
        else:
            target.add_checker()

        source.remove_checker()

    def update_hit(self, color, source_point_index, target_point_index):
        """Hits an opponent's checker. This action is only valid for hitting an
        opponent checker that is alone in a point."""

        source = self.__board[source_point_index]
        target = self.__board[target_point_index]

        source.remove_checker()
        target.add_firstchecker(color)

    def update_bearoff(self, color, source_point_index):
        """Bears a checker off the board."""

        source = self.__board[source_point_index]

        source.remove_checker()

    def update_reenter(self, color, target_index):

        target = self.__board[target_index]

        if target.get_count() == 0:
            target.add_firstchecker(color)
        else:
            target.add_checker()

    def update_reenterhit(self, color, target_index):

        target = self.__board[target_index]

        target.add_firstchecker(color)

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

    def add_firstchecker(self, colorx):
        """Adds first checker to the point"""

        self.__color = colorx
        self.__count = 1

    def remove_checker(self):
        """Removes a single checker."""

        assert self.__count > 0

        self.__count -= 1
        if self.__count == 0:
            self.__color = None

# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import gym
from gym import error, spaces, utils
from gym.utils import seeding

from amca.board import Board


# TODO
def board_to_state(board):
    return 1

# TODO
def state_to_board(state):
    return 1


class BackgammonEnv(gym.Env):
    """Defines a Backgammon environment to run the RL algorithm in.

    The action space has the following structure:
    {'type': [move/hit/bear_off/reenter INT],
     'source': [source index of the checker INT],
     'target': [target index for the checker INT]}.

    The observation space has the following structure:
    {'point01': ([free/white/black INT], [free/checkers count INT]),
     'point02': ([free/white/black INT], [free/checkers count INT]),
     .
     .
     .

     'point24': ([free/white/black INT], [free/checkers count INT]),
     }
     """

    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.__board = Board()
        self.__state = board_to_state(self.__board)
        self.action_space = spaces.Dict({'type': spaces.Discrete(4),
                                         'source': spaces.Discrete(24),
                                         'target': spaces.Discrete(24)})
        self.observation_space = spaces.Dict({
            'point01': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point02': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point03': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point04': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point05': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point06': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point07': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point08': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point09': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point10': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point11': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point12': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point13': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point14': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point15': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point16': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point17': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point18': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point19': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point20': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point21': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point22': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point23': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16))),
            'point24': spaces.Tuple((spaces.Discrete(3), spaces.Discrete(16)))})

    def step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.Accepts an action and returns a tuple
        (state, reward, done, info).
        Args:
            action (object): an action provided by the environment
        Returns:
            state (object): state of the current environment
            reward (float) : amount of reward returned after previous action
            done (boolean): whether the episode has ended, in which case further
            step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for
            debugging, and sometimes learning)
        """

        state = self.get_state()
        reward = self.get_reward()
        done = self.get_done()
        info = self.get_info()

        return (state, reward, done, info)

    def reset(self):
        """Resets then returns the state."""
        pass

    # TODO
    def render(self):
        """Represent the state in the terminal."""
        return

    def get_state(self):
        """Returns the state of the environment, that is the board."""

        return self.__board

    # TODO
    def get_reward(self, state=None):
        if state is None:
            state = self.__board
        return 1

    # TODO
    def get_done(self):
        return 1

    # TODO
    def get_info(self):
        return 1

# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
    Amca: The RL-Based Backgammon Agent
    https://github.com/ardabbour/amca/

    Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu
    Cognitive Robotics Laboratory
    Faculty of Engineering and Natural Sciences
    Sabanci University

    The Simple agent uses a basic DNN model to take an action. Can be trained.
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras


class SimpleAgent:
    def __init__(self, model):
        self.__model = model
        self.__action_history = []

    def act(self, observation, valid_actions):
        """Returns the action that is closest to the predicted output."""

        prediction = self.__model.predict(observation)

        return min(valid_actions, key=lambda x:abs(x-prediction))

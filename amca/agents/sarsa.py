# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
    Amca: The RL-Based Backgammon Agent
    https://github.com/ardabbour/amca/

    Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu
    Cognitive Robotics Laboratory
    Faculty of Engineering and Natural Sciences
    Sabanci University

    This script defines the sarsa algorithm. Modified significantly from
    https://github.com/vmayoral/basic_reinforcement_learning/blob/master/tutorial2/sarsa.py
"""

import random


class SarsaAgent:
    def __init__(self, actions=None, epsilon=0.2, alpha=0.2, gamma=0.9):
        self.q = {}

        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        if actions is None:
            self.actions = {}
        else:
            self.actions = actions

    def getQ(self, state, action):
        return self.q.get((state, action), 0.0)

    def learnQ(self, state, action, reward, value):
        oldv = self.q.get((state, action), None)
        if oldv is None:
            self.q[(state, action)] = reward
        else:
            self.q[(state, action)] = oldv + self.alpha * (value - oldv)

    def chooseAction(self, state, actions):
        if len(actions) < 1:
            actions = [("Nomove", 0, 0)]
            return ("Nomove", 0, 0), 0
        if random.random() < self.epsilon:
            i = random.choice(range(0, len(actions)))
        else:
            q = [self.getQ(state, a) for a in actions]
            if len(q) > 0:
                maxQ = max(q)
                count = q.count(maxQ)
            else:
                count = 0
                #maxQ = random.choice(range(0,len))
            if count >= 1:
                best = [i for i in range(len(actions)) if q[i] == maxQ]
                i = random.choice(best)
            else:
                i = random.choice(range(0, len(actions)))

        action = actions[i]
        return action, i

    def playAction(self, state, actions):
        if len(actions) < 1:
            actions = [("Nomove", 0, 0)]
            return ("Nomove", 0, 0)

        q = [self.getQ(state, a) for a in actions]

        if len(q) > 0:
            maxQ = max(q)
            count = q.count(maxQ)
        else:
            count = 0
        if count >= 1:
            best = [i for i in range(len(actions)) if q[i] == maxQ]
            i = random.choice(best)
        else:
            i = random.choice(range(0, len(actions)))

        action = actions[i]
        return action

    def learn(self, state1, action1, reward, state2, action2):
        qnext = self.getQ(state2, action2)
        self.learnQ(state1, action1, reward, reward + self.gamma * qnext)

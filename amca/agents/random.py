import random

# Modified significantly from
#  https://github.com/vmayoral/basic_reinforcement_learning/blob/master/tutorial2/sarsa.py

class RandomAgent:
    def __init__(self, name):

        self.name = name

    def chooseAction(self, actions):
        action = random.choice(actions)
        return action



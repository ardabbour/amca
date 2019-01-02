import random

# Modified significantly from
#  https://github.com/vmayoral/basic_reinforcement_learning/blob/master/tutorial2/sarsa.py

class SarsaBG:
    def __init__(self, actions=None, epsilon=0.2, alpha=0.2, gamma=0.9):
        self.q = {}

        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.actions = {}
        #self.actions = actions

    def getQ(self, state, action):
        return self.q.get((state, action), 0.0)

    def learnQ(self, state, action, reward, value):
        oldv = self.q.get((state, action), None)
        if oldv is None:
            self.q[(state, action)] = reward 
        else:
            self.q[(state, action)] = oldv + self.alpha * (value - oldv)

    def chooseAction(self, state, actions):
        if random.random() < self.epsilon:
            action = random.choice(actions)
        else:
            q = [self.getQ(state, a) for a in actions]
            maxQ = max(q)
            count = q.count(maxQ)
            if count > 1:
                best = [i for i in range(len(actions)) if q[i] == maxQ]
                i = random.choice(best)
            else:
                i = q.index(maxQ)

            action = actions[i]
        return action, i

    def learn(self, state1, action1, reward, state2, action2):
        qnext = self.getQ(state2, action2)
        self.learnQ(state1, action1, reward, reward + self.gamma * qnext)


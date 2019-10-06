import numpy as np
from agents.agent import Agent


class QLearningAgent(Agent):
    def __init__(self, actions, epsilon=0.1, alpha=0.85, gamma=0.9):
        super(QLearningAgent, self).__init__(actions)
        self.Q = {}
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def get_q(self, state, action):
        return self.Q.get((state, action), 0.0)

    def get_q_max(self, state):
        q = [self.get_q(state, a) for a in self.actions]
        max_q = max(q)
        return max_q, q.index(max_q)

    def act(self, obs):
        if np.random.random() < self.epsilon:
            return np.random.choice(self.actions, 1)[0]

        q_max = self.get_q_max(obs)
        if q_max[0] <= 0:
            return np.random.choice(self.actions, 1)[0]

        return self.actions[q_max[1]]

    def feedback(self, state_before, state_after, action, reward):
        q_next = self.get_q_max(state_after)
        old_v = self.Q.get((state_before, action), 0.0)
        self.Q[(state_before, action)] = old_v + self.alpha * (reward + self.gamma * q_next[0] - old_v)

    def __str__(self):
        return str(self.Q)


from enum import Enum


class AgentType(Enum):
    RANDOM = 1
    GREEDY = 2
    ROUND_ROBIN = 3
    EPSILON_GREEDY = 4
    UCB = 5
    THOMPSON_BETA = 6
    SARSA = 7
    QLEARNING = 8
    LFAQLEARNING = 9


class Agent(object):

    def __init__(self, actions):
        self.actions = actions
        self.num_actions = len(actions)

    def act(self, obs):
        raise NotImplementedError

    def feedback(self, state_before, state_after, action, reward):
        pass

# snakeQL
This is an implementation of Snake game with application of Artificial Intelligence (in particular Reinforcement Learning) written using Python.  
Game itself was written on my own using nothing more than Python, NumPy and PyGame.

## Snake
Snake is a game in which the player moves snake trying to eat as much fruits as possible without hitting walls or any part of snake's body.
Every time snake eats fruit it's size increase and score goes up.  

## Reinforcement Learning
Reinforcement Learning is a learning paradigm. Basically it is all about figuring out what kind of actions to take in order to perform the best in given environment.

## Algorithm
I've used Q-Learning as an algorithm for agent playing the game. The most important part of that algorithm is Q-table in which all the information about actions is stored.
  
### Parameters  
Algorithm has a few parameters:
1. alpha - which stands for learning rate (it scales the change in value)
2. epsilon - [0, 1] for 0 agent will never take random action while for 1 it will always be randomly chosen
3. gamma - which is a discount factor scaling maximal Q-value of a new state

### Actions  
Taking actions requires getting information from environment. It consist of nothing more than a current state of the game.  
I've decided to use 4 values: (x,y) for distance between snake's head and fruit, and (x,y) for distance between head and tail.  
And for actions there are 4 possible values: UP, DOWN, LEFT, RIGHT.  
  
Decision process goes like that:
1. if random number is lesser than epsilon choose random action
2. try to get q-value for current state (0 if no information available)
3. if q-value for state is zero or less choose random action
4. otherwise take the best action

### Rewards
Snake gets 1000.0 as a reward for hitting the fruit.  
Snake gets -1.0 as a reward for hitting either it's body or walls.  
Otherwise it get's reward calculated using this formula:
```python
640.0 / math.sqrt((self.snake.x[0] - self.apple.x) ** 2 +
                                           (self.snake.y[0] - self.apple.y) ** 2)
```
It is meant to motivate snake to get closer and closer to fruit as it is getting higher and higher nearby fruit.

### Learning
After every single action taken agent receives a feedback containing state before and after taking action, action taken and a reward.  
First of all agent figures out max q-value for a after state (q_next) and old q-value for a before state and action (old_v).  
Then it recalculates the q-value using given formula:
```python
self.Q[(state_before, action)] = old_v + self.alpha * (reward + self.gamma * q_next[0] - old_v)
```

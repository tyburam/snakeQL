#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math

import pygame
from pygame.locals import *
import numpy as np

from agents.q_learning_agent import QLearningAgent
from sprites.apple import Apple
from sprites.snake import Snake, SNAKE_MOVES_LEFT, SNAKE_MOVES_UP, SNAKE_MOVES_RIGHT, SNAKE_MOVES_DOWN


class Game:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.snake = None
        self.apple = None
        self.agent = QLearningAgent([SNAKE_MOVES_LEFT, SNAKE_MOVES_UP, SNAKE_MOVES_RIGHT, SNAKE_MOVES_DOWN])
        self.scores = 0
        self.died = 0
        self.record = 0

    def failed(self):
        self._running = False
        self.start()

    def start(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((320, 320), pygame.HWSURFACE)
        pygame.display.set_caption('snakeQL')
        self.init_gameplay()
        clock = pygame.time.Clock()

        while self._running:
            pygame.event.pump()
            pygame.display.set_caption('snakeQL Died = {}. Pts = {}. Max = {} '.format(self.died, self.scores,
                                                                                       self.record))

            for event in pygame.event.get():
                # works until windows is closed or ESC is pressed
                self._running = not ((event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT)
                if not self._running:
                    break

            current_state = self.get_state()
            action_taken = self.agent.act(current_state)
            self.snake.move(action_taken)

            if (self.snake.x[0] <= 0 or self.snake.x[0] >= 10 or self.snake.y[0] <= -1 or self.snake.y[0] >= 10)\
                    or self.snake.hist_its_tail():
                self.died += 1
                self._running = False
                self.agent.feedback(current_state, self.get_state(), action_taken, -1.0)
                self.init_gameplay()
                continue

            if self.snake.hits_apple(self.apple.x, self.apple.y):
                self.apple.move()
                self.scores += 1
                if self.scores > self.record:
                    self.record = self.scores
                self.agent.feedback(current_state, self.get_state(), action_taken, 1000.0)
            else:
                reward = 640.0 / math.sqrt((self.snake.x[0] - self.apple.x) ** 2 +
                                           (self.snake.y[0] - self.apple.y) ** 2)
                self.agent.feedback(current_state, self.get_state(), action_taken, reward)

            self._display_surf.fill((0, 0, 0))
            self.apple.draw(self._display_surf)
            self.snake.draw(self._display_surf)
            pygame.display.flip()

            clock.tick(10)
        pygame.quit()

    def init_gameplay(self):
        self.snake = Snake(pygame.image.load("sprites/assets/snake.png").convert())
        self.apple = Apple(pygame.image.load("sprites/assets/apple.png").convert(), 5, 5)
        self._running = True
        self.scores = 0

    def get_state(self):
        tail = self.snake.tail()
        return '{},{};{},{}'.format(self.snake.x[0] - self.apple.x, self.snake.y[0] - self.apple.y,
                                    self.snake.x[0] - tail.x, self.snake.y[0] - tail.y)


if __name__ == "__main__":
    np.random.seed(2019)
    game = Game()
    game.start()

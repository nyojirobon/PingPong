# -*- coding: utf-8 -*-

import numpy as np

class Environment:
    """
    Virtual environment of ping pong for learning.
    """

    def __init__(self):
        self.field_width = 600
        self.field_height = 400
        self.ball_radius = 10
        self.paddle_width = 80
        self.paddle_height = 10
        self.done = false # flag for if game is over
        self.ball_x = self.field_width/2 # ball position(x-coordinate)
        self.ball_y = self.field_height/2 # ball position(y-coordinate)
        self.ball_dx = 3 # ball moving speed(x-axis)
        self.ball_dy = -3 # ball moving speed(y-axis)
        self.paddle_x = (self.field_width - self.paddleWidth)/2 # agent's paddle position(x-coordinate)
        self.opponent_paddle_x = (self.field_width - self.paddleWidth)/2 # opponet's paddle position(x-coordinate)

    def get_reward(self):
        """
        Calculate ball position and decide immediate reward by the result.

        # Returns:
            reward(float) : immediate reward for current step
        """
        if self.ball_x + self.ball_dx > self.field_width - self.ball_radius or \
        self.ball_x + self.ball_dx < self.ball_radius:
            self.ball_dx -= self.ball_dx

        if self.ball_y + self.ball_dy > self.field_height - self.ball_radius:
            if self.ball_x + self.ball_radius > self.opponent_paddle_x and \
            self.ball_x - self.ball_radius < self.opponent_paddle_x + self.paddle_width:
                self.ball_dy -= self.ball_dy
                return 1.0
            else: # Win the game
                self.done = true
                return 100.0
        elif self.ball_y + self.ball_dy < self.ball_radius:
            if self.ball_x + self.ball_radius > self.paddle_x and \
            self.ball_x - self.ball_radius < self.paddle_x + self.paddle_width:
                self.ball_dy -= self.ball_dy
                return 1.0
            else: # Lose the game
                self.done = true
                return -100.0
        else:
            return 1.0

    def move_paddle(self, current_pos, direction):
        """
        Move paddle toward given direction.

        # Arguments
            current_pos(Integer) : current x-coordinate of paddle
            direction(Integer) : direction of paddle movement(0:stay, 1:left, 2:right)
        """
        if direction == 1: # move to left
            if current_pos - 10 >= 0:
                return current_pos - 10
            else:
                return 0
        elif direction == 2: # move to right
            if current_pos + 10 <= self.field_width - self.paddle_width:
                return current_pos + 10
            else:
                return self.field_width - self.paddle_width
        else: # stay at current position
            return current_pos

    def step(self, direction):
        """
        Run one timestep of the environment's dynamics.

        # Arguments
            direction(Integer) : direction of paddle movement(0:stay, 1:left, 2:right)

        # Returns:
            observation(object) : observation of the environment from agent
            reward(float) : immediate reward for current step
            done(boolean) : whether the current game has ended
        """
        if self.done:
            raise Exception("The game has already ended, should call 'reset()'")

        reward = self.get_reward()
        self.paddle_x = self.move_paddle(self.paddle_x, direction)
        self.opponent_paddle_x = self.move_paddle(self.opponent_paddle_x, np.random.randint(3))
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        observation = (self.paddle_x, self.opponent_paddle_x, self.ball_x, self.ball_y)
        return (observation, reward, self.done)

    def reset(self):
        """
        Reset state of the environment and return initial observation.

        # Returns:
            observation(object) : initial observation
        """
        self.done = false
        self.ball_x = self.field_width/2
        self.ball_y = self.field_height/2
        self.ball_dx = 3
        self.ball_dy = -3
        self.paddle_x = (self.field_width - self.paddleWidth)/2
        self.opponent_paddle_x = (self.field_width - self.paddleWidth)/2
        return (self.paddle_x, self.opponent_paddle_x, self.ball_x, self.ball_y)

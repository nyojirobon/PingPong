# -*- coding: utf-8 -*-

import numpy as np

class Environment:
    """
    Virtual environment of ping pong for learning.
    'done' is not defined, because if one lost of rally means lost of the game,
    learning is not going well.
    Thus, agent should set maximum timesteps for each episode.
    """

    # 0:stay, 1:left, 2:right
    action_space = np.array([0,1,2])

    def __init__(self):
        self.field_width = 600
        self.field_height = 400
        self.ball_radius = 10
        self.paddle_width = 100
        self.paddle_height = 10
        self.ball_x = self.field_width/2 # ball position(x-coordinate)
        self.ball_y = self.field_height/2 # ball position(y-coordinate)
        self.ball_dx = np.random.choice([3, -3]) # ball moving speed(x-axis)
        self.ball_dy = np.random.choice([3, -3]) # ball moving speed(y-axis)
        self.paddle_x = (self.field_width - self.paddle_width)/2 # agent's paddle position(x-coordinate)

    def get_reward(self):
        """
        Calculate ball position and decide immediate reward by the result.

        # Returns:
            reward(float) : immediate reward for current step
        """
        if self.ball_x + self.ball_dx > self.field_width - self.ball_radius or \
        self.ball_x + self.ball_dx < self.ball_radius:
            self.ball_dx = -self.ball_dx

        if self.ball_y + self.ball_dy < self.ball_radius:
            if self.ball_x + self.ball_radius > self.paddle_x and \
            self.ball_x - self.ball_radius < self.paddle_x + self.paddle_width:
                self.ball_dy = -self.ball_dy
                self.ball_dy = self.ball_dy+0.3 if self.ball_dy > 0 else self.ball_dy-0.3
                self.ball_dx = self.ball_dx+0.3 if self.ball_dx > 0 else self.ball_dx-0.3
                return 1.0
            else: # Lose this rally
                self.ball_dy = -self.ball_dy
                return -200.0
        elif self.ball_y + self.ball_dy > self.field_height - self.ball_radius:
            self.ball_dy = -self.ball_dy
            self.ball_dy = self.ball_dy+0.3 if self.ball_dy > 0 else self.ball_dy-0.3
            self.ball_dx = self.ball_dx+0.3 if self.ball_dx > 0 else self.ball_dx-0.3
            return 1.0
        else:
            self.ball_dy = self.ball_dy-0.001 if self.ball_dy > 0 else self.ball_dy+0.001
            self.ball_dx = self.ball_dx-0.001 if self.ball_dx > 0 else self.ball_dx+0.001
            return 1.0

    def move_paddle(self, direction):
        """
        Move paddle toward given direction.

        # Arguments
            direction(int) : direction of paddle movement
        """
        if direction == 1: # move to left
            if self.paddle_x - 10 > 0:
                self.paddle_x -= 10
            else:
                self.paddle_x =  0
        elif direction == 2: # move to right
            if self.paddle_x + 10 < self.field_width - self.paddle_width:
                self.paddle_x += 10
            else:
                self.paddle_x = self.field_width - self.paddle_width

    def step(self, direction):
        """
        Run one timestep of the environment's dynamics.

        # Arguments
            direction(int) : direction of paddle movement

        # Returns:
            observation(object) : observation of the environment from agent
            reward(float) : immediate reward for current step
        """
        self.move_paddle(direction)
        reward = self.get_reward()
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        observation = (self.paddle_x, self.ball_x, self.ball_y, self.ball_dx, self.ball_dy)
        return (observation, reward)

    def reset(self):
        """
        Reset state of the environment and return initial observation.

        # Returns:
            observation(object) : initial observation
        """
        self.ball_x = self.field_width/2
        self.ball_y = self.field_height/2
        self.ball_dx = np.random.choice([3, -3])
        self.ball_dy = np.random.choice([3, -3])
        self.paddle_x = (self.field_width - self.paddle_width)/2
        return (self.paddle_x, self.ball_x, self.ball_y, self.ball_dx, self.ball_dy)

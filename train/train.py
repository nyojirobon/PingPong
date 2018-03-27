# -*- coding: utf-8 -*-

import numpy as np
import os
from environment import Environment

def normalise_state(observation):
    """
    Normalise each element of state.

    # Arguments
        observation(object) : current observation of the environment from agent

    # Returns
        state(int) : state normalised in each element
    """
    paddle_pos, ball_x, ball_y, ball_dx, ball_dy = observation
    normalised_state = [
        np.digitize(paddle_pos, bins = np.linspace(0, 500, normalise_num + 1)[1:-1]),
        np.digitize(ball_x, bins = np.linspace(0, 600, normalise_num + 1)[1:-1]),
        np.digitize(ball_y, bins = np.linspace(0, 400, normalise_num + 1)[1:-1]),
        np.digitize(ball_dx, bins = np.linspace(-6, 6, normalise_num + 1)[1:-1]),
        np.digitize(ball_dy, bins = np.linspace(-6, 6, normalise_num + 1)[1:-1])
    ]
    return sum([x * (normalise_num**i) for i, x in enumerate(normalised_state)])

def get_action(action_space, state, episode):
    """
    Choose action in given state by 'decaying ε-greedy' policy.

    # Arguments
        action_space(numpy.ndarray) : choosable actions
        state(int) : current state
        episode() : number of current episode

    # Returns
        action(int) : action to take in current state
    """
    epsilon = 0.5 * (0.99 ** episode)
    if epsilon <= np.random.uniform(0, 1):
        action = np.argmax(q_table[state]) # choose best action
    else:
        action = np.random.choice(action_space) # choose random action
    return action

def update_qtable(q_table, state, action, reward, next_state):
    """
    Update Q-table.

    # Arguments
        q_table(numpy.ndarray) : current Q-table
        state(int) : current state
        action(int) : action to take in current state
        reward(float) : immediate reward of this timestep
        next_state(int) : next state

    # Returns
        q_table(numpy.ndarray) : updated Q-table
    """
    discount_factor = 0.99 # discount future reward
    learning_rate = 0.3
    next_max_Q = max(q_table[next_state][0], q_table[next_state][1], q_table[next_state][2])
    q_table[state][action] = (1 - learning_rate) * q_table[state][action] +\
     learning_rate * (reward + discount_factor * next_max_Q)
    return q_table

# Main Operation
env = Environment()
max_number_of_steps = 3000 # maximum number of steps per episode
num_episodes = 2000
normalise_num = 10 # separate each element of state into 10
q_table = np.random.uniform(low= -1, high= 1, size= (normalise_num**5, env.action_space.size))# create Q table

for episode in range(num_episodes):
    observation = env.reset()
    state = normalise_state(observation)
    action = np.argmax(q_table[state])
    episode_reward = 0

    for t in range(max_number_of_steps):
        # Take one timestep in the environment
        observation, reward = env.step(action)
        episode_reward += reward
        next_state = normalise_state(observation)

        q_table = update_qtable(q_table, state, action, reward, next_state)# update Q table
        action = get_action(env.action_space, next_state, episode)
        state = next_state

    print("In %dth episode, episode reward is %f." % (episode, episode_reward))

# Save Q table
pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
q_table_path = os.path.join(pardir, "predict", "qtable.csv")
np.savetxt(q_table_path, q_table, delimiter=",")

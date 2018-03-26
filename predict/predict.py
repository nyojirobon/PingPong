# -*- coding: utf-8 -*-

import numpy as np
import sys
import warnings

def normalise_state(observation):
    """
    Normalise each element of state.

    # Arguments
        observation(object) : current observation of the environment from agent
        normalise_num(int) :

    # Returns
        normalised state(int) : state normalised in each element
    """
    paddle_pos, ball_x, ball_y, ball_dx, ball_dy = observation
    normalised_state = [
        np.digitize(paddle_pos, bins = np.linspace(0, 540, normalise_num + 1)[1:-1]),
        np.digitize(ball_x, bins = np.linspace(0, 600, normalise_num + 1)[1:-1]),
        np.digitize(ball_y, bins = np.linspace(0, 400, normalise_num + 1)[1:-1]),
        np.digitize(ball_dx, bins = np.linspace(-5, 5, normalise_num + 1)[1:-1]),
        np.digitize(ball_dy, bins = np.linspace(-5, 5, normalise_num + 1)[1:-1])
    ]
    return sum([x * (normalise_num**i) for i, x in enumerate(normalised_state)])

with warnings.catch_warnings():
    warnings.filterwarnings("error") # consider warnings as errors
    try:
        args = sys.argv[1:]
        observation = [int(x) for x in args]
        normalise_num = 10
        state = normalise_state(observation)
        q_table = np.loadtxt("qtable.csv", delimiter=",")
        action = np.argmax(q_table[state])
        print(action)
    except ValueError:
        sys.stderr.write("Args should be list of integer.")
        print(-1)
    except FileNotFoundError:
        sys.stderr.write("Learned-Qtable is not found.")
        print(-1)
    except UserWarning:
        sys.stderr.write("Learned-Qtable is empty.")
        print(-1)
    except IOError:
        sys.stderr.write("Failed to load Learned-Qtable.")
        print(-1)
    except Exception as e:
        sys.stderr.write("Unexpected error: {0}".format(e))
        print(-1)

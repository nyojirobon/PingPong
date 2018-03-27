# -*- coding: utf-8 -*-

import numpy as np
import os
import sys
import warnings

class Predict:
    """
    Predict the best action in the current state by using pre-learned Q-table.
    """

    def __init__(self):
        self.q_table = self.load_qtable()

    def load_qtable(self):
        """
        Load learned Q-table.

        # Returns
            q_table(numpy.ndarray) : learned Q-table
        """
        with warnings.catch_warnings():
            warnings.filterwarnings("error") # consider warnings as errors
            try:
                pardir = os.path.dirname(os.path.abspath(__file__))
                q_table_path = os.path.join(pardir, "qtable.csv")
                return np.loadtxt(q_table_path, delimiter=",")
            except UserWarning as e:
                sys.stderr.write("Learned-Qtable is empty: {0}".format(e))
                sys.exit(1)
            except IOError as e:
                sys.stderr.write("Failed to load Learned-Qtable: {0}".format(e))
                sys.exit(1)
            except Exception as e:
                sys.stderr.write("Unexpected error: {0}".format(e))
                sys.exit(1)

    def normalise_state(self, observation, normalise_num):
        """
        Normalise each element of state.

        # Arguments
            observation(object) : current observation of the environment from agent
            normalise_num(int) : number for normalisation

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

    def predict(self, observation):
        """
        Choose the best action in current observation.

        # Arguments
            observation(object) : current observation of the environment

        # Returns
            action(int) : best action in current observation
        """
        try:
            observation = [int(x) for x in observation]
            state = self.normalise_state(observation, 10)
            return np.argmax(self.q_table[state])
        except ValueError as e:
            sys.stderr.write("Args should be list of integer: {0}".format(e))
            sys.exit(1)
        except Exception as e:
            sys.stderr.write("Unexpected error: {0}".format(e))
            sys.exit(1)

if __name__ == '__main__':
    pred = Predict()
    args = sys.argv
    print(pred.predict(args[1:]))

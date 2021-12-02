# -*- coding: utf-8 -*-

"""
This module contains a functions for random walk simulations.
"""

import csv
import math
import pathlib
import random
import statistics as st
import sys
import typing

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb
from seaborn.rcmod import reset_defaults

sb.set()


Time = float
Space = typing.Tuple[float]
State = typing.Tuple[Time, Space]
Result = typing.Generator[State, None, None]


__all__ = tuple(["simulate", "visualize"])


def simulate(state: State, steps: int, restricted = False) -> typing.Generator[Result, None, None]:
    """
    Simulate a random walk on 1/2/3-dimensional regular lattice.

    This function is not pure due the random number generation!

    :param steps: The number of steps.
    :param state: The initial state.
    :return: The simulation result.

    """
    if steps <= 0:
        raise ValueError("The steps value must be >= 0.")

    # Unpack the time and space coordinates.
    time, space = state[0], list(state[-1])

    # The previous state for restrickted version.
    previous_increment, previous_dimension = 0, 0

    # The anonymus function to generate random state.
    generate_increment_dimension = lambda: \
        ( random.choice([-1, 1]),
          random.choice([_ for _ in range( 0, len(space))])
        )

    # Update the time and space coordinates.
    for time in range(steps):
        increment, dimension = generate_increment_dimension()

        # When random walk is restricted then generate random state unless the direction is not return.
        if restricted:
            while (previous_increment, previous_dimension) == (-increment, dimension):
                increment, dimension = generate_increment_dimension()

        # Save the current state for the next cycle.
        previous_increment, previous_dimension = increment, dimension

        # Update time and appropriate space coordinate.
        time += 1; space[dimension] += increment

        yield time, tuple(space) # The generated (yielde) return value.


def visualize(data: Result, size = (10, 10), grid = True, style = "-k", path: pathlib.Path = None):
    data = tuple(data)
    # Set the labels and show or save the plot.
    # Get the dimension (length) of coordinates.
    match len(data[0][1]):
        case 1:
            xlabel, ylabel = "t", "x"
            xs, (ys) = zip(*data)
            points = xs, ys
        case 2:
            xlabel, ylabel = "x", "y"
            _, space = zip(*data)
            xs, ys = zip(*space)
            points = xs, ys
        case 3:
            xlabel, ylabel, zlabel = "x", "y", "z"
            _, space = zip(*data)
            xs, ys, zs = zip(*space)
            points = xs, ys, zs
        case _:
            raise Exception("Unknown number of dimensions.")

    title = f"Random walk {len(data[0][1])}D simulation with {len(data)} steps"

    # TODO: Simplify and clean the 2D/3D plot.
    if len(data[0][1]) == 3:
        fig = plt.figure(figsize=(15, 15))
        axs = fig.add_subplot(111, projection='3d')
        axs.set_title(title)
        axs.plot(*points, style)
        saveobj = fig # Hack
    else:
        plt.grid(grid)
        plt.figure(figsize = size)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.plot(*points, style)
        saveobj = plt # Hack

    # plt.plot(xs[-1], ys[-1], c='k', marker='o') # endpoint
    # axs.scatter(xs[-1], ys[-1], zs[-1], c='gray', marker='o')  # endpoint
    saveobj.savefig(str(path), format="png") if path is not None else plt.show()


def solution(trials = 500, repeats = 1000, restricted=False) -> typing.Generator[tuple[float, float, float], None, None]:
    """
    Solution for problem, see the notebook `random_walk.ipynb`.
    """
    for N in range(1, trials): # This loop can be parallelized, but how?
        # For each N repeat e.g 1000-times (trials) and calculate a mean distance R.
        R = []
        for n in range(0, repeats + 1):
            _, space  = tuple(simulate(steps=N, state=[0, (0, 0)], restricted=restricted))[-1]
            # Calculate the Euclidean distance (L2 norm) for the given coordinates.
            R.append(np.linalg.norm(space))

            print(f"trial = {N}/{trials}, walk = {n}/{repeats}", end="\r") # DEBUGGING: Replace by logging!

        # Calculate statistical mean and standard deviation.
        yield (N, st.mean(R), st.stdev(R))


if __name__ == "__main__":

    # TODO >>> Make cleaner command line interface and default parameters.
    import argparse

    # <<<<

    try:
        # Get command line arguments and parameters (will be improved).
        N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000      # Number of steps
        D = int(sys.argv[2]) if len(sys.argv) > 2 else 1         # Dimension 1/2/3D
        SEED = int(sys.argv[3]) if len(sys.argv) > 3 else 123321 # Random seed
        EXAMPLE = sys.argv[4] if len(sys.argv) > 4 else True     # Run example

        RESTRICTED = False
        MESSAGE = f"Random walk in {D}D simulation with {N} steps"

        # Set the seed for reproduciblity.
        random.seed(SEED)

        # Show simualation overview and run.
        if EXAMPLE:
            TRIALS = 500     # cca 500
            REPEATS = 10000  # cca 100
            print(f"Run 2D example with statistics: from 1 to {TRIALS} steps and {REPEATS} repeats per steps.")

            result = solution(trials=TRIALS, repeats=REPEATS, restricted=RESTRICTED)

            # TODO This should be some function.
            with open(f"output/data-{'restricted' if RESTRICTED else 'simple'}.csv",'w') as out:
                csv_out = csv.writer(out)
                csv_out.writerow(['N','R','E'])
                for row in result:
                    csv_out.writerow(row)

            print(f"---SUCCESS---{20 * ' '}")
        else:
            print(f"{MESSAGE}\n{'-' * len(MESSAGE)}")
            match D: # Run simulation for specified diemension.
                case 1:
                    data = simulate(steps = N, state = (0.0, [0.0]), restricted=RESTRICTED)
                case 2:
                    data = simulate(steps = N, state = (0.0, [0.0, 0.0]), restricted=RESTRICTED)
                case 3:
                    data = simulate(steps = N, state = (0.0, [0.0, 0.0, 0.0]), restricted=RESTRICTED)
                case _:
                    print(f"No random walk function for dimension {D} found.")
            # Show or save plots.
            visualize(data, path = pathlib.Path(f"output/RandomWalk{D}D-restricted={RESTRICTED}.png"))
            print(f"---SUCCESS---{20 * ' '}")

        sys.exit(0)

    except Exception as ex:
        print(ex)
        print("---FAILURE---")
        sys.exit(1)

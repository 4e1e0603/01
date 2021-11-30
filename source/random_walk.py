# -*- coding: utf-8 -*-

"""
This module contains a functions for random walk simulations.
"""

import sys
import csv
import math
import random
import typing
import pathlib

import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import statistics as st

from seaborn.rcmod import reset_defaults

sb.set()


Time = float
Space = typing.Tuple[float]
State = typing.Tuple[Time, Space]
Result = typing.Generator[State, None, None]


__all__ = tuple(["simulate", "visualize"])


def simulate(steps: int, state: State, restricted = False) -> Result:
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

    previous_increment, previous_dimension = 0, 0

    generate_increment_dimension = lambda: \
        ( random.choice([-1, 1]),
          random.choice([_ for _ in range( 0, len(state[-1]))])
        )

    # Update the time and space coordinates.
    for time in range(steps):
        increment, dimension = generate_increment_dimension()

        # When restricted random walk then generate unless the direction is not ooposite of previous.
        if restricted:
            while (previous_increment, previous_dimension) == (-increment, dimension):
                increment, dimension = generate_increment_dimension()

        previous_increment, previous_dimension = increment, dimension

        time += 1; space[dimension] += increment

        yield time, tuple(space)


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


def distance(coordinates: typing.Iterable[float]) -> float:
    """
    Calculate the Euclidean distance (L2 norm).
    """
    return math.sqrt(sum(( (x ** 2) for x in coordinates)))


def solution(trials = 500, repeats = 1000):
    """
    To simulate and analyze various types of random walks on the lattice in the plane (all steps are
    of the same length d = 1, but the direction is randomly chosen from a certain set of prescribed
    possibilities).

    Using Nw ≥ 500 random walks of n steps starting at the origin determine the mean Euclidean
    distance R after n steps together with its standard deviation. Plot the dependence of the mean
    distance (including error bars given by the standard deviation) on the number of steps n.

    Check that for all walks this dependence is of the form

        R(n) = c n^α                                                            (1)

    where α ∈ (0, 1). Determine the constant c and the exponent α by the least-square fitting (you
    can use e.g. the built-in function fit in Gnuplot) of the logarithm of the equation (1)

        ln(R) = ln c + α ln(n).                                                 (2)

    """
    result = []

    for N in range(1, trials):
        # For each N repeat e.g 1000-times (trials) and calculate a mean distance R.
        R = []
        for n in range(0, repeats + 1):
            _, space  = tuple(simulate(N, [0, (0, 0)]))[-1]
            R.append(distance(space))

        # Calculate statistical mean and standard deviation.
        result.append((N, st.mean(R), st.stdev(R)))

    with open('output/data.csv','w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['N','R','E'])
        for row in result:
            csv_out.writerow(row)


if __name__ == "__main__":
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
            TRIALS = 500; REPEATS = 1000
            print(f"Run 2D example with statistic calculations: from 1 to {TRIALS} steps and {REPEATS} per steps.")
            solution()
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

        visualize(data, path = pathlib.Path(f"output/RandomWalk{D}D-restricted={RESTRICTED}.png"))
        sys.exit(0)

    except Exception as ex:
        print(ex.with_traceback())
        sys.exit(1)

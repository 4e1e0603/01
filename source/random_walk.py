# -*- coding: utf-8 -*-

"""
This module contains a functions for random walk simulations.
"""

import sys
import random
import typing
import pathlib

import seaborn as sns
import matplotlib.pyplot as plt


sns.set()


Time = float
Space = tuple[float]
State = tuple[Time, Space]
Result = typing.Generator[State, None, None]


def simulate(steps: int, state: State) -> Result:
    """
    Simulate a random walk on 1/2/3-dimensional regular lattice.

    This function is not pure due the random number generation!

    :param steps: The number of steps.
    :param state: The initial state.
    :return: The simulation result.

    """
    # Unpack the time and space coordinates.
    time, space = state

    # Update the time and space coordinates.
    for time in range(steps):

        increment = random.choice([-1, 1])
        dimension = random.choice([_ for _ in range( 0, len(state[-1]))])

        time += 1
        space[dimension] += increment

        yield time, tuple(space)


def visualize(data: Result, size = (10, 10), grid = True, style = "-r", path: pathlib.Path = None):
    data = tuple(data)

    match len(data[0][1]):
        case 1:
            xlabel, ylabel = "t", "x"
            xs, (ys) = zip(*data)
        case 2:
            xlabel, ylabel = "x", "y"
            _, (xs, ys) = zip(*data)
        case 3:
            print("chart 3d")
            # THIS IS ONLY A QUICK DEMO VERSION!
            fig = plt.figure(figsize=(15, 15))
            ax = fig.gca(projection='3d')

            xyz, cur = [], [0, 0, 0]

            _, x, y, z = zip(*data)

            ax.plot(x, y, z, c="r", label='Random walk 3D')
            ax.scatter(x[-1], y[-1], z[-1], c='k', marker='o')   # End point
            ax.legend()

            plt.savefig(str(path), format="png") if path is not None else plt.show()


    plt.grid(grid)
    plt.figure(figsize = size)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(f"Random walk {len(data[0][1]) - 1}D simulation with {len(data)} steps")
    plt.plot(xs, ys, style)
    # plt.legend(loc="upper left")

    if len(data[0]) == 3: # The endpoint for 2D version.
        plt.plot(xs[-1], ys[-1], c='k', marker='o')

    plt.savefig(str(path), format="png") if path is not None else plt.show()


if __name__ == "__main__":

    # Command line arguments.
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000   # steps
    D = int(sys.argv[2]) if len(sys.argv) > 2 else 1      # 1D|2D
    S = int(sys.argv[3]) if len(sys.argv) > 3 else 123321 # seed

    random.seed(S)

    print(f"Random walk in {D}D simulation with {N} steps.")

    match D:
        case 1:
            data = simulate(steps = N, state = (0.0, [0.0]))
            # print(tuple(data))
            visualize(data = data, size = (15, 10), path = pathlib.Path("images/RandomWalk1D.png"))
        case 2:
            data = simulate(steps = N, state = (0.0, [0.0, 0.0]))
            print(tuple(data))
            # visualize(data = data, size = (15, 15), path = pathlib.Path("images/RandomWalk2D.png"))
        case 3:
            data = simulate(steps = N, state = (0.0, [0.0, 0.0, 0.0]))
            print(tuple(data))
            # visualize(data, path = pathlib.Path("images/RandomWalk3D.png"))
        case _:
            print(f"No random walk function for dimension {D} found.")
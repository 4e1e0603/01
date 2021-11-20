# -*- coding: utf-8 -*-

"""
This module contains a functions for random walk simulations.
"""

import sys
from pathlib import Path
from random import choice # randrange

import seaborn as sns
import matplotlib.pyplot as plt

from typing import Generator

sns.set()

# Simulation state type aliases.

Time = float
Space = float

State1D = tuple[Time, Space]
State2D = tuple[Time, Space, Space]
State3D = tuple[Time, Space, Space, Space]

# Simulation result type aliases.

Result1D = Generator[State1D, None, None]
Result2D = Generator[State2D, None, None]
Result3D = Generator[State3D, None, None]


def simulate_1d(steps: int, state: State1D) -> Result1D:
    """
    Simulate a random walk on one-dimensional regular lattice.

    This function is not pure due the random number generation!

    :param steps: The number of steps.
    :param state: The initial state.
    :return: The simulation result.

    """
    t, x = state

    for t in range(steps):
        t, x = (t + 1), x + choice([-1, 1])
        yield t, x


def simulate_2d(steps: int, state: State2D) -> Result2D:
    """
    Simulate a random walk on two-dimensional regular lattice.

    This function is not pure due the random number generation!

    :param steps: The number of steps.
    :param state: The initial position.
    :return: The simulation result.

    """
    t, x, y = state

    for step in range(steps):
        t += 1
        match choice(['x', 'y']):
            case 'x': x += choice([-1, 1])
            case 'y': y += choice([-1, 1])

        yield (t, x, y)


def simulate_3d(steps: int, state: State3D) -> Result3D:
    """
    Simulate a random walk on three-dimensional regular lattice.

    This function is not pure due the random number generation!

    :param steps: The number of steps.
    :param state: The initial position.
    :return: The simulation result.

    """
    t, x, y, z = state

    for step in range(steps):
        t += 1
        match choice(['x', 'y', 'z']):
            case 'x': x += choice([-1, 1])
            case 'y': y += choice([-1, 1])
            case 'z': z += choice([-1, 1])

        yield (t, x, y, z)


def visualize(data: Result1D | Result2D, size = (10, 10), grid = True, style = "-r", path: Path = None):
    data = tuple(data)

    match len(data[0]):
        case 2:
            xlabel, ylabel = "t", "x"
            xs, ys = zip(*data)
        case 3:
            xlabel, ylabel = "x", "y"
            _, xs, ys = zip(*data)

    plt.grid(grid)
    plt.figure(figsize = size)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(f"Random walk {len(data[0]) - 1}D simulation with {len(data)} steps")
    plt.plot(xs, ys, style)
    # plt.legend(loc="upper left")

    if len(data[0]) == 3: # The endpoint for 2D version.
        plt.plot(xs[-1], ys[-1], c='k', marker='o')

    plt.savefig(str(path), format="png") if path is not None else plt.show()


def visualize_3d(data, path):
    # This is only a quick demo version!
    import matplotlib as mpl
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import random

    fig = plt.figure(figsize=(15, 15))
    ax = fig.gca(projection='3d')

    xyz = []
    cur = [0, 0, 0]

    _, x, y, z = zip(*data)
    ax.plot(x, y, z, c="r", label='Random walk 3D')
    ax.scatter(x[-1], y[-1], z[-1], c='k', marker='o')   # End point
    ax.legend()
    plt.savefig(str(path), format="png") if path is not None else plt.show()


if __name__ == "__main__":

    # Command line arguments.
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000 # steps
    D = int(sys.argv[2]) if len(sys.argv) > 2 else 1    # 1D|2D

    print(f"Random walk in {D}D simulaton with {N} steps.")

    match D:
        case 1:
            data = simulate_1d(steps = N, state = (0.0, 0.0))
            visualize(data = data, size = (15, 10), path = Path("images/RandomWalk1D.png"))
        case 2:
            data = simulate_2d(steps = N, state = (0.0, 0.0, 0.0))
            visualize(data = data, size = (15, 15), path = Path("images/RandomWalk2D.png"))
        case 3:
            data = simulate_3d(steps = N, state = (0.0, 0.0, 0.0, 0.0))
            visualize_3d(data, path = Path("images/RandomWalk3D.png"))
        case _:
            print(f"No random walk function for dimension {D} found.")
# -*- coding: utf-8 -*-

import time
from re import T
from typing import Generator

from tqdm import tqdm
import numpy as np
from scipy import optimize, stats
import matplotlib.pyplot as plt


Result = tuple[float, float, float]


def simulate(trials, repeats, restriction = False, check_restrictions = False) -> Generator[Result, None, None]:

    """
    Transition table for restricted moves. Steps with * are not allowed
    rows and columns are indexes to direction array, so e.g star with
    F=0 and T=2 means that move directions[2] cannot follow move direction[0],
    i.e complex(0, -1) cannot ba just after complex(0, 1) etc...

        T 0 1 2 3
        F+-------+
        0| | |*| |
        1| | | |*|
        2|*| | | |
        3| |*| | |
        +-------+
    """

    directions = np.array([complex(0, 1), complex(1, 0), complex(0, -1), complex(-1, 0)])

    # Calculate probabilites for 5 discrete values.
    x = np.arange(-2, 3)
    prob = stats.norm.cdf(x + 0.5, scale=1.58) - stats.norm.cdf(x - 0.5, scale=1.58)
    prob = prob / prob.sum()

    for N in range(1, trials + 1):
        dst = []
        if restriction:
            for n in range(repeats):
                # Choose random numbers from [-2, -1, 0, 1, 2].
                nums = np.random.choice(x, size=N, p=prob)
                # Swap `+/- 2` with `+/- 3`.
                nums[nums == -2] = -3
                nums[nums == 2] = 3
                # Cumulative sum to calculate steps with restriction. (+/- 2 steps are restricted).
                steps = np.mod(np.cumsum(nums), 4)

                # Check steps according to transition table
                if check_restrictions:
                    for F, T in [(0, 2), (1, 3), (2, 0), (3, 1)]:
                        nxt = np.where(steps == F)[0] + 1
                        nxt = nxt[nxt < len(steps)]
                        if np.any(np.where(steps[nxt] == T)[0]):
                            raise ValueError(f'Restricted move ({F}, {T}) found!')

                walk = directions[steps].cumsum()
                dst.append(abs(walk[-1]))
        else:
            for n in range(repeats):
                steps = np.random.randint(0, 4, N)
                walk = directions[steps].cumsum()
                dst.append(abs(walk[-1]))

        yield (N, np.mean(dst), np.std(dst))


def visualize(results) -> None:

    steps, distance, error = np.array(results).T

    # The curve fitting.
    fun = lambda x, a, b: a + b * np.sqrt(x)
    fit, _ = optimize.curve_fit(fun, steps, distance)

    # Plot with 2 sigma and 1 sigma fills, points with mean values and curve for fit.
    plt.fill_between(
        steps, distance - 2 * error, distance + 2 * error, color="gray", alpha=0.2
    )

    plt.fill_between(steps, distance - error, distance + error, color="gray", alpha=0.4)
    plt.plot(steps, distance, "k.")
    plt.plot(steps, fun(steps, *fit), "r", lw=3)
    plt.title(r"$y=%.3f + %.3f\sqrt{x})$" % (fit[0], fit[1]))

    plt.show()


if __name__ == "__main__":

    TRIALS = 50
    REPEATS = 100
    RESTRICTION = True
    CHECK_RESTRICTIONS = True

    print(f"Random walk 2D example (restrictions={RESTRICTION}: from 1 to {TRIALS} steps and {REPEATS} repeats per step.")

    t0 = time.time()
    results =[_ for _ in tqdm(simulate(TRIALS, REPEATS, RESTRICTION, CHECK_RESTRICTIONS), desc="Calculating trials")]
    dt = time.time() - t0

    print(f"Total time of execution: {dt:.2g} seconds.")

    visualize(results)
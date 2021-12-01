import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time

TRIALS = 500   # cca 500
REPEATS = 1000  # cca 100

directions = np.array([complex(0, 1), complex(1, 0), complex(0, -1), complex(-1, 0)])

results = []

t0 = time.time()
for N in range(1, TRIALS):
    dst = []
    for n in range(REPEATS):
        steps = np.random.randint(0, 4, N)
        walk = directions[steps].cumsum()
        dst.append(abs(walk[-1]))
    
    results.append((N, np.mean(dst), np.std(dst)))

t1 = time.time()
soltime = t1 - t0

print(f"Run 2D example with statistics: from 1 to {TRIALS} steps and {REPEATS} repeats per step.")
print(f"Total time of execution: {soltime:.2g} seconds.")

# visualization
steps, distance, error = np.array(results).T

# fit curve
fun = lambda x, a, b: a + b*np.sqrt(x)
fit, _ = curve_fit(fun, steps,  distance)

# plot with 2 sigma and 1 sigma fills, points with mean values and curve for fit
plt.fill_between(steps, distance - 2*error, distance + 2*error, color='gray', alpha=0.2)
plt.fill_between(steps, distance - error, distance + error, color='gray', alpha=0.4)
plt.plot(steps, distance, 'k.')
plt.plot(steps, fun(steps, *fit), 'r', lw=3)
plt.title(r'$y=%.3f + %.3f\sqrt{x})$' % (fit[0], fit[1]))
plt.show()


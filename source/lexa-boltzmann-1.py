from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt


def get_pairs(x):
    return np.diff(np.asarray(list(combinations(x, 2))), axis=1).ravel()


def get_deltad_pairs(r):
    return np.sqrt(get_pairs(r[0]) ** 2 + get_pairs(r[1]) ** 2)


def compute_new_v(v1, v2, r1, r2):
    k = np.diag((v1 - v2).T @ (r1 - r2)) / np.sum((r1 - r2) ** 2, axis=0)
    v1_new = v1 - k * (r1 - r2)
    v2_new = v2 - k * (r2 - r1)
    return v1_new, v2_new


radius = 0.016  # ball radius
ts = 500  # number of simulation time steps
dt = 0.005  # timestep in sec
vi = 1  # initial velocity in m/s

# Initial positions on regular grid
sz = 20
X, Y = np.meshgrid(np.linspace(-1, 1, sz), np.linspace(-1, 1, sz))
ix = (X ** 2 + Y ** 2) < 0.9
r = np.array([X[ix], Y[ix]])
n_particles = r.shape[1]
# constant velocity in random direction
theta = 2 * np.pi * np.random.random(n_particles)
v = vi * np.array([np.cos(theta), np.sin(theta)])

# create ids
ids = np.arange(n_particles)
ids_pairs = np.asarray(list(combinations(ids, 2)))

fig, ax = plt.subplots(figsize=(8, 8))
ax.add_patch(plt.Circle((0, 0), radius=1, fc="none", ec="k"))
(pts,) = ax.plot(r[0], r[1], "go")
ax.set_aspect(1)
ax.set_axis_off()
fig.tight_layout()


for i in range(1, ts):
    ic = ids_pairs[get_deltad_pairs(r) < 2 * radius].T
    cdot = np.diag((v[:, ic[0]] - v[:, ic[1]]).T @ (r[:, ic[0]] - r[:, ic[1]]))
    ic_ok = cdot < 0
    v[:, ic[0, ic_ok]], v[:, ic[1, ic_ok]] = compute_new_v(
        v[:, ic[0, ic_ok]], v[:, ic[1, ic_ok]], r[:, ic[0, ic_ok]], r[:, ic[1, ic_ok]]
    )
    dr = np.linalg.norm(r, axis=0)
    rn = r / dr
    dp = np.diag(rn.T @ v)
    dix = (dr >= 1 - radius) & (dp > 0)
    v[:, dix] = v[:, dix] - 2 * dp[dix] * rn[:, dix]
    r = r + v * dt
    pts.set_data(r[0], r[1])
    plt.draw()
    plt.pause(0.001)

plt.close()

vf = np.linalg.norm(v, axis=0)
# The Maxwell-Boltzmann speed distribution for a two-dimensional gas
vspace = np.linspace(0, 1.1*max(vf), 500)
a = 2/vi**2
mb2d = a*vspace*np.exp(-a*vspace**2 / 2)
plt.hist(vf, bins="auto", density=True)
plt.plot(vspace, mb2d, label='Maxwell–Boltzmann distribution')
plt.xlabel('Velocity [m/s]')
plt.ylabel('Probability')
plt.title('Final velocity distibution')
plt.legend()
plt.show()

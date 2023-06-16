from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.stats import gaussian_kde


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
ts = 2000  # number of simulation time steps
dt = 0.005  # timestep in sec
vi = 1  # initial velocity in m/s

# Initial positions on regular grid
sz = 30
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

fig = plt.figure(figsize=(8, 8))
gs = GridSpec(2, 1, height_ratios=[4, 1])
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

ax1.add_patch(plt.Circle((0, 0), radius=1, fc="none", ec="k"))
(pts,) = ax1.plot(r[0], r[1], "go")
ax1.set_aspect(1)
ax1.set_axis_off()

ax2.set_xlabel('Velocity [m/s]')
ax2.set_ylabel('Probability')

# The Maxwell-Boltzmann speed distribution for a two-dimensional gas
vspace = np.linspace(0, 3, 500)
a = 2/vi**2
mb2d = a*vspace*np.exp(-a*vspace**2 / 2)
ax2.plot(vspace, mb2d, label='Maxwell–Boltzmann distribution')

vf = np.linalg.norm(v, axis=0)
kernel = gaussian_kde(vf)
vf_pdf = kernel(vspace)
ln, = ax2.plot(vspace, vf_pdf, label='Actual velocity distribution')
ax2.legend()
ax2.set_ylim(0, 2)

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
    vf = np.linalg.norm(v, axis=0)
    kernel = gaussian_kde(vf)
    vf_pdf = kernel(vspace)
    ln.set_data(vspace, vf_pdf)
    pts.set_data(r[0], r[1])
    plt.draw()
    plt.pause(0.001)

plt.show()

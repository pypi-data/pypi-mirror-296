import numpy as np
import tkz

# Multiple, long, noisy, solid paths
np.random.seed(0)
xu = np.linspace(-0.5, 0.5, 100000)
u = np.zeros((2, len(xu)))
for j in range(2):
    u[j, :] = 10*(j + 1)*np.cos(2*np.pi*3*xu + j*np.pi*2/3) \
            + 0.01*np.random.randn(len(xu))
u[0, 40000:60000] = np.nan # Add nans.

# Multiple, scatter plots, with infs and out-of-bounds edges
xv = np.linspace(-1, 1, 50)
v = np.array([np.tan(xv - np.pi/2), 1/xv])
v[0, 25] = -np.inf
r = 0.03 + 1*xv**2

# Fill with gaps.
t = np.linspace(0, 2*np.pi, 1000)
xw = 0.4 + 0.1*np.cos(t)
w = 20 + 5*np.sin(t)
w[490:510] = np.nan

# Fill between
xx = np.linspace(0.6, 0.8, 1000)
yx = 21.5 + 1*np.cos(2*np.pi*(xx - 0.7)/0.2)
zx = 18.5 - 1*np.cos(2*np.pi*(xx - 0.7)/0.2)
zx[490:510] = np.nan

tkz.config.savepng = True
tkz.config.savetex = True

fig = tkz.graph('test_range')
fig.plot(xu, u, label='simp')
fig.scatter(xv, v[0], radius=r, label='circles')
fig.scatter(xv, v[1], radius=r, marker=tkz.DOTS, label='dots')
fig.fill(xw, w, label='fill')
fig.fill(xx, yx, zx, label='between')
fig.xlabel = '$x$ axis'
fig.ylabel = '$y$ axis'
fig.xmin = -0.5
fig.render()

import numpy as np
import tkz

x = np.linspace(0, 1, 1000)
y = np.sin(2*np.pi*3*x)

fig = tkz.graph("fig_only_y")
fig.plot(y)
fig.render()

import numpy as np
import tkz

t = np.linspace(0, 2*np.pi, 10000)
x = np.cos(t)
y = np.sin(t)

fig = tkz.graph('test_basic')
fig.plot(x, y)
fig.xlabel = 'x axis'
fig.ylabel = 'y axis'
fig.equal = True
fig.render()

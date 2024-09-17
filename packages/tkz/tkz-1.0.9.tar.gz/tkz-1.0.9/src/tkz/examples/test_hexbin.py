import numpy as np
import matplotlib.pyplot as plt
import tkz

np.random.seed(0)

K = 10000
x = 0.5 + 0.1*np.random.randn(K)
y = 0.5 + 0.1*np.random.randn(K)

if True:
    fig = tkz.graph("test_hexbin")
    fig.hexbin(x, y, radius=-0.05, label="size")
    fig.hexbin(x + 0.5, y, radius=0.05, label="shade")
    fig.scatter(x + 1.0, y, radius=0.01, marker=tkz.DOTS, label="scatter")
    fig.equal = True
    fig.xlabel = "$x$ axis"
    fig.ylabel = "$y$ axis"
    fig.render()
else:
    plt.figure()
    plt.hexbin(x, y, cmap=plt.cm.Blues, mincnt=1, edgecolors=None, label="size")
    plt.hexbin(x + 0.5, y, cmap=plt.cm.Greens, mincnt=1, edgecolors=None,
               label="shade")
    plt.scatter(x + 1.0, y, color="r", s=0.01, edgecolors=None, label="scatter")
    plt.axis("equal")
    plt.xlabel("$x$ axis")
    plt.ylabel("$y$ axis")
    plt.legend()
    plt.savefig("test_hexbin_plt.pdf")
    plt.show()

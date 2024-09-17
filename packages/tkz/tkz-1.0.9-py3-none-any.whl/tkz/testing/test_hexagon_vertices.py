"""
This script demonstrates building the hexagon pattern using a precalculated set
of vertices stored as an x array and a y array. These vertex coordinates are
rounded to the nearest 4th decimal place. This guarantees that all hexagon edges
perfectly butt up against each other. There are no gaps and no overlaps.
"""

import numpy as np
import math as m


def split_hex(U):
    U1a = U[::2, ::3].flatten()
    U1b = U[1::2, 1::3].flatten()
    U2a = U[::2, 1::3].flatten()
    U2b = U[1::2, 2::3].flatten()
    U3a = U[::2, 2::3].flatten()
    U3b = U[1::2, ::3].flatten()
    U1 = np.concatenate((U1a, U1b))
    U2 = np.concatenate((U2a, U2b))
    U3 = np.concatenate((U3a, U3b))
    return U1, U2, U3


def sort_hex(X, Y, P):
    nn = np.argsort(P)
    P = P[nn]
    X = X[nn]
    Y = Y[nn]
    return X, Y, P


s = 0.02 # radial distance to a vertex
Hy = 127 # number of rows
Hx = 127 # number of columns

# Define the vertex arrays.
VX = 2*Hx + 2
Xv = np.round(np.arange(VX)*(s*m.sqrt(3)/2), 4)
VY = 2*Hy + 2
Yv = np.zeros(VY)
Yv[::2] = np.round(np.arange(VY//2)*(s*1.5), 4)
Yv[1::2] = np.round(np.arange(VY//2)*(s*1.5) + s*0.5, 4)

# Define the positions and darknesses of all the hexagons.
if True:
    pps = 100*np.random.rand(Hy, Hx) # point scaling
else:
    pps = np.zeros((Hy, Hx))
    x0 = (Hx - 1)/2.0*s*m.sqrt(3)
    y0 = (Hy - 1)/2.0*s*1.5
    for gy in range(Hy//2):
        for hx in range(Hx):
            # Define position and darkness for row.
            xc = hx*s*m.sqrt(3) - x0
            yc = s*3*gy - y0
            r = np.sqrt(xc*xc + yc*yc)/(s*10)
            c = 50 + 50*np.cos(r)
            pps[2*gy, hx] = c

            # Define position and darkness for next row.
            xc = hx*s*m.sqrt(3) + s*m.sqrt(3)/2 - x0
            yc = s*(gy*3 + 1.5) - y0
            r = np.sqrt(xc*xc + yc*yc)/(s*10)
            c = 50 + 50*np.cos(r)
            pps[2*gy + 1, hx] = c
pps = np.round(pps).astype(int)
hhx = np.outer(np.ones(Hy), np.arange(Hx)).astype(int)
hhy = np.outer(np.arange(Hy), np.ones(Hx)).astype(int)

# Split and flatten the matrices.
X1, X2, X3 = split_hex(hhx)
Y1, Y2, Y3 = split_hex(hhy)
P1, P2, P3 = split_hex(pps)

# Sort.
X1, Y1, P1 = sort_hex(X1, Y1, P1)
X2, Y2, P2 = sort_hex(X2, Y2, P2)
X3, Y3, P3 = sort_hex(X3, Y3, P3)

# Concatenate.
hhx = np.concatenate((X1, X2, X3))
hhy = np.concatenate((Y1, Y2, Y3))
pps = np.concatenate((P1, P2, P3))

# Open the file and write the opening.
fid = open("test_hexagon_vertices.tex", "w")
fid.write("\\documentclass{standalone}\n")
fid.write("\\usepackage{tikz}\n")
fid.write("\\begin{document}\n")
fid.write("\\begin{tikzpicture}\n")

# Write the hexagons.
ps_last = None
for n in range(len(pps)):
    # Define the center of the hexagon.
    ps = pps[n]
    if (ps <= 1):
        continue
    hx = hhx[n]
    hy = hhy[n]

    # Start a new fill command.
    if ps_last is None:
        fid.write("\\fill[%s!%d]" % ("cyan", int(ps)))
        ps_last = ps
    elif ps != ps_last:
        fid.write(";\n\\fill[%s!%d]" % ("cyan", int(ps)))
        ps_last = ps

    # Write the hexagon vertices.
    odd = int(hy % 2)
    fid.write("\n") # bottom half, left to right
    fid.write("    (%.4g,%.4g)" % (Xv[2*hx + 0 + odd], Yv[2*hy + 1]))
    fid.write(" -- (%.4g,%.4g)" % (Xv[2*hx + 1 + odd], Yv[2*hy + 0]))
    fid.write(" -- (%.4g,%.4g)" % (Xv[2*hx + 2 + odd], Yv[2*hy + 1]))
    fid.write("\n   ") # top half, right to left
    fid.write(" -- (%.4g,%.4g)" % (Xv[2*hx + 2 + odd], Yv[2*hy + 2]))
    fid.write(" -- (%.4g,%.4g)" % (Xv[2*hx + 1 + odd], Yv[2*hy + 3]))
    fid.write(" -- (%.4g,%.4g)" % (Xv[2*hx + 0 + odd], Yv[2*hy + 2]))

# Write the closing and close the file.
fid.write(";\n")
fid.write("\\end{tikzpicture}\n")
fid.write("\\end{document}")
fid.close()

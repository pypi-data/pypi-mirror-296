"""
This script tests various methods for creating a heat map with hexagons.

    method      size        time        tex         pdf
    -------     -------     -------     -------     -------
    tikzset     99^2        15.84 s     350 kB      208 kB
    manual      127^2       18.49 s     1.6 MB      294 kB
    predefined  127^2       17.65 s     1.5 MB      277 kB
    grouped     127^2       13.00 s     1.5 MB      305 kB
    manual      64^2        4.74 s      450 kB      74 kB
    grouped     64^2        3.65 s      438 kB      74 kB

The maximum number of hexagons possible was 16256 (127 x 128). The "tikzset"
method relies on defining the shape of the hexagon once with a tikzset command.
Besides the maximum number of allowable hexagons being much lower and the
processing speed being much slower, this method tends to produce visual
artifacts due to the positioning being based on the centers rather than the
vertices of the hexagons. The "manual" method draws each shape manually and
specifies each color with a command like "cyan!20". The "predefined" method
defines all the colors up front and then calls on them. Unfortunately, this
method was only about 5% faster. Grouping the hexagon commands by darkness did
have a marked increase in speed: 42%. Even with one quarter the number of
hexagons, the speed increase was about 30%. The pdf file size did increased by
about 3.7%, but that's not a major concern. The main concern here is that a
single "fill" command could get too long for TeX memory. Testing showed that the
maximum number of hexagons possible in a single command is around 8010, just
about one half the number of hexagons possible with individual commands.
Consequently, it seems unlikely that this limit would be reached before the
total limit of hexagons is reached. The other problem is that the "grouped"
method results in connected hexagons. This is some kind of visual artifact due
to the inner workings of the pdf format. It does, sadly, look better without
that artifact. However, separating the hexagons into three, non-touching groups
fixes this problem. Then again, expanding the hexagons so that there are no
anti-aliasing lines separating any of the hexagons seems to look even better
because it reduces distraction from the pattern created by the hexagon shading.
With such an overlap, grouping the hexagons into three separate groups is
unnecessary. However, it does seem that such hexagon expansion results in
distorted-looking hexagons. Unfortunately, I will have to live with the
anti-aliasing borders.

Using only positive coordinates significantly decreased the compile time, by
about 2.2 times. It did not seem to matter if there were a single point with
negative coordinates. It seems it is the sum total of negative coordinates that
must be processed which slows down compile time.
"""

import numpy as np
import math as m

usePath = False
predefineColors = False
grouped = True

SQ3 = m.sqrt(3)
SQ3_2 = SQ3/2
color = "cyan"

# Define hexagon template.
x = [-SQ3_2, 0, SQ3_2, SQ3_2, 0, -SQ3_2]
y = [0.5, 1, 0.5, -0.5, -1, -0.5]

A = 0.02 # radial distance to a vertex
dx = round(A*SQ3, 4)
N_rows = 127
N_cols = 127
x0 = (N_cols - 1)/2.0*A*SQ3
y0 = (N_rows - 1)/2.0*A*1.5

# Define the positions and darknesses of all the hexagons.
C = np.zeros((N_rows, N_cols))
Xc = np.zeros((N_rows, N_cols))
Yc = np.zeros((N_rows, N_cols))
for n_row in range(N_rows//2):
    for n_col in range(N_cols):
        # Define position and darkness for row.
        xc = n_col*dx - x0
        yc = A*3*n_row - y0
        r = np.sqrt(xc*xc + yc*yc)/(A*10)
        c = 50 + 50*np.cos(r)
        Xc[2*n_row, n_col] = xc
        Yc[2*n_row, n_col] = yc
        C[2*n_row, n_col] = c

        # Define position and darkness for next row.
        xc = n_col*dx + A*SQ3_2 - x0
        yc = A*(n_row*3 + 1.5) - y0
        r = np.sqrt(xc*xc + yc*yc)/(A*10)
        c = 50 + 50*np.cos(r)
        Xc[2*n_row + 1, n_col] = xc
        Yc[2*n_row + 1, n_col] = yc
        C[2*n_row + 1, n_col] = c
if grouped:
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

    def sort_hex(X, Y, C):
        nn = np.argsort(C)
        C = C[nn]
        X = X[nn]
        Y = Y[nn]
        return X, Y, C

    # Split and flatten the matrices.
    X1, X2, X3 = split_hex(Xc)
    Y1, Y2, Y3 = split_hex(Yc)
    C1, C2, C3 = split_hex(C.astype(int))

    # Sort.
    X1, Y1, C1 = sort_hex(X1, Y1, C1)
    X2, Y2, C2 = sort_hex(X2, Y2, C2)
    X3, Y3, C3 = sort_hex(X3, Y3, C3)

    # Concatenate.
    Xc = np.concatenate((X1, X2, X3))
    Yc = np.concatenate((Y1, Y2, Y3))
    C = np.concatenate((C1, C2, C3))
else:
    # Flatten.
    Xc = np.round(Xc.flatten(), 4)
    Yc = np.round(Yc.flatten(), 4)
    C = C.flatten().astype(int)

# Open the file and write the opening.
fid = open("test_hexagons.tex", "w")
fid.write("\\documentclass{standalone}\n")
fid.write("\\usepackage{tikz}\n")
if usePath:
    fid.write("\\tikzset{\n")
    fid.write("    hex/.pic={\\fill (%.4g,%.4g)" %
            (A*x[0], A*y[0]))
    for m in range(1, 6):
        if m == 3:
            fid.write("\n       ")
        fid.write(" -- (%.4g,%.4g)" % (A*x[m], A*y[m]))
    fid.write(";\n}}\n")
if predefineColors:
    for m in range(2, 101):
        fid.write("\\colorlet{C%d}{%s!%d}\n" % (m, color, m))
fid.write("\\begin{document}\n")
fid.write("\\begin{tikzpicture}\n")

# Write the hexagons two rows at a time.
c_last = None
xo = np.array([-0.0005, 0, 0.0005, 0.0005, 0, -0.0005])
yo = np.array([0.0003, 0.0006, 0.0003, -0.0003, -0.0006, -0.0003])
for n in range(len(C)):
    # Define the center of the hexagon.
    xc = Xc[n] + x0
    yc = Yc[n] + y0
    c = C[n]
    # If the darkness is strong enough, draw the hexagon.
    if (c >= 2):
        if usePath:
            fid.write("\\path (%.4g,%.4g) pic[%s!%d] {hex};\n" %
                    (xc, yc, color, int(c)))
        elif predefineColors:
            fid.write("\\fill[C%d] (%.4g,%.4g)" %
                    (int(c), A*x[0]+xc, A*y[0]+yc))
            for m in range(1,6):
                fid.write(" -- (%.4g,%.4g)" % (A*x[m] + xc, A*y[m] + yc))
            fid.write(";\n")
        elif grouped:
            if c_last is None or c != c_last:
                if c_last is None:
                    fid.write("\\fill[%s!%d]" % (color, int(c)))
                else:
                    fid.write(";\n\\fill[%s!%d]" % (color, int(c)))
                c_last = c
            fid.write("\n    (%.4g,%.4g)"
                    % (A*x[0] + xc + xo[0], A*y[0] + yc + yo[0]))
            for m in range(1,6):
                if m == 3:
                    fid.write("\n       ")
                fid.write(" -- (%.4g,%.4g)"
                        % (A*x[m] + xc + xo[m], A*y[m] + yc + yo[m]))
            #fid.write(" -- cycle")
        else:
            fid.write("\\fill[%s!%d] (%.4g,%.4g)" %
                    (color, int(c), A*x[0]+xc, A*y[0]+yc))
            for m in range(1,6):
                fid.write(" -- (%.4g,%.4g)" % (A*x[m] + xc, A*y[m] + yc))
            fid.write(";\n")

if grouped:
    fid.write(";\n")

# Write the closing and close the file.
fid.write("\\end{tikzpicture}\n")
fid.write("\\end{document}")
fid.close()

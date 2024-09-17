"""
This script shows that while the .tex file size might be a bit larger when using
the draw command and no plot coordinates, the draw command is about 6.5 times
faster than the "plot coordinates" method.

            tex size    pdf size    time
            --------    --------    --------
Coords      171 kB      77 kB       12.2 s
Draw        200 kB      77 kB       1.89 s 
"""

import numpy as np


def tikz_open(fid):
    fid.write("% Preamble")
    fid.write("\n\\documentclass{standalone}")
    fid.write("\n\\usepackage{tikz}")
    fid.write("\n\\usepackage[pdftex, outline]{contour}")
    fid.write("\n\\usetikzlibrary{plotmarks}")
    fid.write("\n\\contourlength{0.8pt}")
    fid.write("\n\\newcommand{\\ul}[1] % vectors")
    fid.write("\n    {{}\\mkern1mu\\underline")
    fid.write("{\\mkern-1mu#1\\mkern-1mu}\\mkern1mu}")
    fid.write("\n\\newcommand{\\micro}")
    fid.write("\n    {{\\fontencoding{U}\\fontfamily{eur}")
    fid.write("\\selectfont\\char22}}")
    fid.write("\n\\DeclareSymbolFont{euler}{U}{eur}{m}{n}")
    fid.write("\n\\DeclareMathSymbol{\\PI}{\\mathord}{euler}{25}")
    fid.write("\n% Document contents")
    fid.write("\n\\begin{document}")
    fid.write("\n\\begin{tikzpicture}")


def tikz_close(fid):
    fid.write("\n\\end{tikzpicture}")
    fid.write("\n\\end{document}")


# Create the data.
N = 9750
t = np.linspace(0, 1.0, N)
x = np.cos(2*np.pi*t) + (1/np.sqrt(2))*np.cos(2*np.pi*24*t)
y = np.sin(2*np.pi*t) + (1/np.sqrt(2))*np.sin(2*np.pi*24*t)

# Define the setting.
coords = False

# Write the file.
fid = open("test_draw_coord.tex", "w")
tikz_open(fid)
fid.write("\n\\path (-4.318,-2.66867) rectangle (4.318,2.66867);")
if coords:
    fid.write("\n\\path[fill, red]")
    fid.write("\n    plot coordinates {")
    for n in range(N):
        if n % 4 == 0:
            fid.write("\n   ")
        fid.write(f" ({x[n]:0.4f},{y[n]:0.4f})")
    fid.write("};")
else:
    fid.write("\n\\fill[red]")
    fid.write(f"\n    ({x[0]:0.4f},{y[0]:0.4f})")
    for n in range(1, N):
        if n % 4 == 0:
            fid.write("\n   ")
        fid.write(f" -- ({x[n]:0.4f},{y[n]:0.4f})")
    fid.write(";")
tikz_close(fid)

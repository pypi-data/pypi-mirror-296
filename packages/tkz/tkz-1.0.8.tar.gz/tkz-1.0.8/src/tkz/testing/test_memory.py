"""
When using separate commands ("fill", "draw", and "path[mark]") rather than a
single "path" command with multiple attributes, the maximum number of points
which can be plotted, due to the demands on TeX memory, is decreased by 4.6%
(9329 instead of 9781). However, the .tex file size, .pdf file size, and
compilation time are all smaller for the combined method.

            tex size    pdf size    time
            --------    --------    --------
Separate    547 kB      836 kB      16.87 s
Combined    164 kB      766 kB      13.48 s
PD          70%         8.37%       20.1%

An interesting take away, is also that "path" vs "draw" does not seem to make
any difference in memory limitations. However, the "draw" and "fill" commands
are significantly faster than "path" command with "plot coordinates". When the
marks are not included, separate "fill" and "draw" commands are 3.37 times
faster than the "path" command with "plot coordinates" (3.36 s vs. 11.31 s).

If instead of using the "plot coordinates" method for markers, the "draw"
command is used with the "circle" attribute, the compilation time is much
faster. The entire image is generated in 7.81 s, about 1.7 times faster. This
opens up the possibility of redefining the markers.

Breaking up long paths into smaller paths does not seem to change the total
length of a path that can be handled. Removing returns causes LaTeX to run out
of buffer.
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
N = 9329
t = np.linspace(0, 1.0, N)
x = np.cos(2*np.pi*t) + (1/np.sqrt(2))*np.cos(2*np.pi*24*t)
y = np.sin(2*np.pi*t) + (1/np.sqrt(2))*np.sin(2*np.pi*24*t)

# Define the settings.
separate = True
use_marks = True

# Write the file.
fid = open("test_memory.tex", "w")
tikz_open(fid)
fid.write("\n\\path (-4.318,-2.6687) rectangle (4.318,2.6687);")
if separate:
    fid.write("\n\\fill[red]")
    fid.write(f"\n    ({x[0]:0.4f},{y[0]:0.4f})")
    for n in range(1, N):
        if n % 3 == 0:
            fid.write("\n   ")
        fid.write(f" -- ({x[n]:0.4f},{y[n]:0.4f})")
    fid.write(";")
    fid.write("\n\\draw")
    fid.write(f"\n    ({x[0]:0.4f},{y[0]:0.4f})")
    for n in range(1, N):
        if n % 3 == 0:
            fid.write("\n   ")
        fid.write(f" -- ({x[n]:0.4f},{y[n]:0.4f})")
    fid.write(";")
    if use_marks:
        for n in range(N):
            fid.write(f"\n\\draw ({x[n]:0.4f},{y[n]:0.4f}) circle (0.01);")
        #fid.write("\n\\path[mark=*, mark size=0.2pt]")
        #fid.write("\n    plot coordinates {")
        #for n in range(N):
        #    if n % 4 == 0:
        #        fid.write("\n   ")
        #    fid.write(f" ({x[n]:0.4f},{y[n]:0.4f})")
        #fid.write("};")
else:
    if use_marks:
        fid.write("\n\\path[draw, fill=red, mark=*, mark size=0.2pt]")
    else:
        fid.write("\n\\path[draw, fill=red]")
    fid.write("\n    plot coordinates {")
    for n in range(N):
        if n % 4 == 0:
            fid.write("\n   ")
        fid.write(f" ({x[n]:0.4f},{y[n]:0.4f})")
    fid.write("};")
tikz_close(fid)

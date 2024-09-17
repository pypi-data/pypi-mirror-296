"""
When the format is 0.3f, there is noticeable quantization in a high-point-count
circle. This visible quantization disappears with a 0.4f format. There is a
12.5% increase in the file size going from a 0.3f format to a 0.4f format. Using
the test_memory.py script, the maximum profile length was only slightly shorter
using a 0.4f format rather than a 0.3f format. For circles the size of the
letter 'o', 0.4f format can result in some visible quantization, but only when
zooming in very close.
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
N = 1000
R = 0.1
t = np.linspace(0, 1.0, N)
x = R*np.cos(2*np.pi*t)
y = R*np.sin(2*np.pi*t)

# Write the file.
fid = open("test_precision.tex", "w")
tikz_open(fid)
fid.write("\n\\path (-4.318,-2.66867) rectangle (4.318,2.66867);")
fid.write("\n\\draw[ultra thin]")
fid.write("\n    plot coordinates {")
for n in range(N):
    if n % 4 == 0:
        fid.write("\n   ")
    fid.write(f" ({x[n]:0.4f},{y[n]:0.4f})")
fid.write("};")
tikz_close(fid)

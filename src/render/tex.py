"""LaTeX configuration for Manim using the local TeX Live 2025 XeLaTeX."""
import os

from manim import TexTemplate

TEX_BIN = "/home/lanshuye/Apps/texlive/2025/bin/x86_64-linux"

# Make the local TeX Live visible even when a script imports this module without
# sourcing scripts/env.sh first. Manim calls xelatex/dvisvgm by name.
if TEX_BIN not in os.environ.get("PATH", "").split(os.pathsep):
    os.environ["PATH"] = TEX_BIN + os.pathsep + os.environ.get("PATH", "")

# XeLaTeX + xeCJK lets us typeset formulas and occasional Chinese labels with
# the same bundled Source Han Sans family used by the Text mobjects.
S01_TEX_TEMPLATE = TexTemplate(
    tex_compiler="xelatex",
    output_format=".xdv",
    preamble=r"""
\usepackage[english]{babel}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{xeCJK}
\setCJKmainfont{Source Han Sans CN}
""",
)

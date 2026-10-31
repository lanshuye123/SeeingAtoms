"""S01 16:9 cover with all essential content inside the centered 4:3 area.

Core safe area: 1440x1080 at x=240..1680 on a 1920x1080 canvas.
Background may extend to the full 16:9 frame; title, crystal, labels and
patterns stay inside the 4:3 crop.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from manim import (
    DOWN, LEFT, RIGHT, UP, Circle, Dot, Ellipse, FadeIn, Line, Polygon,
    RoundedRectangle, Scene, VGroup,
)

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.render.tex import S01_TEX_TEMPLATE  # noqa: E402
from src.render.theme import COLORS, body, credit, label, title  # noqa: E402

BG = COLORS["bg"]
INK = COLORS["ink"]
BEAM = COLORS["beam"]
MEASURE = COLORS["measure"]
MUTED = COLORS["muted"]


class S01Cover(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Full-bleed background: a faint beam and distant measurement marks.
        for i, x in enumerate([-6.8, -6.0, 6.0, 6.8]):
            self.add(Line([x, -4, 0], [x, 4, 0], color=COLORS["grid"], stroke_width=1).set_opacity(0.18))
        self.add(Line([-7.2, -3.4, 0], [7.2, 3.4, 0], color=BEAM, stroke_width=1).set_opacity(0.12))
        self.add(Line([-7.2, -3.7, 0], [7.2, 3.1, 0], color=BEAM, stroke_width=1).set_opacity(0.08))

        # Core title block, left aligned and inside the 4:3 safe width.
        kicker = label("看见原子 · 第一期", font_size=23, color=BEAM)
        main = title("一束 X 射线", font_size=78)
        sub = body("如何读出原子排列？", font_size=34, color=INK)
        rule = Line(LEFT * 2.6, RIGHT * 2.6, color=MEASURE, stroke_width=2)
        block = VGroup(kicker, main, sub, rule).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        block.move_to(LEFT * 1.55 + UP * 1.45)

        # A faceted crystal and an internal lattice, right side of the 4:3 area.
        crystal = Polygon(
            UP * 1.35, RIGHT * 0.95 + UP * 0.55, RIGHT * 0.72 + DOWN * 0.75,
            DOWN * 0.2 + DOWN * 1.15, LEFT * 0.78 + DOWN * 0.85, LEFT * 0.88 + UP * 0.45,
            color=BEAM, stroke_width=2, fill_color=BEAM, fill_opacity=0.04,
        )
        inner = Polygon(
            UP * 0.85, RIGHT * 0.62 + UP * 0.28, RIGHT * 0.44 + DOWN * 0.48,
            DOWN * 0.1 + DOWN * 0.72, LEFT * 0.5 + DOWN * 0.52, LEFT * 0.55 + UP * 0.25,
            color=BEAM, stroke_width=1, fill_opacity=0,
        ).set_stroke(opacity=0.45)
        lattice = VGroup()
        for row in range(3):
            for col in range(3):
                lattice.add(Dot([ (col - 1) * 0.32, (row - 1) * 0.32, 0], radius=0.03, color=INK).set_opacity(0.65))
        crystal_group = VGroup(crystal, inner, lattice).move_to(RIGHT * 3.85 + UP * 1.45)
        beam = Line(LEFT * 1.85 + UP * 2.55, RIGHT * 2.95 + UP * 1.65, color=MEASURE, stroke_width=2).set_opacity(0.75)
        beam_dot = Dot([2.95, 1.65, 0], radius=0.06, color=MEASURE)

        # Two small open reference patterns along the bottom, inside the safe area.
        def sticks(x0, y0, heights, color):
            g = VGroup()
            for i, h in enumerate(heights):
                x = x0 + i * 0.26
                g.add(Line([x, y0, 0], [x, y0 + h, 0], color=color, stroke_width=3))
            return g

        si = sticks(-4.35, -2.55, [0.55, 0.38, 0.24, 0.12], BEAM)
        ti = sticks(1.75, -2.55, [0.55, 0.38, 0.16, 0.30, 0.22], MEASURE)
        si_lab = label("Si", font_size=24, color=BEAM).next_to(si, UP, buff=0.18)
        ti_lab = label("TiO₂", font_size=24, color=MEASURE).next_to(ti, UP, buff=0.18)
        si_sub = credit("金刚石立方", font_size=17).next_to(si_lab, DOWN, buff=0.02)
        ti_sub = credit("金红石", font_size=17).next_to(ti_lab, DOWN, buff=0.02)

        # Small bottom line, still inside the safe area.
        bottom = credit("X 射线衍射 · 从一张图谱读出晶胞、原子与晶体完整性", font_size=17)
        bottom.move_to(DOWN * 3.35)

        self.add(block, crystal_group, beam, beam_dot, si, ti, si_lab, ti_lab, si_sub, ti_sub, bottom)
        # No extra animation needed; render a single still frame.

"""S01 style frame (not a final shot): title + crystal + lattice motif."""
from pathlib import Path
import sys

from manim import (
    DOWN, LEFT, RIGHT, UP, Circle, DashedLine, Dot, Line, Polygon, Scene, VGroup,
)

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.render.theme import COLORS, body, credit, label, title  # noqa: E402


class S01StyleFrame(Scene):
    def construct(self):
        self.camera.background_color = COLORS["bg"]

        # Faint measurement grid, deliberately low contrast.
        grid = VGroup()
        for x in range(-8, 9, 2):
            grid.add(Line(UP * 4.5, DOWN * 4.5, stroke_width=0.5, color=COLORS["grid"]).shift(RIGHT * x))
        for y in range(-4, 5, 2):
            grid.add(Line(LEFT * 8, RIGHT * 8, stroke_width=0.5, color=COLORS["grid"]).shift(UP * y))
        grid.set_opacity(0.22)
        self.add(grid)

        kicker = label("看见原子 · 第一期", color=COLORS["beam"], font_size=26)
        main = title("一束 X 射线", font_size=84)
        sub = body("如何读出原子的排列？", font_size=42, color=COLORS["ink"])
        rule = Line(LEFT * 3.1, RIGHT * 3.1, color=COLORS["measure"], stroke_width=2)
        foot = credit("风格样张 · 非成片", font_size=18)

        text_group = VGroup(kicker, main, sub, rule).arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        text_group.move_to(LEFT * 3.25 + UP * 0.10)

        # Abstract crystal: a faceted outline with an internal lattice.
        outline = Polygon(
            UP * 2.6, RIGHT * 1.55 + UP * 1.25, RIGHT * 1.25 + DOWN * 1.7,
            DOWN * 0.25 + DOWN * 2.2, LEFT * 1.35 + DOWN * 1.55, LEFT * 1.55 + UP * 1.05,
            color=COLORS["beam"], stroke_width=2, fill_color=COLORS["beam"], fill_opacity=0.045,
        )
        inner = Polygon(
            UP * 1.55, RIGHT * 1.05 + UP * 0.55, RIGHT * 0.75 + DOWN * 1.0,
            DOWN * 0.1 + DOWN * 1.25, LEFT * 0.85 + DOWN * 0.9, LEFT * 0.95 + UP * 0.55,
            color=COLORS["beam"], stroke_width=1, fill_opacity=0,
        ).set_stroke(opacity=0.55)

        lattice = VGroup()
        for row in range(4):
            for col in range(4):
                x = (col - 1.5) * 0.42
                y = (row - 1.5) * 0.42
                lattice.add(Dot([x, y, 0], radius=0.035, color=COLORS["ink"]).set_opacity(0.55))
        lattice.move_to(RIGHT * 0.05 + DOWN * 0.05)

        # A measurement line crossing the crystal, echoing the scale motif.
        measure = Line(LEFT * 2.4 + UP * 1.8, RIGHT * 2.4 + DOWN * 1.5, color=COLORS["measure"], stroke_width=1.2)
        tick = Line(UP * 0.12, DOWN * 0.12, color=COLORS["measure"], stroke_width=1.2).move_to(measure.get_end())
        crystal = VGroup(outline, inner, lattice)
        crystal.move_to(RIGHT * 3.55 + UP * 0.05)
        measure.move_to(RIGHT * 3.55 + UP * 0.05)
        tick.move_to(measure.get_end())

        self.add(text_group, crystal, measure, tick)
        foot.to_edge(DOWN, buff=0.45).to_edge(RIGHT, buff=0.7)
        self.add(foot)
        self.wait(0.2)

"""S01 style frame: XeLaTeX formula integrated with the series palette."""
from pathlib import Path
import sys

from manim import DOWN, LEFT, RIGHT, UP, Line, MathTex, Scene, VGroup

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.render.tex import S01_TEX_TEMPLATE  # noqa: E402
from src.render.theme import COLORS, body, credit, label, title  # noqa: E402


class BraggStyleFrame(Scene):
    def construct(self):
        self.camera.background_color = COLORS["bg"]

        kicker = label("看见原子 · 第一期", color=COLORS["beam"], font_size=24)
        heading = title("布拉格条件", font_size=46)
        formula = MathTex(r"2d\sin\theta = n\lambda", tex_template=S01_TEX_TEMPLATE, font_size=104)
        formula.set_color(COLORS["ink"])

        labels = VGroup(
            body("d  晶面间距", font_size=26, color=COLORS["measure"]),
            body("θ  射线与晶面的夹角", font_size=26, color=COLORS["measure"]),
            body("λ  X 射线波长", font_size=26, color=COLORS["measure"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)

        left = VGroup(kicker, heading, formula).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        left.move_to(LEFT * 2.5 + UP * 0.2)
        labels.next_to(formula, DOWN, buff=0.55).align_to(formula, LEFT)
        labels.shift(RIGHT * 0.15)

        rule = Line(LEFT * 4.3, RIGHT * 4.3, color=COLORS["measure"], stroke_width=1.5)
        rule.move_to(DOWN * 3.1)
        note = credit("示意 · 非成片", font_size=18)
        note.to_edge(DOWN, buff=0.45).to_edge(RIGHT, buff=0.7)

        self.add(left, labels, rule, note)
        self.wait(0.2)

"""Smoke test for XeLaTeX formulas and Chinese TeX labels."""
from pathlib import Path
import sys

from manim import DOWN, MathTex, Scene, Tex, UP, VGroup

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.render.tex import S01_TEX_TEMPLATE  # noqa: E402
from src.render.theme import COLORS, body, label  # noqa: E402


class TeXSmokeTest(Scene):
    def construct(self):
        self.camera.background_color = COLORS["bg"]
        formula = MathTex(r"2d\sin\theta = n\lambda", tex_template=S01_TEX_TEMPLATE, font_size=86)
        formula.set_color(COLORS["ink"])
        cn = Tex("晶面间距", tex_template=S01_TEX_TEMPLATE, font_size=48)
        cn.set_color(COLORS["measure"])
        note = body("XeLaTeX + xeCJK / Source Han Sans CN", font_size=26, color=COLORS["muted"])
        group = VGroup(formula, cn, note).arrange(DOWN, buff=0.55).move_to(UP * 0.1)
        self.add(label("公式渲染测试", color=COLORS["beam"]).to_edge(UP, buff=0.7))
        self.add(group)
        self.wait(0.2)

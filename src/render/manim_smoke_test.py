"""Manim smoke test: verifies CJK text, bundled fonts, and 16:9 rendering."""
from pathlib import Path
import sys

from manim import DOWN, LEFT, RIGHT, Line, Scene, UP

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.render.theme import COLORS, body, credit, label, title  # noqa: E402


class CJKSmokeTest(Scene):
    def construct(self):
        self.camera.background_color = COLORS["bg"]

        kicker = label("看见原子 · 第一期", color=COLORS["beam"])
        main = title("一束 X 射线", font_size=84)
        sub = body("如何读出原子的排列？", font_size=42, color=COLORS["ink"])
        rule = Line(LEFT * 3.0, RIGHT * 3.0, color=COLORS["measure"], stroke_width=2)
        foot = credit("字体与画面测试 · 1920×1080", font_size=18)

        kicker.move_to(UP * 2.2)
        main.move_to(UP * 1.0)
        sub.next_to(main, DOWN, buff=0.42)
        rule.next_to(sub, DOWN, buff=0.40)
        foot.to_edge(DOWN, buff=0.55)

        self.add(kicker, main, sub, rule, foot)
        self.wait(0.2)

"""S02 cover: 16:9, core content inside the centred 4:3 safe area."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from manim import DOWN, LEFT, RIGHT, UP, Circle, Dot, FadeIn, ImageMobject, Line, Rectangle, RoundedRectangle, Scene, VGroup

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.render.theme import COLORS, body, credit, label, title  # noqa: E402

BG = COLORS["bg"]
INK = COLORS["ink"]
BEAM = COLORS["beam"]
MEASURE = COLORS["measure"]
MUTED = COLORS["muted"]
GRID = COLORS["grid"]


class S02Cover(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Full-bleed background, but all text/graphics inside the 4:3 crop.
        for x in [-6.8, -6.2, 6.2, 6.8]:
            self.add(Line([x, -4, 0], [x, 4, 0], color=GRID, stroke_width=1).set_opacity(0.18))
        self.add(Line([-7.2, -3.3, 0], [7.2, 3.1, 0], color=BEAM, stroke_width=1).set_opacity(0.12))

        kicker = label("看见原子 · 第二期", font_size=23, color=BEAM)
        main = title("电子显微镜", font_size=78)
        sub = body("如何把原子“拍”出来？", font_size=34, color=INK)
        rule = Line(LEFT * 2.7, RIGHT * 2.7, color=MEASURE, stroke_width=2)
        block = VGroup(kicker, main, sub, rule).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        block.move_to(LEFT * 1.55 + UP * 1.5)

        # Simulated HRTEM panel, inside the 4:3 safe width.
        img = ImageMobject(ROOT / "chapters/s02/assets/sim/sim_srtio3_001_sr_under.png")
        img.set_height(3.8).move_to(RIGHT * 3.05 + UP * 1.2)
        frame = Rectangle(width=3.95, height=3.95, color=MEASURE, stroke_width=1.8).move_to(img)
        tag = credit("模拟计算 · 非实测", font_size=16, color=MUTED).next_to(frame, DOWN, buff=0.12)

        bottom = credit("从电子波长到相位衬度 · 一张高分辨像的读法", font_size=17)
        bottom.move_to(DOWN * 3.3)

        self.add(block, img, frame, tag, bottom)

"""S02 sync demo, S00: a 3b1b-style camera-led opening.

The aim is not decoration. Each camera move answers a question in the
narration: what is this object, how big is it, where does the electron go,
why is the screen green, why does the image sharpen, and what is a "column".

References for the vocabulary (not copied shots):
* Manim's MovingCameraScene / camera.frame:
  https://docs.manim.community/en/stable/reference/manim.scene.moving_camera_scene.html
* TransformMatchingTex/FadeTransform, ported from 3b1b/manim:
  https://github.com/ManimCommunity/manim/pull/1037
* 3b1b's scene source archive:
  https://github.com/www2341/3Blue1Brown.com_videos_animation_source_python

Render:
  source scripts/env.sh
  .venv/bin/manim -qm --fps 30 --media_dir media \
    chapters/s02/manim/sync_demo.py S02SyncDemo
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, Arrow, Circle, Circumscribe, Create, Dot, FadeIn,
    FadeOut, Flash, GrowArrow, GrowFromCenter, ImageMobject, Indicate,
    LaggedStart, Line, ORIGIN, Rectangle, ReplacementTransform, Rotate,
    RoundedRectangle, ShowPassingFlash, Text, VGroup, Write, always_redraw,
    smooth,
)

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import (  # noqa: E402
    BEAM, BG, GRID, INK, MEASURE, MUTED, TimelineScene,
)
from effects import (  # noqa: E402
    column_3d, lattice_3d, plate, radial_glow,
)
from src.render.theme import body, label, title  # noqa: E402

ASSETS = ROOT / "chapters" / "s02" / "assets"


class S02SyncDemo(TimelineScene):
    section_id = "S00"

    def construct(self):

        # A faint lattice is the visual ground for the whole opening.
        bg_lattice = lattice_3d(nx=6, ny=3, nz=3, a=0.62,
                                center=(-2.2, 0.2, 0), yaw=-0.55, pitch=0.40)
        bg_lattice.set_opacity(0.55)
        self.add(bg_lattice)

        # ---------------------------------------------------------------- S00_01
        self.cue("S00_01")
        grid = ImageMobject(ASSETS / "illustrations" / "ai_01_copper_grid_graded.png")
        grid.set_height(6.4).move_to(RIGHT * 1.5)
        grid.set_opacity(0.92)
        ring = Circle(radius=2.05, color=MEASURE, stroke_width=2.0).move_to(RIGHT * 1.5)
        ticks = VGroup()
        for i in range(24):
            ang = i * math.pi / 12
            r0 = 2.05
            r1 = 2.05 + (0.16 if i % 2 == 0 else 0.08)
            p0 = np.array([1.5 + r0 * math.cos(ang), r0 * math.sin(ang), 0])
            p1 = np.array([1.5 + r1 * math.cos(ang), r1 * math.sin(ang), 0])
            ticks.add(Line(p0, p1, color=MEASURE, stroke_width=1.2).set_opacity(0.7))
        grid_label = plate("3 mm 铜网", font_size=28, color=INK).move_to(LEFT * 1.9 + UP * 2.3)
        foil_label = plate("中间一层薄片", font_size=24, color=MEASURE).move_to(LEFT * 1.9 + UP * 1.3)
        foil_arrow = Arrow(foil_label.get_right() + RIGHT * 0.1, np.array([0.2, 0.15, 0]),
                           buff=0.08, color=MEASURE, stroke_width=2.2,
                           max_tip_length_to_length_ratio=0.12)

        self.play_t(FadeIn(grid, scale=1.05), FadeIn(ring), Create(ticks),
                    run_time=2.2)
        self.play_t(FadeIn(grid_label, shift=UP * 0.1),
                    FadeIn(foil_label, shift=UP * 0.1),
                    GrowArrow(foil_arrow), run_time=1.2)
        self.camera_to(width=9.4, center=RIGHT * 1.4, run_time=2.4)
        # A quick beam skim across the grid.
        beam_skim = Line(LEFT * 3.0 + UP * 3.2, RIGHT * 1.5 + DOWN * 0.2,
                         color=BEAM, stroke_width=2.2)
        self.play_t(ShowPassingFlash(beam_skim, time_width=0.35), run_time=1.2)

        # ---------------------------------------------------------------- S00_02
        self.cue("S00_02")
        column = ImageMobject(ASSETS / "illustrations" / "ai_02_column_graded.png")
        column.set_height(7.6).move_to(RIGHT * 1.0)
        column.set_opacity(0.95)
        beam = Line(RIGHT * 1.4 + UP * 3.7, RIGHT * 1.4 + DOWN * 3.6,
                    color=BEAM, stroke_width=3.0)
        beam_glow = radial_glow(RIGHT * 1.4 + UP * 3.4, 0.7, BEAM, max_opacity=0.22)
        rod = Line(LEFT * 3.2 + DOWN * 1.15, RIGHT * 0.2 + DOWN * 1.15,
                   color=MEASURE, stroke_width=7)
        rod_holder = RoundedRectangle(width=0.5, height=0.24, corner_radius=0.05,
                                      stroke_width=0, fill_color=MEASURE,
                                      fill_opacity=0.9).move_to(LEFT * 0.1 + DOWN * 1.15)
        rod_label = plate("样品杆", font_size=24, color=MEASURE).move_to(LEFT * 2.4 + DOWN * 1.9)

        self.play_t(FadeOut(grid), FadeOut(ring), FadeOut(ticks),
                    FadeOut(grid_label), FadeOut(foil_label), FadeOut(foil_arrow),
                    run_time=0.6)
        self.play_t(FadeIn(column), run_time=1.0)
        self.play_t(Create(beam), FadeIn(beam_glow, scale=0.7), run_time=0.9)
        self.play_t(FadeIn(rod, shift=RIGHT * 0.5), FadeIn(rod_holder),
                    FadeIn(rod_label), run_time=0.9)
        self.camera_to(width=8.2, center=RIGHT * 1.0, run_time=0.9)

        # ---------------------------------------------------------------- S00_03
        self.cue("S00_03")
        screen = RoundedRectangle(width=4.9, height=3.1, corner_radius=0.10,
                                  stroke_color=MUTED, stroke_width=1.2,
                                  fill_color="#0A241C", fill_opacity=1)
        screen.move_to(ORIGIN)
        screen_lab = plate("荧光屏", font_size=22, color=INK).move_to(screen.get_corner(DOWN + LEFT) + RIGHT * 0.8 + UP * 0.38)
        glow = radial_glow(ORIGIN, 1.25, BEAM, layers=48, max_opacity=0.42)
        hot = Dot(ORIGIN, radius=0.22, color=BEAM).set_opacity(0.9)

        self.play_t(FadeOut(column), FadeOut(beam), FadeOut(beam_glow),
                    FadeOut(rod), FadeOut(rod_holder), FadeOut(rod_label),
                    run_time=0.6)
        self.play_t(FadeIn(screen), FadeIn(screen_lab), run_time=0.8)
        self.play_t(FadeIn(glow, scale=0.7), FadeIn(hot), run_time=1.2)
        self.camera_to(width=7.4, center=ORIGIN, run_time=1.0)
        self.play_t(Flash(ORIGIN, color=BEAM, flash_radius=0.5,
                          line_length=0.12, num_lines=12), run_time=0.4)

        # ---------------------------------------------------------------- S00_04
        self.cue("S00_04")
        slab = RoundedRectangle(width=4.8, height=0.92, corner_radius=0.06,
                                stroke_color=MEASURE, stroke_width=1.4,
                                fill_color="#0B241C", fill_opacity=1).move_to(ORIGIN)
        grains = VGroup()
        rng = np.random.default_rng(4)
        for i in range(18):
            x = rng.uniform(-2.1, 2.1)
            y = rng.uniform(-0.32, 0.32)
            grains.add(Circle(radius=rng.uniform(0.055, 0.10),
                              stroke_width=0, fill_color=MEASURE,
                              fill_opacity=rng.uniform(0.65, 1.0))
                       .move_to([x, y, 0]))
        e_arrow = Arrow(LEFT * 4.2 + DOWN * 0.9, LEFT * 2.45 + DOWN * 0.15,
                        buff=0.05, color=BEAM, stroke_width=3.2,
                        max_tip_length_to_length_ratio=0.10)
        zn_label = body("ZnS:Cu", font_size=28, color=INK).move_to(LEFT * 1.6 + DOWN * 1.05)
        spectrum = Line(RIGHT * 1.0 + DOWN * 1.05, RIGHT * 2.8 + DOWN * 1.05,
                        color=BEAM, stroke_width=6)
        spectrum_lab = body("550 nm", font_size=24, color=INK).move_to(RIGHT * 2.0 + DOWN * 1.50)

        self.play_t(ReplacementTransform(screen, slab), FadeOut(screen_lab),
                    FadeOut(glow), FadeOut(hot), run_time=1.0)
        self.bring_to_front(slab)
        self.play_t(FadeIn(e_arrow, shift=RIGHT * 0.2), run_time=0.8)
        self.play_t(LaggedStart(*[GrowFromCenter(g) for g in grains],
                                lag_ratio=0.07), run_time=1.8)
        self.bring_to_front(grains)
        self.play_t(FadeIn(zn_label), Create(spectrum), FadeIn(spectrum_lab),
                    run_time=1.2)
        self.camera_to(width=6.2, center=LEFT * 0.1, run_time=1.2)

        # ---------------------------------------------------------------- S00_05
        self.cue("S00_05")
        sharp = ImageMobject(ASSETS / "sim" / "sim_srtio3_001_sr_under.png")
        sharp.set_height(3.4).move_to(RIGHT * 1.8)
        blur = ImageMobject(ASSETS / "sim" / "sim_srtio3_001_sr_under_blur.png")
        blur.set_height(3.4).move_to(RIGHT * 1.8)
        frame = Rectangle(width=3.45, height=3.45, stroke_color=GRID,
                          stroke_width=1.2, fill_opacity=0).move_to(RIGHT * 1.8)
        sharp.set_opacity(0)

        self.play_t(FadeOut(slab), FadeOut(grains), FadeOut(e_arrow),
                    FadeOut(zn_label), FadeOut(spectrum), FadeOut(spectrum_lab),
                    run_time=0.8)
        self.camera_to(width=7.6, center=RIGHT * 1.2, run_time=1.6)
        self.play_t(FadeIn(blur), FadeIn(frame), run_time=1.2)
        self.play_t(blur.animate.set_opacity(0.0), sharp.animate.set_opacity(1.0),
                    run_time=2.2)
        self.play_t(Flash(np.array([2.15, 0.55, 0]), color=MEASURE,
                          flash_radius=0.35, line_length=0.10, num_lines=10),
                    run_time=0.6)

        # ---------------------------------------------------------------- S00_06
        self.cue("S00_06")
        target = Dot(np.array([2.15, 0.55, 0]), radius=0.10, color=MEASURE)
        target_ring = Circle(radius=0.24, color=MEASURE, stroke_width=1.8).move_to(target)
        atom_label = title("原子列", font_size=42).move_to(LEFT * 1.4 + UP * 1.55)
        atom_arrow = Arrow(atom_label.get_right() + RIGHT * 0.15,
                           np.array([0.35, 0.65, 0]), buff=0.06,
                           color=MEASURE, stroke_width=2.2,
                           max_tip_length_to_length_ratio=0.12)
        note = plate("模拟计算 · 非实测", font_size=18,
                     color=MUTED).move_to(frame.get_corner(DOWN + RIGHT) + UP * 0.20 + LEFT * 0.85)

        self.play_t(FadeIn(target), FadeIn(target_ring), run_time=0.3)
        self.play_t(FadeIn(atom_label, shift=UP * 0.1), GrowArrow(atom_arrow),
                    FadeIn(note), run_time=0.7)

        # A small column model, from top view (collapsed) to side view.
        build_col, col_tracker = column_3d(n=5, spacing=0.30,
                                           center=LEFT * 1.45 + UP * 0.45)
        col = always_redraw(build_col)
        col_lab = body("一列原子", font_size=20, color=BEAM).move_to(LEFT * 1.45 + DOWN * 0.75)
        self.add(col)
        self.wait_t(0.1)
        self.play_t(FadeIn(col_lab), col_tracker.animate.set_value(0.72), run_time=0.8)

        # ---------------------------------------------------------------- S00_07
        self.cue("S00_07")
        question = body("那一排排线，是怎么来的？", font_size=48, color=INK)
        question.move_to(LEFT * 1.3 + DOWN * 0.1)
        q_bg = Rectangle(width=question.width + 0.5, height=question.height + 0.3,
                         stroke_width=0, fill_color=BG, fill_opacity=0.85).move_to(question)
        underline = Line(question.get_left() + DOWN * 0.35,
                         question.get_left() + DOWN * 0.35 + RIGHT * 4.6,
                         color=MEASURE, stroke_width=2.2).set_opacity(0.7)
        col.clear_updaters()
        self.play_t(FadeOut(target), FadeOut(target_ring), FadeOut(atom_label),
                    FadeOut(atom_arrow), FadeOut(note), FadeOut(col), FadeOut(col_lab),
                    sharp.animate.set_opacity(0.18), frame.animate.set_opacity(0.18),
                    bg_lattice.animate.set_opacity(0.18),
                    run_time=1.0)
        self.camera_to(width=12.0, center=LEFT * 0.6, run_time=1.8)
        self.play_t(FadeIn(q_bg), Write(question), Create(underline), run_time=1.8)
        self.finish()

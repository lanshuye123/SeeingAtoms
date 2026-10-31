"""S01 storyboard scenes (1080p, 30 fps).

Each scene is a separately rendered segment; audio timing comes from
chapters/s01/audio/timing.json. The final assembly concatenates the silent
segments with the narration and burned-in SRT.
"""
from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path

import numpy as np

from manim import (
    DOWN, LEFT, RIGHT, UP, Arc, Arrow, Axes, Circle, Create, Dot, Ellipse,
    FadeIn, FadeOut, GrowArrow, GrowFromCenter, GrowFromPoint, LaggedStart, Line, Polygon,
    Rectangle, RoundedRectangle, Text, Transform, VGroup, Write, YELLOW,
    config, linear, smooth,
)

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.render.tex import S01_TEX_TEMPLATE  # noqa: E402
from src.render.theme import COLORS, body, credit, label, title  # noqa: E402
from common import (  # noqa: E402
    ALERT, BEAM, BG, GRID, INK, MEASURE, MUTED, ROOT, TimedScene, axes_2theta,
    badge, callout, formula, kicker, lattice, note, pattern_group, peak_shape, powder_holder,
    scene_duration, section_title, simple_unit_cell, wave,
)

APP_DIR = ROOT / "chapters" / "s01" / "assets"
PATTERNS = json.loads((APP_DIR / "xrd_patterns.json").read_text(encoding="utf-8"))
PEAKS = {p["id"]: p["peaks"] for p in PATTERNS["phases"]}


class S00(TimedScene):
    scene_id = "s00"

    def construct(self):
        kicker(self)

        # Title card over a dark ground.
        t1 = title("一束 X 射线", font_size=76)
        t2 = body("如何读出原子的排列？", font_size=38, color=INK)
        title_group = VGroup(t1, t2).arrange(DOWN, buff=0.28).move_to(UP * 0.1)
        self.play_t(FadeIn(title_group, shift=UP * 0.15), run_time=2.0)
        self.wait_t(3.0)
        self.play_t(FadeOut(title_group), run_time=1.2)

        # The sample holder: a shallow tray of white powder.
        holder = powder_holder(width=8.8, height=3.6, seed=11).move_to(UP * 0.15)
        self.play_t(FadeIn(holder), run_time=1.8)
        apps = label("药物 · 陶瓷 · 催化剂 · 电池材料", font_size=24, color=MUTED)
        apps.next_to(holder, DOWN, buff=0.28)
        self.play_t(FadeIn(apps, shift=UP * 0.1), run_time=1.5)
        self.play_t(holder.animate.scale(1.10), run_time=7.0, rate_func=linear)
        self.play_t(FadeOut(apps), run_time=0.6)
        self.play_t(FadeOut(holder), run_time=0.8)

        # A minimal diffractometer cross-section.
        tube = RoundedRectangle(width=1.25, height=1.05, corner_radius=0.12,
                                stroke_color=MEASURE, fill_color="#151C2E", fill_opacity=1)
        tube.move_to(LEFT * 5.3 + UP * 0.8)
        stage = RoundedRectangle(width=2.0, height=0.42, corner_radius=0.08,
                                 stroke_color=BEAM, fill_color="#151C2E", fill_opacity=1)
        stage.move_to(LEFT * 0.4 + DOWN * 0.4)
        det = RoundedRectangle(width=0.42, height=2.4, corner_radius=0.08,
                               stroke_color=MUTED, fill_color="#151C2E", fill_opacity=1)
        det.move_to(RIGHT * 3.7 + DOWN * 0.1)
        beam = Line(tube.get_right(), stage.get_left() + UP * 0.05, color=BEAM, stroke_width=3)
        beam2 = Line(stage.get_right() + UP * 0.05, det.get_left(), color=BEAM, stroke_width=2)
        lab_tube = label("X 射线管", font_size=20).next_to(tube, DOWN, buff=0.15)
        lab_stage = label("样品", font_size=20).next_to(stage, DOWN, buff=0.15)
        lab_det = label("探测器", font_size=20).next_to(det, DOWN, buff=0.15)
        instrument = VGroup(tube, stage, det, beam, beam2, lab_tube, lab_stage, lab_det)
        self.play_t(FadeIn(instrument), run_time=1.2)
        self.play_t(Create(beam), run_time=1.0)
        self.play_t(Create(beam2), run_time=0.8)
        self.wait_t(2.0)
        self.play_t(FadeOut(instrument), run_time=0.8)

        # Zoom to the atomic lattice and the scale ruler.
        atoms = lattice(rows=4, cols=5, dx=1.0, dy=0.9, radius=0.10).move_to(LEFT * 2.1)
        bonds = VGroup()
        for i in range(4):
            for j in range(5):
                p = [(j - 2) * 1.0 - 2.1, (i - 1.5) * 0.9, 0]
                if j < 4:
                    bonds.add(Line(p, [p[0] + 1.0, p[1], 0], color=GRID, stroke_width=2))
                if i < 3:
                    bonds.add(Line(p, [p[0], p[1] + 0.9, 0], color=GRID, stroke_width=2))
        lattice_group = VGroup(bonds, atoms)
        self.play_t(FadeIn(lattice_group), run_time=1.2)
        self.play_t(LaggedStart(*[GrowFromCenter(a) for a in atoms], lag_ratio=0.05), run_time=2.0)
        self.play_t(Create(bonds), run_time=1.0)

        ruler = Line(UP * 2.6 + RIGHT * 3.5, DOWN * 2.5 + RIGHT * 3.5, color=MUTED, stroke_width=2)
        ticks = VGroup()
        for i, y in enumerate([2.6, 1.4, 0.2, -1.0, -2.2]):
            ticks.add(Line([3.35, y, 0], [3.65, y, 0], color=MUTED, stroke_width=1.5))
        ruler_labels = VGroup(
            label("10⁻² m", font_size=18).next_to([3.8, 2.6, 0], RIGHT, buff=0.05),
            label("10⁻⁶ m", font_size=18).next_to([3.8, 0.2, 0], RIGHT, buff=0.05),
            label("10⁻¹⁰ m", font_size=18).next_to([3.8, -2.2, 0], RIGHT, buff=0.05),
        )
        self.play_t(Create(ruler), run_time=1.0)
        self.play_t(Create(ticks), run_time=1.2)
        self.play_t(FadeIn(ruler_labels), run_time=0.8)

        vis_dot = Dot([3.5, -0.4, 0], radius=0.07, color=BEAM)
        atom_dot = Dot([3.5, -2.2, 0], radius=0.07, color=MEASURE)
        vis = callout("可见光 400–700 nm", color=BEAM, font_size=18).move_to(RIGHT * 5.45 + DOWN * 0.4)
        atom_lab = callout("原子间距约 0.1–0.3 nm", color=MEASURE, font_size=18).move_to(RIGHT * 5.45 + DOWN * 2.75)
        self.play_t(FadeIn(vis_dot), FadeIn(atom_dot), run_time=0.6)
        self.play_t(FadeIn(atom_lab, shift=DOWN * 0.1), run_time=0.8)
        self.play_t(FadeIn(vis, shift=UP * 0.1), run_time=0.8)
        badge(self, "示意 · 尺度不按比例")
        self.wait_t(4.0)


        self.finish()

class S01(TimedScene):
    scene_id = "s01"

    def construct(self):
        kicker(self)
        section_title(self, "换一把尺子", y=2.75)

        # Two wavelength bands on a vertical ruler.
        ruler = Line(UP * 2.2 + LEFT * 4.7, DOWN * 2.4 + LEFT * 4.7, color=MUTED, stroke_width=2)
        vis_band = Rectangle(width=0.35, height=1.8, color=BEAM, fill_opacity=0.25).move_to(LEFT * 4.7 + UP * 1.25)
        x_band = Line(LEFT * 5.0 + DOWN * 1.55, LEFT * 4.4 + DOWN * 1.55, color=MEASURE, stroke_width=22).set_opacity(0.8)
        self.play_t(Create(ruler), run_time=0.8)
        self.play_t(FadeIn(vis_band), run_time=0.8)
        self.play_t(GrowFromCenter(x_band), run_time=0.8)
        vlab = label("可见光", font_size=22, color=BEAM).next_to(vis_band, RIGHT, buff=0.35)
        xlab = label("X 射线", font_size=22, color=MEASURE).next_to(x_band, RIGHT, buff=0.35)
        self.play_t(FadeIn(vlab), FadeIn(xlab), run_time=0.8)
        self.wait_t(2.0)

        # Lattice + incident wave + outgoing wavelets.
        lat = lattice(rows=3, cols=3, dx=1.05, dy=1.0, radius=0.10).move_to(UP * 0.35)
        clouds = VGroup(*[Circle(radius=0.20, color=BEAM, stroke_width=1).set_opacity(0.28).move_to(a.get_center()) for a in lat])
        incoming = wave((-5.2, 1.4), (-1.6, 0.5), wavelength=0.42, amplitude=0.13, color=BEAM, width=2.5)
        self.play_t(FadeIn(lat), FadeIn(clouds), run_time=1.0)
        self.play_t(Create(incoming), run_time=1.8)
        wavelets = VGroup()
        for a in lat:
            c = Circle(radius=0.2, color=BEAM, stroke_width=1).move_to(a.get_center())
            wavelets.add(c)
        self.play_t(LaggedStart(*[GrowFromPoint(c, c.get_center()) for c in wavelets], lag_ratio=0.04), run_time=2.5)
        self.play_t(FadeOut(incoming), run_time=0.5)

        # In-phase and out-of-phase directions.
        bright = Line(UP * 1.2 + LEFT * 1.0, DOWN * 1.0 + RIGHT * 2.0, color=MEASURE, stroke_width=4)
        dark = Line(DOWN * 0.2 + LEFT * 1.0, DOWN * 2.0 + RIGHT * 1.2, color=ALERT, stroke_width=2).set_opacity(0.55)
        bright_lab = label("相长", font_size=22, color=MEASURE).next_to(bright, RIGHT, buff=0.15)
        dark_lab = label("相消", font_size=22, color=ALERT).next_to(dark, RIGHT, buff=0.15)
        self.play_t(Create(bright), Create(dark), run_time=1.5)
        self.play_t(FadeIn(bright_lab), FadeIn(dark_lab), run_time=0.8)
        self.play_t(FadeOut(lat), FadeOut(clouds), FadeOut(wavelets), run_time=0.6)

        # Two sine waves, aligned and opposed.
        def s_wave(y, phase):
            return wave((-3.8, y), (3.8, y), wavelength=1.3, amplitude=0.22, phase=phase, color=INK, width=2)
        w1 = s_wave(0.9, 0.0)
        w2 = s_wave(0.2, 0.0)
        w3 = s_wave(-1.2, 0.0)
        w4 = s_wave(-1.9, math.pi)
        self.play_t(Create(w1), Create(w2), run_time=1.2)
        self.play_t(Create(w3), Create(w4), run_time=1.2)
        lab1 = label("同相：叠加", font_size=22, color=MEASURE).move_to(RIGHT * 3.0 + UP * 1.4)
        lab2 = label("反相：抵消", font_size=22, color=ALERT).move_to(RIGHT * 3.0 + DOWN * 1.1)
        self.play_t(FadeIn(lab1), FadeIn(lab2), run_time=0.8)
        badge(self, "示意 · 波前与散射")
        self.wait_t(3.0)


        self.finish()

class S02(TimedScene):
    scene_id = "s02"

    def construct(self):
        kicker(self)
        section_title(self, "布拉格条件", y=2.85)

        # Two adjacent planes and a ray path.
        planes = VGroup()
        for y in [1.15, 0.05, -1.05]:
            planes.add(Line(LEFT * 4.4 + UP * y, RIGHT * 3.4 + UP * y, color=MEASURE, stroke_width=2))
            for x in np.linspace(-4.2, 3.2, 8):
                planes.add(Dot([x, y, 0], radius=0.055, color=INK))
        hit_top = np.array([-1.1, 1.15, 0])
        hit_bot = np.array([-0.25, 0.05, 0])
        inc = Line(np.array([-5.0, 2.2, 0]), hit_top, color=BEAM, stroke_width=3)
        scat = Line(hit_top, np.array([2.4, 2.2, 0]), color=BEAM, stroke_width=3)
        inc2 = Line(np.array([-4.35, 1.9, 0]), hit_bot, color=BEAM, stroke_width=2).set_opacity(0.65)
        scat2 = Line(hit_bot, np.array([1.65, 1.9, 0]), color=BEAM, stroke_width=2).set_opacity(0.65)
        angle_arc = Arc(radius=0.7, start_angle=-16 * math.pi / 180, angle=32 * math.pi / 180,
                        arc_center=hit_top, color=MEASURE, stroke_width=2)
        theta = formula(r"\theta", font_size=32, color=MEASURE).move_to(hit_top + RIGHT * 0.95 + UP * 0.18)
        d_arrow = Arrow([0.55, 1.15, 0], [0.55, 0.05, 0], buff=0.02, color=MEASURE,
                        stroke_width=2, max_tip_length_to_length_ratio=0.15)
        d_lab = formula("d", font_size=32, color=MEASURE).next_to(d_arrow, RIGHT, buff=0.12)
        self.play_t(Create(planes), run_time=1.5)
        self.play_t(Create(inc), Create(scat), run_time=2.0)
        self.play_t(Create(inc2), Create(scat2), run_time=1.5)
        self.play_t(Create(angle_arc), FadeIn(theta), run_time=1.0)
        self.play_t(GrowFromPoint(d_arrow, d_arrow.get_start()), FadeIn(d_lab), run_time=1.0)
        self.wait_t(2.0)

        # Path difference and formula.
        extra1 = Line(np.array([-1.1, 1.15, 0]), np.array([-1.1, 0.05, 0]), color=ALERT, stroke_width=4)
        extra2 = Line(np.array([-0.25, 0.05, 0]), np.array([-0.25, 1.15, 0]), color=ALERT, stroke_width=4)
        self.play_t(Create(extra1), Create(extra2), run_time=1.5)
        f = formula(r"2d\sin\theta = n\lambda", font_size=72, color=INK).move_to(RIGHT * 2.5 + DOWN * 1.75)
        self.play_t(Write(f), run_time=2.0)
        note1 = label("相邻两层的光程差", font_size=20, color=MUTED).move_to(RIGHT * 2.5 + DOWN * 2.65)
        self.play_t(FadeIn(note1), run_time=0.8)
        self.wait_t(3.0)

        # Multilayer constructive addition.
        layers = VGroup()
        for i, y in enumerate(np.linspace(-1.4, 1.6, 7)):
            layers.add(Line(LEFT * 4.2 + UP * y, LEFT * 0.4 + UP * y, color=MEASURE, stroke_width=1.5).set_opacity(0.55))
        amps = VGroup()
        for i, y in enumerate(np.linspace(-1.4, 1.6, 7)):
            amps.add(Line(RIGHT * 0.8 + UP * y, RIGHT * (0.8 + 0.16 * (i + 1)) + UP * y,
                          color=BEAM, stroke_width=3))
        bright = Line(RIGHT * 2.0 + DOWN * 1.5, RIGHT * 2.0 + UP * 1.7, color=MEASURE, stroke_width=5)
        self.play_t(FadeIn(layers), run_time=1.0)
        self.play_t(LaggedStart(*[GrowFromPoint(a, a.get_start()) for a in amps], lag_ratio=0.12), run_time=2.0)
        self.play_t(Create(bright), run_time=1.0)
        add_lab = label("同相叠加", font_size=20, color=MEASURE).next_to(bright, RIGHT, buff=0.15)
        self.play_t(FadeIn(add_lab), run_time=0.8)
        self.wait_t(2.0)
        self.play_t(FadeOut(VGroup(planes, inc, scat, inc2, scat2, angle_arc, theta, d_arrow, d_lab,
                                   extra1, extra2, f, note1, layers, amps, bright, add_lab)), run_time=1.0)

        # The mirror misconception.
        mirror = Line(LEFT * 5.0 + DOWN * 0.6, LEFT * 1.5 + DOWN * 0.6, color=MUTED, stroke_width=4)
        in_ray = Line(LEFT * 4.6 + UP * 2.0, LEFT * 3.2 + DOWN * 0.55, color=BEAM, stroke_width=3)
        out_ray = Line(LEFT * 3.2 + DOWN * 0.55, LEFT * 1.8 + UP * 2.0, color=BEAM, stroke_width=3)
        mirror_lab = label("镜面反射", font_size=20, color=MUTED).next_to(mirror, DOWN, buff=0.2)
        cross = Line(LEFT * 4.9 + UP * 1.5, LEFT * 1.7 + DOWN * 1.4, color=ALERT, stroke_width=5)
        self.play_t(FadeIn(mirror), Create(in_ray), Create(out_ray), FadeIn(mirror_lab), run_time=1.2)
        self.play_t(Create(cross), run_time=0.8)

        # Real picture: many weak scattered waves, one phase-matched direction.
        center = RIGHT * 1.0 + DOWN * 0.1
        atoms = VGroup(*[Dot(center + RIGHT * 0.35 * i + UP * 0.25 * (i % 3), radius=0.06, color=INK) for i in range(6)])
        rays = VGroup()
        for i in range(12):
            ang = i * math.pi / 6
            end = center + np.array([math.cos(ang), math.sin(ang), 0]) * 1.1
            rays.add(Line(center, end, color=BEAM, stroke_width=1).set_opacity(0.25))
        phase_ray = Arrow(center, center + np.array([1.8, 1.15, 0]), buff=0.02, color=MEASURE, stroke_width=4)
        self.play_t(FadeIn(atoms), FadeIn(rays), run_time=1.2)
        self.play_t(GrowFromPoint(phase_ray, center), run_time=1.0)
        real_lab = label("原子向各方向发次波", font_size=20, color=BEAM).move_to(RIGHT * 2.8 + DOWN * 2.4)
        phase_lab = label("只有一个方向同相", font_size=20, color=MEASURE).move_to(RIGHT * 3.2 + UP * 2.0)
        self.play_t(FadeIn(real_lab), FadeIn(phase_lab), run_time=0.8)
        badge(self, "示意 · 布拉格几何模型")
        self.wait_t(5.0)


        self.finish()

class S03(TimedScene):
    scene_id = "s03"

    def construct(self):
        kicker(self)
        section_title(self, "粉末：用数量换角度", y=2.85)

        # Single crystal: rotate, one spot at a time.
        crystal = Polygon(UP * 0.55, RIGHT * 0.55 + UP * 0.2, RIGHT * 0.35 + DOWN * 0.5,
                          DOWN * 0.55, LEFT * 0.45 + DOWN * 0.35, LEFT * 0.5 + UP * 0.25,
                          color=BEAM, stroke_width=2, fill_color=BEAM, fill_opacity=0.08)
        crystal.scale(1.25).move_to(LEFT * 4.2 + UP * 0.5)
        stage_lab = label("单晶", font_size=20, color=MUTED).next_to(crystal, DOWN, buff=0.2)
        det_arc = Arc(radius=3.0, start_angle=-50 * math.pi / 180, angle=100 * math.pi / 180,
                      arc_center=LEFT * 1.3 + UP * 0.2, color=MUTED, stroke_width=2)
        spot = Dot(det_arc.point_from_proportion(0.55), radius=0.09, color=MEASURE)
        self.play_t(FadeIn(crystal), FadeIn(stage_lab), Create(det_arc), run_time=1.5)
        self.play_t(crystal.animate.rotate(2 * math.pi), run_time=7.0, rate_func=linear)
        self.play_t(GrowFromCenter(spot), run_time=0.8)
        self.wait_t(2.0)
        self.play_t(FadeOut(VGroup(crystal, stage_lab, det_arc, spot)), run_time=0.8)

        # Powder: many random grains, cones.
        rng = random.Random(4)
        grains = VGroup()
        for _ in range(38):
            x, y = rng.uniform(-5.2, -2.6), rng.uniform(-1.7, 1.9)
            s = rng.uniform(0.08, 0.16)
            ang = rng.uniform(0, math.pi)
            pts = [np.array([math.cos(ang) * s, math.sin(ang) * s, 0]),
                   np.array([-math.sin(ang) * s, math.cos(ang) * s, 0]),
                   np.array([-math.cos(ang) * s, -math.sin(ang) * s, 0]),
                   np.array([math.sin(ang) * s, -math.cos(ang) * s, 0])]
            grains.add(Polygon(*[p + np.array([x, y, 0]) for p in pts],
                               color=INK, stroke_width=1, fill_color=INK, fill_opacity=0.2))
        powder_lab = label("粉末：成千上万颗小晶粒", font_size=20, color=MUTED).move_to(LEFT * 4.0 + DOWN * 2.3)
        self.play_t(FadeIn(grains), FadeIn(powder_lab), run_time=1.2)
        sample = Dot([-2.8, 0.1, 0], radius=0.10, color=MEASURE)
        self.play_t(GrowFromCenter(sample), run_time=0.5)
        cone_colors = [BEAM, MEASURE, ALERT]
        cones = VGroup()
        for i, h in enumerate([0.8, 1.15, 1.55]):
            base = [2.0, 0.1, 0]
            lines = VGroup(Line(sample.get_center(), [base[0], base[1] + h, 0], color=cone_colors[i], stroke_width=2).set_opacity(0.8),
                           Line(sample.get_center(), [base[0], base[1] - h, 0], color=cone_colors[i], stroke_width=2).set_opacity(0.8))
            ell = Ellipse(width=0.32, height=2 * h, color=cone_colors[i], stroke_width=2, fill_opacity=0).move_to(base).set_stroke(opacity=0.85)
            cones.add(VGroup(lines, ell))
        self.play_t(LaggedStart(*[FadeIn(c, scale=0.9) for c in cones], lag_ratio=0.2), run_time=3.0)
        cone_lab = label("每一组晶面 → 一个圆锥", font_size=20, color=MEASURE).move_to(RIGHT * 1.4 + UP * 2.3)
        self.play_t(FadeIn(cone_lab), run_time=0.8)
        self.wait_t(4.0)

        # Detector scans the cones; a curve appears.
        self.play_t(FadeOut(VGroup(grains, powder_lab, cones, cone_lab, sample)), run_time=0.8)
        ax, ax_labels = axes_2theta((10, 90, 10), (0, 110, 50), width=8.2, height=2.7)
        ax.move_to(DOWN * 1.0)
        ax_labels[0].next_to(ax.x_axis, DOWN, buff=0.12)
        ax_labels[1].next_to(ax.y_axis, LEFT, buff=0.12)
        self.play_t(Create(ax), FadeIn(ax_labels), run_time=1.2)
        peaks = [{"two_theta": 22, "intensity": 45}, {"two_theta": 33, "intensity": 100},
                 {"two_theta": 47, "intensity": 62}, {"two_theta": 61, "intensity": 30},
                 {"two_theta": 76, "intensity": 18}]
        pat = pattern_group(ax, peaks, fwhm=0.7, color=BEAM, max_height=100)
        self.play_t(Create(pat), run_time=4.0)
        xlab = label("强度随衍射角变化", font_size=20, color=MUTED).move_to(RIGHT * 2.3 + UP * 2.3)
        self.play_t(FadeIn(xlab), run_time=0.8)
        badge(self, "示意 · 衍射圆锥与扫描曲线")
        self.wait_t(4.0)


        self.finish()

class S04(TimedScene):
    scene_id = "s04"

    def construct(self):
        kicker(self)
        section_title(self, "峰位：先看峰在哪", y=2.85)

        ax, ax_labels = axes_2theta((10, 90, 10), (0, 110, 50), width=8.2, height=2.9)
        ax.move_to(DOWN * 0.65)
        ax_labels[0].next_to(ax.x_axis, DOWN, buff=0.12)
        ax_labels[1].next_to(ax.y_axis, LEFT, buff=0.12)
        peaks = [{"two_theta": 28.4, "intensity": 100}, {"two_theta": 47.3, "intensity": 62},
                 {"two_theta": 56.1, "intensity": 38}, {"two_theta": 69.1, "intensity": 12}]
        pat = pattern_group(ax, peaks, fwhm=0.7, color=BEAM, max_height=100)
        self.play_t(Create(ax), FadeIn(ax_labels), run_time=1.2)
        self.play_t(Create(pat), run_time=3.0)
        self.wait_t(2.0)

        # Mark the first peak and drop a line to the angle axis.
        x0 = 28.4
        top = ax.c2p(x0, 100)
        base = ax.c2p(x0, 0)
        marker = Line(base, top, color=MEASURE, stroke_width=3)
        ring = Circle(radius=0.12, color=MEASURE, stroke_width=2).move_to(top)
        self.play_t(Create(marker), GrowFromCenter(ring), run_time=1.2)
        d_lab = formula("d", font_size=40, color=MEASURE).move_to(RIGHT * 1.8 + UP * 1.4)
        formula_1 = formula(r"2d\sin\theta = n\lambda", font_size=50, color=INK).move_to(RIGHT * 2.2 + UP * 0.7)
        self.play_t(FadeIn(d_lab), Write(formula_1), run_time=1.5)
        self.wait_t(2.0)

        # A unit cell with a, b, c.
        self.play_t(FadeOut(VGroup(pat, marker, ring, d_lab, formula_1, ax, ax_labels)), run_time=0.8)
        cell = simple_unit_cell(center=[0.4, 0.2, 0], scale=1.35, color=MEASURE)
        cell_dots = VGroup(
            Dot([0.4, 0.2, 0], radius=0.07, color=INK),
            Dot([1.68, 0.44, 0], radius=0.07, color=INK),
            Dot([0.4, 1.55, 0], radius=0.07, color=INK),
            Dot([1.01, 0.94, 0], radius=0.07, color=INK),
        )
        cell_group = VGroup(cell, cell_dots)
        self.play_t(Create(cell), FadeIn(cell_dots), run_time=1.5)
        a_lab = formula("a", font_size=30, color=MEASURE).move_to(RIGHT * 1.15 + DOWN * 0.1)
        b_lab = formula("b", font_size=30, color=MEASURE).move_to(RIGHT * 0.15 + UP * 1.0)
        c_lab = formula("c", font_size=30, color=MEASURE).move_to(RIGHT * 1.55 + UP * 1.35)
        self.play_t(FadeIn(VGroup(a_lab, b_lab, c_lab)), run_time=0.8)
        flow = label("峰位  →  晶面间距 d  →  晶胞", font_size=22, color=MEASURE).move_to(LEFT * 2.8 + DOWN * 0.7)
        self.play_t(FadeIn(flow), run_time=0.8)
        cell_note = label("晶胞：形状 + 大小", font_size=20, color=MUTED).move_to(DOWN * 2.35)
        self.play_t(FadeIn(cell_note), run_time=0.8)

        # Experimental caveat.
        caveat = label("样品高度 / 仪器零点 → 峰整体偏移", font_size=18, color=ALERT).move_to(DOWN * 2.85)
        self.play_t(FadeIn(caveat), run_time=0.8)
        badge(self, "示意 · 晶胞参数")
        self.wait_t(4.0)


        self.finish()

class S05(TimedScene):
    scene_id = "s05"

    def construct(self):
        kicker(self)
        section_title(self, "峰高：没那么老实", y=2.85)

        # Two cells: light vs heavy atoms.
        left_cell = simple_unit_cell(center=[-4.0, 0.2, 0], scale=1.15, color=MEASURE)
        left_atoms = VGroup(*[Dot([-4.0 + x, 0.2 + y, 0], radius=0.075, color=MUTED)
                              for x, y in [(0, 0), (1.1, 0.2), (0, 1.15), (0.55, 0.65)]])
        right_cell = simple_unit_cell(center=[-1.6, 0.2, 0], scale=1.15, color=MEASURE)
        right_atoms = VGroup(*[Dot([-1.6 + x, 0.2 + y, 0], radius=0.13, color=MEASURE)
                               for x, y in [(0, 0), (1.1, 0.2), (0, 1.15), (0.55, 0.65)]])
        self.play_t(Create(left_cell), FadeIn(left_atoms), run_time=1.0)
        self.play_t(Create(right_cell), FadeIn(right_atoms), run_time=1.0)
        light_lab = label("轻原子", font_size=20, color=MUTED).next_to(left_cell, DOWN, buff=0.15)
        heavy_lab = label("重原子", font_size=20, color=MEASURE).next_to(right_cell, DOWN, buff=0.15)
        self.play_t(FadeIn(light_lab), FadeIn(heavy_lab), run_time=0.8)

        # Peak bars.
        bar1 = Rectangle(width=0.5, height=0.6, color=MUTED, fill_opacity=0.4).move_to(RIGHT * 1.2 + DOWN * 1.2)
        bar2 = Rectangle(width=0.5, height=1.5, color=MEASURE, fill_opacity=0.55).move_to(RIGHT * 2.1 + DOWN * 0.75)
        bar_lab = label("峰高", font_size=20, color=MUTED).move_to(RIGHT * 1.65 + DOWN * 2.0)
        self.play_t(GrowFromPoint(bar1, bar1.get_bottom()), GrowFromPoint(bar2, bar2.get_bottom()), run_time=1.2)
        self.play_t(FadeIn(bar_lab), run_time=0.6)
        self.wait_t(2.0)

        # Phasors: add and cancel.
        origin = np.array([2.2, 0.6, 0])
        arrows = VGroup()
        for ang, length, col in [(20, 0.9, BEAM), (65, 0.8, BEAM), (150, 0.85, ALERT), (205, 0.8, ALERT)]:
            end = origin + np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang)), 0]) * length
            arrows.add(Arrow(origin, end, buff=0.02, color=col, stroke_width=3, max_tip_length_to_length_ratio=0.16))
        sum_arrow = Arrow(origin, origin + np.array([1.2, 0.6, 0]), buff=0.02, color=MEASURE,
                          stroke_width=4, max_tip_length_to_length_ratio=0.14)
        self.play_t(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=2.0)
        self.play_t(GrowArrow(sum_arrow), run_time=1.0)
        phasor_lab = label("结构因子：相加 / 抵消", font_size=19, color=MUTED).move_to(RIGHT * 3.2 + DOWN * 2.2)
        self.play_t(FadeIn(phasor_lab), run_time=0.8)
        self.wait_t(2.0)

        # Preferred orientation: flat platelets lie down.
        self.play_t(FadeOut(VGroup(left_cell, right_cell, left_atoms, right_atoms, light_lab, heavy_lab,
                                   bar1, bar2, bar_lab, arrows, sum_arrow, phasor_lab)), run_time=0.8)
        random_plates = VGroup()
        rng = random.Random(3)
        for i in range(8):
            x, y = rng.uniform(-5.5, -2.5), rng.uniform(-1.5, 1.5)
            ang = rng.uniform(0, math.pi)
            e = Ellipse(width=0.7, height=0.16, color=BEAM, fill_opacity=0.25).rotate(ang).move_to([x, y, 0])
            random_plates.add(e)
        aligned = VGroup()
        for i in range(8):
            x = -1.0 + (i % 4) * 0.65
            y = -1.0 + (i // 4) * 0.45
            aligned.add(Ellipse(width=0.7, height=0.16, color=MEASURE, fill_opacity=0.35).move_to([x + 1.0, y, 0]))
        self.play_t(FadeIn(random_plates), run_time=1.0)
        self.play_t(FadeIn(aligned), run_time=1.0)
        lab1 = label("随机取向", font_size=20, color=BEAM).move_to(LEFT * 4.0 + DOWN * 2.2)
        lab2 = label("片状晶粒平躺：择优取向", font_size=20, color=MEASURE).move_to(RIGHT * 2.4 + DOWN * 2.2)
        self.play_t(FadeIn(lab1), FadeIn(lab2), run_time=0.8)
        badge(self, "示意 · 峰高与择优取向")
        self.wait_t(4.0)


        self.finish()

class S06(TimedScene):
    scene_id = "s06"

    def construct(self):
        kicker(self)
        section_title(self, "峰宽：与晶粒有关", y=2.85)

        # Large vs small crystallite.
        big = Polygon(UP * 0.8, RIGHT * 0.7 + UP * 0.25, RIGHT * 0.45 + DOWN * 0.6,
                      DOWN * 0.5, LEFT * 0.55 + DOWN * 0.35, LEFT * 0.6 + UP * 0.45,
                      color=MEASURE, stroke_width=2, fill_color=MEASURE, fill_opacity=0.10).move_to(LEFT * 4.5 + UP * 1.2)
        small = Circle(radius=0.28, color=BEAM, stroke_width=2, fill_color=BEAM, fill_opacity=0.12).move_to(RIGHT * 4.4 + UP * 1.2)
        big_lab = label("大晶粒", font_size=20, color=MEASURE).next_to(big, DOWN, buff=0.15)
        small_lab = label("小晶粒", font_size=20, color=BEAM).next_to(small, DOWN, buff=0.15)
        self.play_t(FadeIn(big), FadeIn(small), FadeIn(big_lab), FadeIn(small_lab), run_time=1.2)

        ax, ax_labels = axes_2theta((20, 90, 10), (0, 110, 50), width=8.2, height=2.9)
        ax.move_to(DOWN * 0.9)
        ax_labels[0].next_to(ax.x_axis, DOWN, buff=0.12)
        ax_labels[1].next_to(ax.y_axis, LEFT, buff=0.12)
        sharp = ax.plot(lambda x: peak_shape(x, 42, 0.35, 100), x_range=[20, 90], color=MEASURE, stroke_width=2.5)
        broad = ax.plot(lambda x: peak_shape(x, 42, 1.0, 100), x_range=[20, 90], color=BEAM, stroke_width=2.5)
        self.play_t(Create(ax), FadeIn(ax_labels), run_time=1.0)
        self.play_t(Create(sharp), run_time=1.5)
        self.play_t(Create(broad), run_time=1.5)
        left_lab = label("峰窄", font_size=18, color=MEASURE).next_to(sharp, UP, buff=0.1)
        right_lab = label("峰宽", font_size=18, color=BEAM).next_to(broad, UP, buff=0.1)
        self.play_t(FadeIn(left_lab), FadeIn(right_lab), run_time=0.8)
        self.wait_t(2.0)

        # Contributions to the observed width.
        self.play_t(FadeOut(VGroup(big, small, big_lab, small_lab, sharp, broad, left_lab, right_lab, ax, ax_labels)), run_time=0.8)
        title2 = label("观测到的峰宽，来自几件事", font_size=24, color=INK).move_to(UP * 2.2)
        self.play_t(FadeIn(title2), run_time=0.8)
        contributions = [
            ("仪器展宽", 0.55, MUTED),
            ("晶粒尺寸", 1.45, BEAM),
            ("应变 / 缺陷", 1.05, ALERT),
        ]
        bars = VGroup()
        for i, (name, length, col) in enumerate(contributions):
            y = 0.9 - i * 0.85
            bar = Rectangle(width=length, height=0.18, color=col, fill_opacity=0.55).move_to(LEFT * 3.0 + RIGHT * length / 2 + UP * y)
            bars.add(bar)
            bars.add(label(name, font_size=20, color=col).next_to(bar, LEFT, buff=0.2))
        self.play_t(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars], lag_ratio=0.12), run_time=2.0)
        total = Line(LEFT * 3.0 + DOWN * 1.7, LEFT * 3.0 + RIGHT * 3.2 + DOWN * 1.7, color=INK, stroke_width=4)
        total_lab = label("观测峰宽", font_size=20, color=INK).next_to(total, DOWN, buff=0.15)
        self.play_t(Create(total), FadeIn(total_lab), run_time=1.0)
        self.wait_t(2.0)

        # Scherrer + instrument subtraction.
        self.play_t(FadeOut(VGroup(bars, total, total_lab, title2)), run_time=0.8)
        scherrer = formula(r"\beta = \frac{K\lambda}{L\cos\theta}", font_size=58, color=INK).move_to(LEFT * 2.4 + UP * 0.6)
        self.play_t(Write(scherrer), run_time=1.8)
        std = RoundedRectangle(width=0.9, height=0.9, corner_radius=0.08, color=MUTED, fill_opacity=0.15).move_to(RIGHT * 2.5 + UP * 0.7)
        std_lab = label("标样", font_size=18, color=MUTED).next_to(std, DOWN, buff=0.12)
        arr = Arrow(std.get_right(), std.get_right() + RIGHT * 0.8, buff=0.05, color=MEASURE, stroke_width=2)
        arr_lab = label("扣除仪器展宽", font_size=18, color=MEASURE).next_to(arr, UP, buff=0.08)
        self.play_t(FadeIn(std), FadeIn(std_lab), run_time=0.8)
        self.play_t(Create(arr), FadeIn(arr_lab), run_time=0.8)
        note1 = label("单峰 → 法向厚度，不一定是颗粒直径", font_size=20, color=ALERT).move_to(DOWN * 2.55)
        self.play_t(FadeIn(note1), run_time=0.8)
        badge(self, "示意 · 峰宽与谢乐公式")
        self.wait_t(4.0)


        self.finish()

class S07(TimedScene):
    scene_id = "s07"

    def construct(self):
        kicker(self)
        section_title(self, "两张图：硅与金红石", y=2.9)

        def panel(center_x, phase_id, phase_name, sub, peak_labels, color):
            ax, ax_labels = axes_2theta((20, 90, 10), (0, 110, 50), width=4.6, height=2.5)
            ax.move_to([center_x, -0.55, 0])
            ax_labels[0].scale(0.85).next_to(ax.x_axis, DOWN, buff=0.08)
            ax_labels[1].scale(0.85).next_to(ax.y_axis, LEFT, buff=0.08)
            pat = pattern_group(ax, PEAKS[phase_id], fwhm=0.55, color=color, max_height=100)
            name = formula(phase_name, font_size=38, color=color).move_to([center_x - 0.7, 2.25, 0])
            sub_lab = label(sub, font_size=18, color=MUTED).next_to(name, RIGHT, buff=0.2)
            return ax, ax_labels, pat, name, sub_lab

        ax_l, lab_l, pat_l, name_l, sub_l = panel(-3.45, "Si", "Si", "金刚石立方", ["111", "220", "311"], BEAM)
        ax_r, lab_r, pat_r, name_r, sub_r = panel(3.45, "rutile", r"TiO_2", "金红石 · 四方", ["110", "101", "111"], MEASURE)
        self.play_t(FadeIn(name_l), FadeIn(name_r), FadeIn(sub_l), FadeIn(sub_r), run_time=1.0)
        self.play_t(Create(ax_l), Create(ax_r), FadeIn(lab_l), FadeIn(lab_r), run_time=1.5)
        self.play_t(Create(pat_l), run_time=4.0)
        self.wait_t(2.0)
        self.play_t(Create(pat_r), run_time=5.0)
        self.wait_t(3.0)

        # Label the first strong peaks.
        def peak_label(ax, x, intensity, text, color, dy=0.18):
            p = ax.c2p(x, intensity)
            dot = Dot(p, radius=0.05, color=color)
            lab = label(text, font_size=17, color=color).next_to(dot, UP, buff=dy)
            return VGroup(dot, lab)

        labels_l = VGroup(
            peak_label(ax_l, 28.44, 100, "111", BEAM),
            peak_label(ax_l, 47.31, 67, "220", BEAM),
            peak_label(ax_l, 56.13, 40, "311", BEAM),
        )
        labels_r = VGroup(
            peak_label(ax_r, 27.44, 100, "110", MEASURE),
            peak_label(ax_r, 36.08, 67, "101", MEASURE),
            peak_label(ax_r, 39.20, 18, "200", MEASURE),
        )
        self.play_t(FadeIn(labels_l), FadeIn(labels_r), run_time=1.2)
        compare = label("峰位组合 = 物相的指纹", font_size=24, color=INK).move_to(DOWN * 2.55)
        self.play_t(FadeIn(compare), run_time=0.8)
        badge(self, "COD 结构计算 · 非实测 · Cu Kα1")
        self.wait_t(5.0)


        self.finish()

class S08(TimedScene):
    scene_id = "s08"

    def construct(self):
        kicker(self)
        section_title(self, "边界：它喜欢整齐的东西", y=2.9)

        # Ordered vs disordered.
        ordered = lattice(rows=4, cols=4, dx=0.75, dy=0.75, radius=0.07).move_to(LEFT * 4.3 + UP * 0.6)
        rng = random.Random(8)
        disordered = VGroup(*[Dot([-1.4 + rng.uniform(-1.0, 1.0), 0.6 + rng.uniform(-1.0, 1.0), 0],
                                  radius=0.06, color=INK).set_opacity(rng.uniform(0.3, 0.9)) for _ in range(35)])
        ol = label("长程有序 → 尖峰", font_size=20, color=BEAM).next_to(ordered, DOWN, buff=0.3)
        dl = label("无序 → 鼓包", font_size=20, color=ALERT).next_to(disordered, DOWN, buff=0.3)
        self.play_t(FadeIn(ordered), FadeIn(disordered), FadeIn(ol), FadeIn(dl), run_time=1.5)
        self.wait_t(6.0)

        # Beam footprint over several phases.
        self.play_t(FadeOut(VGroup(ordered, disordered, ol, dl)), run_time=0.8)
        grains = VGroup()
        colors = [BEAM, MEASURE, ALERT]
        for i in range(3):
            g = RoundedRectangle(width=2.0, height=1.8, corner_radius=0.15,
                                 color=colors[i], fill_color=colors[i], fill_opacity=0.10)
            g.move_to(LEFT * 2.6 + RIGHT * i * 2.1 + UP * 0.5)
            grains.add(g)
        beam = Circle(radius=1.5, color=INK, stroke_width=2).set_opacity(0.7).move_to(UP * 0.5)
        beam.set_fill(INK, opacity=0.04)
        self.play_t(FadeIn(grains), run_time=1.0)
        self.play_t(FadeIn(beam), run_time=1.0)
        avg = label("束斑里是平均：少量相可能被淹没", font_size=21, color=MUTED).move_to(DOWN * 2.3)
        self.play_t(FadeIn(avg), run_time=0.8)
        self.wait_t(4.0)

        # Light elements and hydrogen.
        self.play_t(FadeOut(VGroup(grains, beam, avg)), run_time=0.8)
        atoms = VGroup()
        for i in range(6):
            col = MEASURE if i % 2 == 0 else MUTED
            r = 0.16 if i % 2 == 0 else 0.08
            atoms.add(Dot([-4.0 + i * 1.3, 0.9, 0], radius=r, color=col))
        h = Dot([-4.0 + 6 * 1.3, 0.9, 0], radius=0.045, color=ALERT).set_opacity(0.6)
        atoms.add(h)
        hlab = label("H", font_size=18, color=ALERT).next_to(h, UP, buff=0.08)
        self.play_t(FadeIn(atoms), FadeIn(hlab), run_time=1.0)
        light_lab = label("轻元素散射弱；氢几乎看不见", font_size=22, color=MUTED).move_to(DOWN * 1.8)
        self.play_t(FadeIn(light_lab), run_time=0.8)
        self.wait_t(3.0)

        # Convenience and the average/local boundary.
        self.play_t(FadeOut(VGroup(atoms, h, hlab, light_lab)), run_time=0.8)
        holder = powder_holder(width=3.8, height=1.5, seed=5).move_to(LEFT * 3.5 + UP * 0.3)
        check = label("✓ 通常压片即可", font_size=22, color=BEAM).next_to(holder, RIGHT, buff=0.35)
        check2 = label("不需切开 / 抽真空", font_size=20, color=MUTED).next_to(check, DOWN, buff=0.12)
        self.play_t(FadeIn(holder), FadeIn(check), FadeIn(check2), run_time=1.0)
        line = Line(UP * 1.8 + RIGHT * 0.4, DOWN * 1.8 + RIGHT * 0.4, color=GRID, stroke_width=2)
        avg2 = label("擅长：平均结构", font_size=22, color=BEAM).move_to(RIGHT * 2.6 + UP * 0.7)
        local2 = label("很难：局部缺陷", font_size=22, color=ALERT).move_to(RIGHT * 2.6 + DOWN * 0.7)
        self.play_t(Create(line), FadeIn(avg2), FadeIn(local2), run_time=1.0)
        badge(self, "示意 · 平均与局域")
        self.wait_t(4.0)


        self.finish()

class S09(TimedScene):
    scene_id = "s09"

    def construct(self):
        kicker(self)
        section_title(self, "换一种眼睛", y=2.9)

        # X-ray beam fades out.
        xray = Line(LEFT * 4.2 + UP * 0.5, RIGHT * 2.0 + UP * 0.5, color=BEAM, stroke_width=4)
        xlab = label("X 射线：平均结构", font_size=20, color=BEAM).next_to(xray, UP, buff=0.2)
        self.play_t(Create(xray), FadeIn(xlab), run_time=1.0)
        self.wait_t(1.5)
        self.play_t(FadeOut(xray), FadeOut(xlab), run_time=0.8)

        # Electron column: beam, two lenses, thin sample and an image.
        beam = Line(UP * 2.2, DOWN * 0.4, color=INK, stroke_width=3)
        lens1 = Ellipse(width=2.0, height=0.35, color=MEASURE, stroke_width=2).move_to(UP * 1.35)
        lens2 = Ellipse(width=1.6, height=0.30, color=MEASURE, stroke_width=2).move_to(UP * 0.65)
        sample = Rectangle(width=2.0, height=0.16, color=BEAM, fill_opacity=0.25).move_to(DOWN * 0.45)
        screen = Rectangle(width=3.4, height=2.2, color=GRID, stroke_width=2, fill_opacity=0.05).move_to(DOWN * 2.2)
        lattice_img = lattice(rows=3, cols=4, dx=0.45, dy=0.45, radius=0.05).move_to(DOWN * 2.2)
        defect = Dot([0.4, -2.2, 0], radius=0.10, color=ALERT)
        trajectories = VGroup(
            Line(UP * 0.9 + LEFT * 0.8, DOWN * 0.45 + LEFT * 0.5, color=BEAM, stroke_width=1.5),
            Line(UP * 0.9, DOWN * 0.45, color=BEAM, stroke_width=1.5),
            Line(UP * 0.9 + RIGHT * 0.8, DOWN * 0.45 + RIGHT * 0.5, color=BEAM, stroke_width=1.5),
        )
        self.play_t(Create(beam), run_time=0.8)
        self.play_t(FadeIn(lens1), FadeIn(lens2), run_time=1.0)
        self.play_t(Create(trajectories), FadeIn(sample), run_time=1.0)
        self.play_t(FadeIn(screen), FadeIn(lattice_img), FadeIn(defect), run_time=1.5)
        elab = label("电子束 + 磁透镜 → 实空间成像", font_size=20, color=BEAM).move_to(DOWN * 2.1)
        self.play_t(FadeIn(elab), run_time=0.8)
        self.wait_t(3.0)

        # Next episode card.
        self.play_t(FadeOut(VGroup(beam, lens1, lens2, sample, screen, lattice_img, defect, trajectories, elab)), run_time=0.8)
        next_kicker = label("看见原子 · 第二期", font_size=22, color=BEAM).move_to(UP * 1.7)
        next_title = title("电子显微镜", font_size=64).move_to(UP * 0.7)
        next_sub = body("如何把原子“拍”出来？", font_size=34, color=INK).move_to(DOWN * 0.1)
        next_line = Line(LEFT * 2.6 + DOWN * 1.0, RIGHT * 2.6 + DOWN * 1.0, color=MEASURE, stroke_width=2)
        self.play_t(FadeIn(next_kicker), FadeIn(next_title), FadeIn(next_sub), Create(next_line), run_time=2.0)
        self.wait_t(3.0)
        self.finish()

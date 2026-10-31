"""Shared visual helpers for the S01 scenes."""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

from manim import (
    DOWN, LEFT, RIGHT, UP, Arrow, Axes, Circle, Create, Dot, FadeIn, FadeOut,
    GrowFromCenter, Line, ParametricFunction, Polygon, Rectangle, RoundedRectangle,
    Scene, Text, Transform, VGroup, Write, YELLOW, config,
)

from src.render.tex import S01_TEX_TEMPLATE  # noqa: E402
from src.render.theme import COLORS, body, credit, label, title  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
TIMING = ROOT / "chapters" / "s01" / "audio" / "timing.json"

BG = COLORS["bg"]
INK = COLORS["ink"]
MUTED = COLORS["muted"]
BEAM = COLORS["beam"]
MEASURE = COLORS["measure"]
ALERT = COLORS["alert"]
GRID = COLORS["grid"]


def read_timing() -> dict:
    return json.loads(TIMING.read_text(encoding="utf-8"))


def scene_duration(scene_id: str, extra_tail: float = 0.5) -> float:
    if scene_id == "s10":
        return 78.0
    data = read_timing()
    scenes = data["scenes"]
    for i, s in enumerate(scenes):
        if s["id"] == scene_id:
            if i + 1 < len(scenes):
                return float(scenes[i + 1]["start"] - s["start"])
            return float(s["duration"] + extra_tail)
    return 30.0


class TimedScene(Scene):
    scene_id = "s00"

    def setup(self):
        self.target = scene_duration(self.scene_id)
        self.elapsed = 0.0
        self.camera.background_color = BG

    def play_t(self, *anims, run_time: float = 1.0, **kwargs):
        self.play(*anims, run_time=run_time, **kwargs)
        self.elapsed += run_time

    def wait_t(self, t: float):
        if t <= 0:
            return
        self.wait(t)
        self.elapsed += t

    def finish(self):
        self.wait_t(max(0.15, self.target - self.elapsed))


def badge(scene: Scene, text: str, color: str = MUTED):
    t = credit(text, font_size=17, color=color)
    t.to_corner(DOWN + LEFT, buff=0.35)
    scene.add(t)
    return t


def kicker(scene: Scene, text: str = "看见原子 · 第一期"):
    t = label(text, color=BEAM, font_size=22)
    t.to_corner(UP + LEFT, buff=0.55)
    scene.add(t)
    return t


def section_title(scene: Scene, text: str, y: float = 2.55):
    t = title(text, font_size=44)
    t.move_to(UP * y)
    scene.add(t)
    return t


def note(scene: Scene, text: str, y: float = -2.85, color: str = MUTED):
    t = label(text, color=color, font_size=20)
    t.move_to(DOWN * 2.85 + UP * (y + 2.85))
    scene.add(t)
    return t


def powder_holder(width: float = 8.6, height: float = 3.5, seed: int = 7) -> VGroup:
    rng = random.Random(seed)
    holder = RoundedRectangle(
        width=width, height=height, corner_radius=0.25,
        stroke_color=MEASURE, stroke_width=2, fill_color="#151C2E", fill_opacity=1,
    )
    inner = RoundedRectangle(
        width=width - 0.35, height=height - 0.35, corner_radius=0.18,
        stroke_color=GRID, stroke_width=1, fill_color="#D9D4C7", fill_opacity=0.12,
    )
    dots = VGroup()
    for _ in range(650):
        x = rng.uniform(-width / 2 + 0.3, width / 2 - 0.3)
        y = rng.uniform(-height / 2 + 0.3, height / 2 - 0.3)
        r = rng.uniform(0.012, 0.045)
        c = rng.choice(["#E8E1D2", "#CFC7B8", "#F5EFE3", "#BDB5A6"])
        d = Dot([x, y, 0], radius=r, color=c).set_opacity(rng.uniform(0.35, 0.9))
        dots.add(d)
    # A few scrape marks, intentionally imperfect.
    marks = VGroup()
    for i in range(4):
        y = rng.uniform(-height / 3, height / 3)
        x0 = rng.uniform(-width / 3, 0)
        x1 = rng.uniform(0, width / 2.5)
        marks.add(Line([x0, y, 0], [x1, y + rng.uniform(-0.06, 0.06), 0],
                       color="#F5EFE3", stroke_width=1).set_opacity(0.12))
    return VGroup(holder, inner, dots, marks)


def lattice(rows: int = 4, cols: int = 5, dx: float = 1.0, dy: float = 0.9,
            radius: float = 0.09, color: str = INK) -> VGroup:
    g = VGroup()
    for i in range(rows):
        for j in range(cols):
            g.add(Dot([(j - (cols - 1) / 2) * dx, (i - (rows - 1) / 2) * dy, 0],
                      radius=radius, color=color))
    return g


def wave(start, end, wavelength=1.0, amplitude=0.18, phase=0.0, color=BEAM, width=3):
    x0, y0 = start
    x1, y1 = end
    length = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / length, (y1 - y0) / length
    nx, ny = -uy, ux

    def f(t):
        s = t * length
        return [
            x0 + ux * s + nx * amplitude * math.sin(2 * math.pi * s / wavelength + phase),
            y0 + uy * s + ny * amplitude * math.sin(2 * math.pi * s / wavelength + phase),
            0,
        ]

    return ParametricFunction(f, t_range=[0, 1], color=color, stroke_width=width)


def axes_2theta(x_range=(15, 95, 10), y_range=(0, 110, 50), width=8.4, height=3.2):
    ax = Axes(
        x_range=list(x_range), y_range=list(y_range),
        x_length=width, y_length=height, tips=False,
        axis_config={"color": MUTED, "stroke_width": 1.5, "include_numbers": False},
    )
    xlab = label("衍射角 2θ", font_size=20).next_to(ax.x_axis, DOWN, buff=0.18)
    ylab = label("强度", font_size=20).rotate(90 * math.pi / 180).next_to(ax.y_axis, LEFT, buff=0.20)
    return ax, VGroup(xlab, ylab)


def peak_shape(x, center, fwhm=0.55, height=100.0):
    sigma = fwhm / 2.3548
    return height * math.exp(-0.5 * ((x - center) / sigma) ** 2)


def pattern_group(ax: Axes, peaks, fwhm=0.6, color=BEAM, max_height=100.0):
    """Draw an open calculated reference pattern as sticks (PDF-card style)."""
    peaks = [p for p in peaks if p.get("intensity", 0) >= 1.0]
    baseline = Line(ax.c2p(20, 0), ax.c2p(90, 0), color=MUTED, stroke_width=1.2)
    sticks = VGroup()
    for p in peaks:
        h = max_height * p["intensity"] / max(1.0, max(q["intensity"] for q in peaks))
        sticks.add(Line(ax.c2p(p["two_theta"], 0), ax.c2p(p["two_theta"], h),
                        color=color, stroke_width=3))
    return VGroup(baseline, sticks)


def formula(tex: str, font_size: float = 64, color: str = INK):
    from manim import MathTex
    return MathTex(tex, tex_template=S01_TEX_TEMPLATE, font_size=font_size, color=color)


def simple_unit_cell(center=(0, 0, 0), scale=1.2, color=MEASURE):
    """A 2D oblique projection of a unit cell."""
    c = [center[0], center[1], 0]
    a = [0.95 * scale, 0.18 * scale, 0]
    b = [0.0, 1.0 * scale, 0]
    d = [0.45 * scale, 0.55 * scale, 0]
    o = c
    p1 = [o[0] + a[0], o[1] + a[1], 0]
    p2 = [o[0] + b[0], o[1] + b[1], 0]
    p3 = [o[0] + d[0], o[1] + d[1], 0]
    p4 = [o[0] + a[0] + b[0], o[1] + a[1] + b[1], 0]
    p5 = [o[0] + a[0] + d[0], o[1] + a[1] + d[1], 0]
    p6 = [o[0] + b[0] + d[0], o[1] + b[1] + d[1], 0]
    p7 = [o[0] + a[0] + b[0] + d[0], o[1] + a[1] + b[1] + d[1], 0]
    edges = VGroup(
        Line(o, p1, color=color, stroke_width=2), Line(o, p2, color=color, stroke_width=2),
        Line(o, p3, color=color, stroke_width=2), Line(p1, p4, color=color, stroke_width=2),
        Line(p2, p4, color=color, stroke_width=2), Line(p1, p5, color=color, stroke_width=2),
        Line(p3, p5, color=color, stroke_width=2), Line(p2, p6, color=color, stroke_width=2),
        Line(p3, p6, color=color, stroke_width=2), Line(p4, p7, color=color, stroke_width=2),
        Line(p5, p7, color=color, stroke_width=2), Line(p6, p7, color=color, stroke_width=2),
    )
    return VGroup(edges)


def callout(text: str, color: str = MEASURE, font_size: int = 22):
    return body(text, font_size=font_size, color=color)


def arrow_between(start, end, color=MEASURE, width=3):
    return Arrow(start, end, buff=0.08, color=color, stroke_width=width, max_tip_length_to_length_ratio=0.12)


def clear_scene(scene: Scene, *mobjects, run_time=0.4):
    if mobjects:
        scene.play_t(*[FadeOut(m) for m in mobjects], run_time=run_time)

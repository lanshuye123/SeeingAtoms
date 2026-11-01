"""Small, reusable effects for the S02 Manim scenes.

The reference is 3Blue1Brown's habit of letting the camera and a single
continuous transformation carry an idea, rather than stacking decorative
effects. The helpers here are deliberately few:

* `radial_glow`      soft phosphor/beam bloom
* `lattice_3d`       isometric atom lattice (static, readable)
* `column_3d`        a column of atoms that can rotate from top view to side view
* `focus_dial`       a knob whose pointer follows a focus parameter
* `plate`            text on a translucent plate, so labels survive busy frames

All positions are in Manim world units (default frame is 14.22 x 8).
"""
from __future__ import annotations

import math

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, Circle, Dot, Line, Rectangle, RoundedRectangle,
    VGroup, always_redraw, interpolate_color,
)

from src.render.theme import COLORS, body, label

BG = COLORS["bg"]
INK = COLORS["ink"]
MUTED = COLORS["muted"]
BEAM = COLORS["beam"]
MEASURE = COLORS["measure"]
ALERT = COLORS["alert"]
GRID = COLORS["grid"]


def radial_glow(center, radius: float, color: str = BEAM,
                layers: int = 7, max_opacity: float = 0.30) -> VGroup:
    """A stack of filled circles; draw outermost first."""
    g = VGroup()
    for i in range(layers):
        frac = (i + 1) / layers
        c = Circle(radius=radius * frac, stroke_width=0,
                   fill_color=color, fill_opacity=max_opacity * (1 - frac) ** 1.4)
        c.move_to(center)
        g.add(c)
    return g


def _project(p, yaw: float, pitch: float):
    x, y, z = p
    cy, sy = math.cos(yaw), math.sin(yaw)
    cp, sp = math.cos(pitch), math.sin(pitch)
    x1 = x * cy - y * sy
    y1 = x * sy + y * cy
    y2 = y1 * cp - z * sp
    z2 = y1 * sp + z * cp
    return np.array([x1, y2, z2])


def lattice_3d(nx: int = 7, ny: int = 4, nz: int = 3, a: float = 0.55,
               center=(0, 0, 0), yaw: float = -0.55, pitch: float = 0.42,
               color: str = GRID, radius: float = 0.032,
               bonds: bool = True) -> VGroup:
    """An isometric lattice, depth-sorted, for background atmosphere."""
    c = np.array(center, dtype=float)
    raw = []
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                p = np.array([(i - (nx - 1) / 2) * a,
                              (j - (ny - 1) / 2) * a,
                              (k - (nz - 1) / 2) * a]) + c
                raw.append((p, _project(p, yaw, pitch)))
    raw.sort(key=lambda item: item[1][2])

    group = VGroup()
    if bonds:
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    p = np.array([(i - (nx - 1) / 2) * a,
                                  (j - (ny - 1) / 2) * a,
                                  (k - (nz - 1) / 2) * a]) + c
                    for di, dj in ((1, 0), (0, 1)):
                        ii, jj = i + di, j + dj
                        if ii < nx and jj < ny:
                            q = np.array([(ii - (nx - 1) / 2) * a,
                                          (jj - (ny - 1) / 2) * a,
                                          (k - (nz - 1) / 2) * a]) + c
                            a2 = _project(p, yaw, pitch)
                            b2 = _project(q, yaw, pitch)
                            group.add(Line([a2[0], a2[1], 0], [b2[0], b2[1], 0], color=color,
                                           stroke_width=1.1).set_opacity(0.22))
    for _, q in raw:
        depth = (q[2] + 2.5) / 5.0
        dot = Dot([q[0], q[1], 0], radius=radius * (0.75 + 0.5 * depth), color=color)
        dot.set_opacity(0.25 + 0.35 * depth)
        group.add(dot)
    return group


def column_3d(n: int = 5, spacing: float = 0.42, center=(0, 0, 0),
              radius: float = 0.085, color: str = INK):
    """Return (build_fn, tracker). The build_fn is used with always_redraw."""
    from manim import ValueTracker
    tracker = ValueTracker(0.0)  # 0 = top view, 1 = side view

    def build():
        t = tracker.get_value()
        pitch = t * (math.pi / 2)
        c = np.array(center, dtype=float)
        pts = []
        for k in range(n):
            p = np.array([0, 0, (k - (n - 1) / 2) * spacing]) + c
            pts.append(_project(p, 0.0, pitch))
        pts.sort(key=lambda q: q[2])
        g = VGroup()
        for q in pts:
            depth = (q[2] + 1.0) / 2.0
            d = Dot([q[0], q[1], 0], radius=radius * (0.8 + 0.4 * depth), color=color)
            d.set_opacity(0.45 + 0.5 * depth)
            g.add(d)
        # A thin spine makes the column legible at both views.
        g.add(Line([pts[0][0], pts[0][1], 0], [pts[-1][0], pts[-1][1], 0],
                   color=color, stroke_width=1.4).set_opacity(0.35))
        return g

    return build, tracker


def focus_dial(center=(0, 0, 0), radius: float = 0.55,
               color: str = MUTED, pointer_color: str = MEASURE):
    ring = Circle(radius=radius, color=color, stroke_width=1.4)
    ring.move_to(center)
    ticks = VGroup()
    for i in range(24):
        ang = i * math.pi / 12
        r0 = radius * (0.86 if i % 3 else 0.78)
        p0 = np.array(center) + np.array([math.cos(ang), math.sin(ang), 0]) * r0
        p1 = np.array(center) + np.array([math.cos(ang), math.sin(ang), 0]) * radius
        ticks.add(Line(p0, p1, color=color, stroke_width=1.0).set_opacity(0.55))
    pointer = Line(center, np.array(center) + np.array([radius * 0.72, 0, 0]),
                   color=pointer_color, stroke_width=2.4)
    return VGroup(ring, ticks, pointer), pointer


def plate(text: str, font_size: int = 26, color: str = INK,
          fill: str = BG, opacity: float = 0.72):
    t = body(text, font_size=font_size, color=color)
    pad_x, pad_y = 0.18, 0.10
    rect = RoundedRectangle(
        width=t.width + 2 * pad_x, height=t.height + 2 * pad_y,
        corner_radius=0.08, stroke_width=0, fill_color=fill, fill_opacity=opacity,
    ).move_to(t.get_center())
    return VGroup(rect, t)

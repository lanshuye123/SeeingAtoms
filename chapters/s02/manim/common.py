"""Shared timeline helpers for S02.

The S01 scenes advanced a local `elapsed` counter and appended whatever time
was left at the end of the scene. That keeps scene starts aligned but lets the
picture drift inside a scene.

Here every visual action is attached to a sentence id. `cue()` waits until the
measured start of that sentence, and `play_t()` refuses to run past the next
cue. The same `timing.json` drives audio, subtitles and QC.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from manim import DOWN, LEFT, RIGHT, UP, FadeIn, MovingCameraScene, smooth
from src.render.theme import COLORS, body, credit, label, title  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
TIMING = ROOT / "chapters" / "s02" / "audio" / "timing.json"

BG = COLORS["bg"]
INK = COLORS["ink"]
MUTED = COLORS["muted"]
BEAM = COLORS["beam"]
MEASURE = COLORS["measure"]
ALERT = COLORS["alert"]
GRID = COLORS["grid"]


class TimelineScene(MovingCameraScene):
    section_id = "S00"

    def setup(self):
        super().setup()
        data = json.loads(TIMING.read_text(encoding="utf-8"))
        self.section = next(s for s in data["sections"] if s["id"] == self.section_id)
        self.sent_by_id = {s["id"]: s for s in self.section["sentences"]}
        self.t0 = float(self.section["start"])
        self.elapsed = 0.0
        self.camera.background_color = BG
        # Start a little wider than the default frame; the scene pushes in.
        self.camera.frame.set(width=16.0, height=9.0)

    def rel(self, sentence_id: str) -> float:
        return float(self.sent_by_id[sentence_id]["start"]) - self.t0

    def cue(self, sentence_id: str, pad: float = 0.0) -> None:
        target = self.rel(sentence_id) + pad
        if target > self.elapsed + 1e-3:
            self.wait(target - self.elapsed)
            self.elapsed = target

    def play_t(self, *anims, run_time: float = 1.0, **kwargs):
        self.play(*anims, run_time=run_time, **kwargs)
        self.elapsed += run_time

    def camera_to(self, width: float | None = None, center=None,
                  run_time: float = 1.6, rate_func=smooth):
        """Move/zoom the camera frame and keep the scene clock honest."""
        anim = self.camera.frame.animate
        if width is not None:
            anim = anim.set(width=width, height=width * 9 / 16)
        if center is not None:
            anim = anim.move_to(center)
        self.play_t(anim, run_time=run_time, rate_func=rate_func)

    def wait_t(self, seconds: float):
        if seconds > 0:
            self.wait(seconds)
            self.elapsed += seconds

    def finish(self):
        target = float(self.section["duration"])
        if target > self.elapsed + 1e-3:
            self.wait(target - self.elapsed)
            self.elapsed = target


def pin_to_frame(mob, frame, corner, buff: float = 0.35):
    """Keep a label pinned to a camera-frame corner while the camera moves."""
    def update(m):
        p = frame.get_corner(corner)
        dx = buff if corner[0] < 0 else -buff
        dy = -buff if corner[1] > 0 else buff
        m.move_to(p + np.array([dx, dy, 0]))
    mob.add_updater(update)
    update(mob)
    return mob


def kicker(scene: Scene, text: str = "看见原子 · 第二期"):
    t = label(text, color=BEAM, font_size=22)
    t.to_corner(UP + LEFT, buff=0.55)
    scene.add(t)
    return t


def foot(scene: Scene, text: str, color: str = MUTED):
    t = credit(text, color=color, font_size=18)
    t.to_corner(DOWN + LEFT, buff=0.35)
    scene.add(t)
    return t

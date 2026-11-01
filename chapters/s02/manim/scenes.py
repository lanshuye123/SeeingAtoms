"""S02 scenes S00-S07, 1920x1080 / 30 fps.

Each scene is a TimelineScene: every visual beat is attached to a sentence id
from chapters/s02/audio/timing.json, so the picture waits for the voice rather
than the other way round. S00 is the already-approved camera-led opening.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, Arc, Arrow, Circle, Create, Dot, Ellipse, FadeIn,
    FadeOut, Flash, Group, GrowArrow, GrowFromCenter, ImageMobject, Indicate, LaggedStart, Line,
    MathTex, ORIGIN, Polygon, Rectangle, ReplacementTransform, Rotate,
    RoundedRectangle, Transform, VGroup, Write, always_redraw, smooth, ParametricFunction,
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
from src.render.tex import S01_TEX_TEMPLATE  # noqa: E402
from src.render.theme import body, label, title  # noqa: E402
from sync_demo import S02SyncDemo  # noqa: E402

ASSETS = ROOT / "chapters" / "s02" / "assets"
SHOW_SCENE_SUBS = False  # burned SRT carries the narration; scene sub text would duplicate


def txt(text: str, size: int = 26, color: str = INK) -> VGroup:
    return body(text, font_size=size, color=color)


def tag(text: str, size: int = 22, color: str = INK, opacity: float = 0.82) -> VGroup:
    return plate(text, font_size=size, color=color, opacity=opacity)


def slab(width: float = 4.6, height: float = 1.5, rows: int = 4, cols: int = 9,
         color: str = MEASURE) -> VGroup:
    rect = RoundedRectangle(width=width, height=height, corner_radius=0.06,
                            stroke_color=color, stroke_width=1.6,
                            fill_color="#101A28", fill_opacity=1)
    atoms = VGroup()
    for i in range(rows):
        for j in range(cols):
            atoms.add(Dot([(j - (cols - 1) / 2) * width / cols,
                           (i - (rows - 1) / 2) * height / rows, 0],
                          radius=0.045, color=INK).set_opacity(0.55))
    return VGroup(rect, atoms)


def ray(start, end, color: str = BEAM, width: float = 2.4, opacity: float = 0.9):
    return Line(start, end, color=color, stroke_width=width).set_opacity(opacity)


def lens(center=ORIGIN, radius: float = 1.1, color: str = BEAM) -> VGroup:
    c = np.array(center, dtype=float)
    top = Ellipse(width=radius * 0.55, height=radius * 2.05, color=color,
                  stroke_width=2).move_to(c + UP * radius * 0.95)
    bot = Ellipse(width=radius * 0.55, height=radius * 2.05, color=color,
                  stroke_width=2).move_to(c + DOWN * radius * 0.95)
    coils = VGroup()
    for k in range(4):
        y = (k - 1.5) * radius * 0.42
        coils.add(Ellipse(width=radius * 0.85, height=radius * 0.20,
                          color=MUTED, stroke_width=1.2).move_to(c + UP * y))
    return VGroup(top, bot, coils)


def card(title_text: str, lines: list[str], color: str = BEAM,
         width: float = 4.4, height: float = 2.2) -> VGroup:
    box = RoundedRectangle(width=width, height=height, corner_radius=0.12,
                           stroke_color=color, stroke_width=1.6,
                           fill_color="#101A28", fill_opacity=0.96)
    head = txt(title_text, size=28, color=color)
    body_lines = VGroup(*[txt(t, size=20, color=INK) for t in lines]).arrange(DOWN, buff=0.10)
    content = VGroup(head, body_lines).arrange(DOWN, buff=0.18).move_to(box)
    return VGroup(box, content)


# --------------------------------------------------------------------------- S00
class S00(S02SyncDemo):
    """The approved S00 opening; no debug labels."""
    section_id = "S00"


# --------------------------------------------------------------------------- S01
class S01(TimelineScene):
    section_id = "S01"

    def construct(self):
        self.camera.frame.set(width=13.5, height=7.59)

        # 01
        self.cue("S01_01")
        sample = slab(6.2, 1.7, rows=4, cols=11).move_to(DOWN * 0.2)
        q = txt("电子在样品里经历了什么？", 34).move_to(UP * 2.7)
        self.play_t(FadeIn(sample), FadeIn(q), run_time=1.2)

        # 02
        self.cue("S01_02")
        atom = VGroup(Circle(radius=0.55, color=MEASURE, stroke_width=1.5).set_opacity(0.5),
                      Dot(ORIGIN, radius=0.12, color=MEASURE),
                      Circle(radius=0.95, color=BEAM, stroke_width=1).set_opacity(0.25))
        atom.move_to(LEFT * 1.8 + UP * 0.2)
        e_path = ray(LEFT * 5.8 + UP * 0.5, LEFT * 3.0 + UP * 0.2)
        e_path2 = ray(LEFT * 3.0 + UP * 0.2, LEFT * 1.1 + DOWN * 0.4)
        e_dot = Dot(LEFT * 5.8 + UP * 0.5, radius=0.08, color=BEAM)
        pull = Arrow(LEFT * 2.4 + UP * 0.5, LEFT * 1.9 + UP * 0.3,
                     buff=0.02, color=MEASURE, stroke_width=2)
        push = Arrow(LEFT * 2.4 + DOWN * 0.2, LEFT * 1.9 + DOWN * 0.05,
                     buff=0.02, color=BEAM, stroke_width=2)
        nuc_lab = tag("原子核", 18, MEASURE).move_to(LEFT * 1.8 + DOWN * 1.2)
        cloud_lab = tag("电子云", 18, BEAM).move_to(LEFT * 1.8 + UP * 1.5)
        self.play_t(FadeOut(sample), FadeOut(q), run_time=0.5)
        self.play_t(FadeIn(atom), FadeIn(e_path), FadeIn(e_path2), FadeIn(e_dot),
                    FadeIn(nuc_lab), FadeIn(cloud_lab), run_time=1.0)
        self.camera_to(width=9.0, center=LEFT * 1.6 + UP * 0.2, run_time=1.4)
        self.play_t(GrowArrow(pull), GrowArrow(push), run_time=0.9)
        self.play_t(e_dot.animate.move_to(LEFT * 1.1 + DOWN * 0.4), run_time=1.6)

        # 03
        self.cue("S01_03")
        left = card("电子衍射", ["1–2 秒", "信号强"], BEAM, 4.0, 2.0).move_to(LEFT * 3.6 + UP * 0.1)
        right = card("X 射线", ["数十分钟", "信号弱"], MEASURE, 4.0, 2.0).move_to(RIGHT * 3.6 + UP * 0.1)
        self.play_t(FadeOut(atom), FadeOut(e_path), FadeOut(e_path2), FadeOut(e_dot),
                    FadeOut(pull), FadeOut(push), FadeOut(nuc_lab), FadeOut(cloud_lab),
                    run_time=0.5)
        self.camera_to(width=12.0, center=ORIGIN, run_time=1.2)
        self.play_t(FadeIn(left), FadeIn(right), run_time=1.0)

        # 04
        self.cue("S01_04")
        thick = slab(5.0, 2.4, rows=6, cols=9).move_to(LEFT * 2.6)
        blocked = ray(LEFT * 6.2 + UP * 0.3, LEFT * 4.0 + UP * 0.3)
        stop = Dot(LEFT * 4.0 + UP * 0.3, radius=0.10, color=MEASURE)
        warn = txt("电子穿不透", 32, MEASURE).move_to(RIGHT * 3.8 + UP * 1.2)
        self.play_t(FadeOut(left), FadeOut(right), run_time=0.5)
        self.play_t(FadeIn(thick), FadeIn(blocked), FadeIn(stop), FadeIn(warn), run_time=1.0)

        # 05
        self.cue("S01_05")
        paths = VGroup()
        rng = np.random.default_rng(3)
        for i in range(5):
            x0 = -5.2
            y0 = -0.7 + i * 0.35
            pts = [np.array([x0, y0, 0])]
            for k in range(4):
                pts.append(pts[-1] + np.array([1.0, rng.uniform(-0.35, 0.35), 0]))
            paths.add(VGroup(*[Line(pts[k], pts[k + 1], color=BEAM, stroke_width=1.4)
                              .set_opacity(0.7) for k in range(len(pts) - 1)]))
        dark = Rectangle(width=3.4, height=1.1, stroke_width=0, fill_color="#000000",
                         fill_opacity=0.55).move_to(LEFT * 2.6 + UP * 1.1)
        thick_label = tag("厚区：电子出不来", 22, INK).move_to(RIGHT * 3.2 + DOWN * 0.6)
        self.play_t(FadeOut(blocked), FadeOut(stop), FadeOut(warn), run_time=0.4)
        self.play_t(FadeIn(paths), FadeIn(dark), FadeIn(thick_label), run_time=1.2)

        # 06
        self.cue("S01_06")
        axis = Line(LEFT * 5.8 + DOWN * 0.2, RIGHT * 5.8 + DOWN * 0.2, color=MUTED, stroke_width=2)
        mark1 = Line(LEFT * 1.2 + DOWN * 0.5, LEFT * 1.2 + UP * 0.1, color=BEAM, stroke_width=3)
        mark2 = Line(RIGHT * 3.4 + DOWN * 0.5, RIGHT * 3.4 + UP * 0.1, color=MEASURE, stroke_width=3)
        lab1 = tag("衍射：50–100 nm", 22, BEAM).move_to(LEFT * 1.2 + UP * 0.8)
        lab2 = tag("高分辨：<10 nm", 22, MEASURE).move_to(RIGHT * 3.4 + UP * 0.8)
        self.play_t(FadeOut(thick), FadeOut(paths), FadeOut(dark), FadeOut(thick_label),
                    run_time=0.4)
        self.play_t(Create(axis), Create(mark1), Create(mark2), FadeIn(lab1), FadeIn(lab2),
                    run_time=1.2)

        # 07-11: a five-step sample-prep strip
        self.cue("S01_07")
        strip_title = txt("块状材料 → 几十纳米", 28).move_to(UP * 2.6)
        block = slab(1.2, 1.2, rows=4, cols=4, color=MEASURE).move_to(LEFT * 5.4 + DOWN * 0.4)
        arrow = Arrow(LEFT * 4.6 + DOWN * 0.4, LEFT * 4.0 + DOWN * 0.4,
                      color=MEASURE, stroke_width=2)
        self.play_t(FadeOut(axis), FadeOut(mark1), FadeOut(mark2), FadeOut(lab1), FadeOut(lab2),
                    run_time=0.4)
        self.play_t(FadeIn(strip_title), FadeIn(block), GrowArrow(arrow), run_time=0.9)

        step_lab = VGroup()
        step_icons = VGroup()
        xs = [-2.6, -0.6, 1.4, 3.4, 5.2]
        labels = ["1 mm 切片", "磨到 1 µm", "3 mm 铜环", "凹坑", "离子减薄"]

        def mini_disc(x, y=-0.4, r=0.55):
            g = VGroup(Circle(radius=r, color=MEASURE, stroke_width=2,
                              fill_color="#101A28", fill_opacity=1).move_to([x, y, 0]))
            return g

        self.cue("S01_08")
        s1 = mini_disc(xs[0])
        l1 = tag(labels[0], 18, MEASURE).move_to([xs[0], -1.4, 0])
        self.play_t(FadeIn(s1), FadeIn(l1), run_time=0.8)

        self.cue("S01_09")
        s2 = VGroup(mini_disc(xs[1]), Arrow([xs[1] - 0.9, -0.4, 0], [xs[1] - 0.2, -0.4, 0],
                                          color=BEAM, stroke_width=2))
        l2 = tag(labels[1], 18, BEAM).move_to([xs[1], -1.4, 0])
        self.play_t(FadeIn(s2), FadeIn(l2), run_time=0.8)

        self.cue("S01_10")
        s3 = VGroup(Circle(radius=0.55, color=MEASURE, stroke_width=2).move_to([xs[2], -0.4, 0]),
                    Circle(radius=0.18, color=GRID, stroke_width=1.5).move_to([xs[2], -0.4, 0]))
        l3 = tag(labels[2], 18, MEASURE).move_to([xs[2], -1.4, 0])
        self.play_t(FadeIn(s3), FadeIn(l3), run_time=0.8)

        self.cue("S01_11")
        s4 = VGroup(Circle(radius=0.55, color=MEASURE, stroke_width=2).move_to([xs[3], -0.4, 0]),
                    Circle(radius=0.30, color=GRID, stroke_width=1.5).move_to([xs[3], -0.4, 0]))
        l4 = tag(labels[3], 18, MUTED).move_to([xs[3], -1.4, 0])
        s5 = VGroup(Circle(radius=0.55, color=MEASURE, stroke_width=2).move_to([xs[4], -0.4, 0]),
                    Circle(radius=0.12, color=BG, fill_color=BG, fill_opacity=1).move_to([xs[4], -0.4, 0]),
                    Arrow([xs[4] - 0.8, 1.0, 0], [xs[4] - 0.2, -0.1, 0],
                          color=BEAM, stroke_width=2),
                    Arrow([xs[4] + 0.8, -1.6, 0], [xs[4] + 0.2, -0.7, 0],
                          color=BEAM, stroke_width=2))
        l5 = tag(labels[4], 18, BEAM).move_to([xs[4], -1.4, 0])
        self.play_t(FadeIn(s4), FadeIn(l4), FadeIn(s5), FadeIn(l5), run_time=1.0)

        # 12
        self.cue("S01_12")
        glow = radial_glow([xs[4], -0.4, 0], 0.75, BEAM, layers=22, max_opacity=0.35)
        thin_lab = tag("孔边的薄区，才是要看的", 22, BEAM).move_to(DOWN * 2.4)
        self.play_t(FadeIn(glow), FadeIn(thin_lab), run_time=0.9)

        # 13
        self.cue("S01_13")
        # The burned SRT already carries this line; keep the strip clean.
        self.play_t(FadeOut(thin_lab), run_time=0.5)
        self.finish()


# --------------------------------------------------------------------------- S02
class S02(TimelineScene):
    section_id = "S02"

    def construct(self):
        self.camera.frame.set(width=13.5, height=7.59)
        self.head = None
        self.sub = None

        def head(text, color=INK, size=40):
            new = title(text, font_size=size, color=color).move_to(UP * 2.9)
            if self.head is None:
                self.play_t(FadeIn(new), run_time=0.6)
            else:
                self.play_t(FadeOut(self.head), FadeIn(new), run_time=0.5)
            self.head = new

        def sub(text, color=INK, size=24):
            if not SHOW_SCENE_SUBS:
                return
            new = txt(text, size=size, color=color).move_to(DOWN * 2.9)
            if self.sub is None:
                self.play_t(FadeIn(new), run_time=0.5)
            else:
                self.play_t(FadeOut(self.sub), FadeIn(new), run_time=0.4)
            self.sub = new

        # 01
        self.cue("S02_01")
        head("能看多细？")
        ruler = Line(LEFT * 6.0 + DOWN * 0.2, RIGHT * 6.0 + DOWN * 0.2, color=MUTED, stroke_width=2)
        self.play_t(Create(ruler), run_time=0.8)

        # 02
        self.cue("S02_02")
        e_mark = Dot(LEFT * 2.0 + DOWN * 0.2, radius=0.10, color=BEAM)
        e_lab = tag("电子 0.025 Å", 24, BEAM).move_to(LEFT * 2.0 + UP * 0.5)
        self.play_t(FadeIn(e_mark), FadeIn(e_lab), run_time=0.8)
        sub("二百千伏的电子波长")

        # 03
        self.cue("S02_03")
        x_mark = Dot(RIGHT * 2.8 + DOWN * 0.2, radius=0.10, color=MEASURE)
        x_lab = tag("X 射线 1.54 Å", 24, MEASURE).move_to(RIGHT * 2.8 + UP * 0.5)
        ratio = tag("≈ 60 倍", 26, MEASURE).move_to(UP * 1.4)
        self.play_t(FadeIn(x_mark), FadeIn(x_lab), FadeIn(ratio), run_time=0.9)
        sub("实验室最常见的铜靶 X 射线")

        # 04
        self.cue("S02_04")
        self.play_t(FadeOut(ratio), run_time=0.3)
        ideal = txt("理论极限 0.05 Å", 30, BEAM).move_to(UP * 1.4)
        self.play_t(FadeIn(ideal), run_time=0.8)
        sub("只按波长算，看原子绰绰有余")

        # 05
        self.cue("S02_05")
        self.play_t(FadeOut(ideal), run_time=0.3)
        actual = txt("实际 1.9 Å", 30, MEASURE).move_to(UP * 1.4)
        gap_arrow = Arrow(LEFT * 0.8 + DOWN * 0.7, RIGHT * 0.8 + DOWN * 0.7,
                          color=MEASURE, stroke_width=2.5)
        self.play_t(FadeIn(actual), GrowArrow(gap_arrow), run_time=0.8)
        sub("差了一个多数量级")

        # 06
        self.cue("S02_06")
        self.play_t(FadeOut(actual), FadeOut(gap_arrow), FadeOut(e_mark), FadeOut(e_lab),
                    FadeOut(x_mark), FadeOut(x_lab), FadeOut(ruler), run_time=0.5)
        head("差在透镜上", MEASURE)
        lens_g = lens(ORIGIN + DOWN * 0.1, 1.0)
        self.play_t(FadeIn(lens_g), run_time=0.8)
        sub("电子带电，能用磁场掰弯")

        # 07
        self.cue("S02_07")
        tvals = np.linspace(0, 6 * math.pi, 260)
        pts = [np.array([-2.9 + 5.8 * t / (6 * math.pi),
                         0.1 + 0.55 * math.sin(t), 0]) for t in tvals]
        path = VGroup(*[Line(pts[i], pts[i + 1], color=BEAM, stroke_width=1.6)
                        .set_opacity(0.75) for i in range(len(pts) - 1)])
        self.play_t(FadeIn(path), run_time=1.2)
        sub("磁透镜：电子走螺旋线")

        # 08
        self.cue("S02_08")
        sub("电流大 → 焦距短；电流小 → 焦距长")

        # 09
        self.cue("S02_09")
        zoom = card("磁透镜", ["焦距连续可调", "放大倍数连续变"], BEAM, 4.2, 2.0)
        zoom.move_to(LEFT * 3.4 + DOWN * 1.0)
        glass = card("玻璃透镜", ["只能换镜头", "焦距固定"], MEASURE, 4.2, 2.0)
        glass.move_to(RIGHT * 3.4 + DOWN * 1.0)
        self.play_t(FadeIn(zoom), FadeIn(glass), run_time=0.9)
        sub("放大倍数：连续变 vs 换镜头")

        # 10
        self.cue("S02_10")
        self.play_t(FadeOut(zoom), FadeOut(glass), run_time=0.4)
        head("磁透镜不能像玻璃那样消像差", MEASURE, 34)
        sub("凹透镜+凸透镜的组合，在这里用不上")

        # 11
        self.cue("S02_11")
        self.play_t(FadeOut(lens_g), FadeOut(path), run_time=0.4)
        head("一个点 → 一个斑", MEASURE)
        rays = VGroup()
        for y in [-1.2, -0.6, 0.0, 0.6, 1.2]:
            rays.add(Line(LEFT * 4.6 + UP * y, LEFT * 0.6 + UP * y,
                          color=BEAM, stroke_width=1.8).set_opacity(0.75))
            rays.add(Line(LEFT * 0.6 + UP * y, RIGHT * 1.6 + UP * (0.0 if y == 0 else 0.35 * np.sign(y)),
                          color=BEAM, stroke_width=1.8).set_opacity(0.75))
        blur = Ellipse(width=0.9, height=0.35, color=MEASURE, fill_color=MEASURE,
                       fill_opacity=0.35, stroke_width=1.5).move_to(RIGHT * 2.4 + UP * 0.3)
        self.play_t(FadeIn(rays), FadeIn(blur), run_time=1.0)
        sub("离轴越远，偏得越狠")

        # 12
        self.cue("S02_12")
        head("球差", MEASURE, 48)
        formula = MathTex(r"r_s = C_s\beta^3", tex_template=S01_TEX_TEMPLATE,
                          font_size=44, color=INK).move_to(RIGHT * 3.6 + DOWN * 1.2)
        self.play_t(FadeIn(formula), run_time=0.8)
        sub("限制分辨率的大头")

        # 13
        self.cue("S02_13")
        corrector = VGroup(*[Ellipse(width=0.26, height=1.6, color=MEASURE,
                                     stroke_width=1.5).move_to(LEFT * 0.6 + RIGHT * i * 0.32)
                             for i in range(3)])
        self.play_t(FadeIn(corrector), run_time=0.8)
        head("球差校正器", MEASURE, 36)
        sub("多极磁透镜，把这份误差抵掉")

        # 14
        self.cue("S02_14")
        head("校正后 ~1 Å", BEAM, 40)
        sub("好一点的，~0.5 Å")

        # 15
        self.cue("S02_15")
        self.play_t(FadeOut(rays), FadeOut(blur), FadeOut(formula), FadeOut(corrector),
                    run_time=0.6)
        head("两件事", INK, 40)
        left_card = card("第一期", ["卡在波长"], MUTED, 4.0, 1.8).move_to(LEFT * 3.4 + DOWN * 0.7)
        right_card = card("第二期", ["卡在透镜"], BEAM, 4.0, 1.8).move_to(RIGHT * 3.4 + DOWN * 0.7)
        self.play_t(FadeIn(left_card), FadeIn(right_card), run_time=0.9)
        self.finish()


# --------------------------------------------------------------------------- S03
class S03(TimelineScene):
    section_id = "S03"

    def construct(self):
        self.camera.frame.set(width=13.5, height=7.59)
        self.head = None
        self.sub = None

        def head(text, color=INK, size=40):
            new = title(text, font_size=size, color=color).move_to(UP * 2.9)
            if self.head is None:
                self.play_t(FadeIn(new), run_time=0.6)
            else:
                self.play_t(FadeOut(self.head), FadeIn(new), run_time=0.5)
            self.head = new

        def sub(text, color=INK, size=24):
            if not SHOW_SCENE_SUBS:
                return
            new = txt(text, size=size, color=color).move_to(DOWN * 2.9)
            if self.sub is None:
                self.play_t(FadeIn(new), run_time=0.5)
            else:
                self.play_t(FadeOut(self.sub), FadeIn(new), run_time=0.4)
            self.sub = new

        # 01
        self.cue("S03_01")
        head("能看多细 / 看到什么")
        a = card("能看多细", ["分辨率"], MUTED, 4.0, 1.8).move_to(LEFT * 3.4 + DOWN * 0.4)
        b = card("看到什么", ["像 / 衍射"], BEAM, 4.0, 1.8).move_to(RIGHT * 3.4 + DOWN * 0.4)
        self.play_t(FadeIn(a), FadeIn(b), run_time=0.9)
        sub("分辨率是一回事，信息类型是另一回事")

        # 02
        self.cue("S03_02")
        self.play_t(FadeOut(a), FadeOut(b), run_time=0.4)
        head("两拨电子")
        samp = slab(4.2, 1.4, rows=3, cols=7).move_to(ORIGIN)
        tbeam = ray(LEFT * 6.2 + UP * 0.5, LEFT * 2.1 + UP * 0.5)
        dbeam = ray(LEFT * 6.2 + DOWN * 0.3, LEFT * 2.1 + DOWN * 0.3)
        tbeam2 = ray(RIGHT * 2.1 + UP * 0.5, RIGHT * 5.6 + UP * 0.5)
        dbeam2 = ray(RIGHT * 2.1 + DOWN * 0.3, RIGHT * 5.6 + DOWN * 1.0)
        self.play_t(FadeIn(samp), Create(tbeam), Create(dbeam), run_time=0.9)
        self.play_t(Create(tbeam2), Create(dbeam2), run_time=0.9)
        sub("一拨没怎么偏，一拨被晶面拐了个小角度")

        # 03
        self.cue("S03_03")
        lens_g = lens(RIGHT * 4.2 + UP * 0.1, 0.85)
        bfp = Line(RIGHT * 5.6 + DOWN * 1.9, RIGHT * 5.6 + UP * 1.9, color=MUTED, stroke_width=1.4)
        spots = VGroup(Dot(RIGHT * 5.6 + UP * 1.0, radius=0.09, color=BEAM),
                       Dot(RIGHT * 5.6 + DOWN * 0.9, radius=0.09, color=MEASURE))
        bfp_lab = tag("后焦面", 18, MUTED).next_to(bfp, UP, buff=0.05)
        self.play_t(FadeIn(lens_g), Create(bfp), FadeIn(spots), FadeIn(bfp_lab), run_time=1.0)
        sub("物镜把两拨电子收到后焦面，各成一个斑点")

        # 04
        self.cue("S03_04")
        head("后焦面 = 衍射图")
        sub("斑点就是衍射图，不是样品的像")

        # 05
        self.cue("S03_05")
        mid = RoundedRectangle(width=1.1, height=1.7, corner_radius=0.08,
                               stroke_color=BEAM, fill_color="#101A28",
                               fill_opacity=1).move_to(LEFT * 1.4 + DOWN * 2.2)
        mid_lab = tag("中间镜", 18, BEAM).next_to(mid, DOWN, buff=0.08)
        mode = txt("像平面 ↔ 后焦面", 22, INK).move_to(LEFT * 3.2 + DOWN * 1.2)
        self.play_t(FadeIn(mid), FadeIn(mid_lab), FadeIn(mode), run_time=0.8)
        head("一台机器，两种看法")
        sub("中间镜的物平面对在哪里，就看到什么")

        # 06
        self.cue("S03_06")
        knob = Circle(radius=0.40, color=MEASURE, stroke_width=2).move_to(LEFT * 3.2 + DOWN * 2.4)
        ptr = Line(knob.get_center(), knob.get_center() + UP * 0.3, color=MEASURE, stroke_width=2)
        self.play_t(FadeIn(knob), FadeIn(ptr), Rotate(ptr, angle=1.0, about_point=knob.get_center()),
                    run_time=0.9)
        sub("扭一下旋钮：像 ↔ 衍射斑点")

        # 07
        self.cue("S03_07")
        ap = VGroup(Rectangle(width=1.5, height=1.0, color=MEASURE, stroke_width=1.5),
                    Circle(radius=0.22, color=BEAM, fill_color=BEAM, fill_opacity=0.25))
        ap.move_to(samp.get_center())
        ap_lab = tag("选区光阑", 18, MEASURE).next_to(ap, UP, buff=0.08)
        self.play_t(FadeIn(ap), FadeIn(ap_lab), run_time=0.8)
        head("只让一小块信号过去")
        sub("在中间镜的物平面上插一个金属小孔")

        # 08
        self.cue("S03_08")
        head("选区电子衍射", BEAM, 44)
        sub("SAED：这一小块区域的衍射")

        # 09
        self.cue("S03_09")
        self.play_t(FadeOut(ap), FadeOut(ap_lab), FadeOut(mid), FadeOut(mid_lab), FadeOut(mode),
                    FadeOut(knob), FadeOut(ptr), FadeOut(lens_g), FadeOut(bfp),
                    FadeOut(spots), FadeOut(bfp_lab), run_time=0.5)
        head("衍射角：电子 ~1°，X 射线几十度")
        origin = LEFT * 4.0 + DOWN * 1.8
        base = Line(origin, origin + RIGHT * 6.0, color=MUTED, stroke_width=2)
        e_line = Line(origin, origin + RIGHT * 6.0 + UP * 0.35, color=BEAM, stroke_width=2)
        arc = Arc(radius=1.4, start_angle=0, angle=0.06, arc_center=origin, color=BEAM, stroke_width=2)
        x_arc = Arc(radius=2.2, start_angle=0, angle=0.9, arc_center=origin, color=MEASURE, stroke_width=2)
        e_lab = tag("电子 ~1°", 18, BEAM).move_to(RIGHT * 1.0 + DOWN * 1.0)
        x_lab = tag("X 射线 几十度", 18, MEASURE).move_to(RIGHT * 3.0 + DOWN * 0.5)
        self.play_t(Create(base), Create(e_line), Create(arc), Create(x_arc),
                    FadeIn(e_lab), FadeIn(x_lab), run_time=1.0)
        sub("波长越短，满足布拉格条件的角度越小")

        # 10
        self.cue("S03_10")
        self.play_t(FadeOut(base), FadeOut(e_line), FadeOut(arc), FadeOut(x_arc),
                    FadeOut(e_lab), FadeOut(x_lab), FadeOut(samp), FadeOut(tbeam),
                    FadeOut(dbeam), FadeOut(tbeam2), FadeOut(dbeam2), run_time=0.5)
        head("二维截面 / 一维投影")
        lat = VGroup(*[Dot([-4.4 + i * 0.34, -0.2 + j * 0.34, 0], radius=0.03,
                           color=BEAM).set_opacity(0.7) for i in range(5) for j in range(4)])
        plane = Polygon([-4.8, -0.5, 0], [-2.8, -0.5, 0], [-2.8, 0.9, 0], [-4.8, 0.9, 0],
                        color=BEAM, stroke_width=1.2, fill_color=BEAM, fill_opacity=0.06)
        p2 = tag("电子：二维截面", 18, BEAM).move_to(LEFT * 3.8 + DOWN * 1.3)
        p1 = tag("X 射线：一维投影", 18, MEASURE).move_to(RIGHT * 3.6 + DOWN * 1.3)
        proj = VGroup(*[Dot([2.0 + i * 0.25, -0.2, 0], radius=0.05, color=MEASURE)
                        for i in range(6)])
        self.play_t(FadeIn(lat), FadeIn(plane), FadeIn(p2), FadeIn(proj), FadeIn(p1), run_time=1.0)
        sub("电子衍射是倒易点阵的二维截面")

        # 11
        self.cue("S03_11")
        rod = Line(RIGHT * 4.4 + DOWN * 1.2, RIGHT * 4.4 + UP * 2.2, color=MEASURE, stroke_width=3)
        rod_lab = tag("薄样品 → 倒易杆", 18, MEASURE).move_to(RIGHT * 2.6 + UP * 1.4)
        self.play_t(Create(rod), FadeIn(rod_lab), run_time=0.8)
        head("薄样品把倒易点拉成杆")
        sub("杆长了，角度稍微偏一点，也能衍射")

        # 12
        self.cue("S03_12")
        self.play_t(FadeOut(lat), FadeOut(plane), FadeOut(p2), FadeOut(proj),
                    FadeOut(p1), FadeOut(rod), FadeOut(rod_lab), run_time=0.5)
        head("更宽容，也更受厚度影响", BEAM, 36)
        sub("电子衍射的花样，和 X 射线不是一回事")
        self.finish()


# --------------------------------------------------------------------------- S04
class S04(TimelineScene):
    section_id = "S04"

    def construct(self):
        self.camera.frame.set(width=13.5, height=7.59)
        self.head = None
        self.sub = None
        self.stage_group = None
        sim = ASSETS / "sim" / "sim_srtio3_001_sr_under.png"
        sim_over = ASSETS / "sim" / "sim_srtio3_001_sr_over.png"

        def head(text, color=INK, size=40):
            new = title(text, font_size=size, color=color).move_to(UP * 2.9)
            if self.head is None:
                self.play_t(FadeIn(new), run_time=0.5)
            else:
                self.play_t(FadeOut(self.head), FadeIn(new), run_time=0.45)
            self.head = new

        def sub(text, color=INK, size=24):
            if not SHOW_SCENE_SUBS:
                return
            new = txt(text, size=size, color=color).move_to(DOWN * 2.9)
            if self.sub is None:
                self.play_t(FadeIn(new), run_time=0.4)
            else:
                self.play_t(FadeOut(self.sub), FadeIn(new), run_time=0.35)
            self.sub = new

        def stage(*mobs, keep=False):
            new = Group(*mobs)
            if self.stage_group is not None:
                self.play_t(FadeOut(self.stage_group), FadeIn(new),
                            run_time=0.55)
            else:
                self.play_t(FadeIn(new), run_time=0.6)
            self.stage_group = new
            return new

        # 01
        self.cue("S04_01")
        head("回到那排细线")
        img = ImageMobject(sim).set_height(4.6).move_to(RIGHT * 1.8 + DOWN * 0.1)
        stage(img)
        sub("高分辨像，不是把原子放大")

        # 02
        self.cue("S04_02")
        head("相位，不是放大")
        atoms = VGroup(*[Dot([-4.6 + i * 0.55, 0.4, 0], radius=0.07, color=INK)
                         for i in range(9)])
        wave = ParametricFunction(
            lambda t: np.array([-5.0 + 10.0 * t,
                                0.0 + 0.35 * math.sin(6 * math.pi * t + 0.8 * math.sin(4 * math.pi * t)),
                                0]),
            t_range=[0, 1], color=BEAM, stroke_width=2.2)
        stage(atoms, wave)
        sub("原子势让电子波的相位变了一点")

        # 03
        self.cue("S04_03")
        head("探测器只记亮度")
        det = RoundedRectangle(width=5.0, height=1.2, corner_radius=0.08,
                               stroke_color=MUTED, stroke_width=1.2,
                               fill_color="#101A28", fill_opacity=1).move_to(DOWN * 0.4)
        bars = VGroup(*[Rectangle(width=0.18, height=0.3 + 0.2 * (i % 3),
                                  stroke_width=0, fill_color=BEAM,
                                  fill_opacity=0.55).move_to(det.get_center() + LEFT * 1.9 + RIGHT * i * 0.46)
                        for i in range(8)])
        stage(det, bars)
        sub("相位差看不见，亮度可以")

        # 04
        self.cue("S04_04")
        head("球差 + 离焦")
        lens_g = lens(ORIGIN + DOWN * 0.2, 1.0)
        p1 = radial_glow(LEFT * 1.6 + DOWN * 0.2, 0.7, BEAM, layers=16, max_opacity=0.30)
        stage(lens_g, p1)
        sub("把相位差翻译成亮度差")

        # 05
        self.cue("S04_05")
        head("亮点 = 翻译后的相位")
        img2 = ImageMobject(sim).set_height(4.4).move_to(RIGHT * 1.8 + DOWN * 0.1)
        dots = VGroup(*[Circle(radius=0.16, color=MEASURE, stroke_width=1.5)
                        .move_to(RIGHT * 1.8 + np.array([x, y, 0]))
                        for x, y in [(-0.9, 0.8), (0.0, 0.2), (0.9, -0.5)]])
        stage(img2, dots)
        sub("不是原子的影子，是相位被翻译后的结果")

        # 06
        self.cue("S04_06")
        head("离焦反转")
        im1 = ImageMobject(sim).set_height(3.4).move_to(LEFT * 2.6 + DOWN * 0.2)
        im2 = ImageMobject(sim_over).set_height(3.4).move_to(RIGHT * 2.6 + DOWN * 0.2)
        l1 = tag("−20 nm", 18, BEAM).next_to(im1, DOWN, buff=0.08)
        l2 = tag("+20 nm", 18, MEASURE).next_to(im2, DOWN, buff=0.08)
        stage(im1, im2, l1, l2)
        sub("离焦量变一点，亮点可能变成暗点")

        # 07
        self.cue("S04_07")
        head("一个亮点 = 一列原子")
        build, tracker = column_3d(n=5, spacing=0.32, center=RIGHT * 1.8)
        col = always_redraw(build)
        stage(col)
        self.play_t(tracker.animate.set_value(0.72), run_time=1.2)
        sub("图上的一个亮点，是一整列原子的投影")

        # 08
        self.cue("S04_08")
        head("读图前，先知道参数")
        chips = VGroup(*[tag(t, 18, INK) for t in ["电压", "球差", "离焦", "厚度"]])
        chips.arrange(RIGHT, buff=0.18).move_to(DOWN * 0.2)
        stage(chips)
        sub("加速电压、球差、离焦、样品厚度")

        # 09
        self.cue("S04_09")
        head("两张模拟图对照")
        a = ImageMobject(sim).set_height(3.2).move_to(LEFT * 2.8 + DOWN * 0.2)
        b = ImageMobject(sim_over).set_height(3.2).move_to(RIGHT * 2.8 + DOWN * 0.2)
        stage(a, b)
        sub("同一结构，不同离焦 / 厚度：亮点会变")

        # 10
        self.cue("S04_10")
        head("模拟图是证据的一部分")
        ev = txt("不是装饰；它让“这几个点是哪种原子”有依据。", 24, MEASURE).move_to(DOWN * 0.2)
        stage(ev)
        sub("没有模拟，高分辨像很难定量解读")

        # 11
        self.cue("S04_11")
        head("投影：沿厚度压扁")
        layers = VGroup(*[Dot([0, (k - 1.5) * 0.35, 0], radius=0.09, color=INK)
                          for k in range(4)])
        layers.move_to(ORIGIN)
        press = Arrow(UP * 2.0, UP * 0.8, color=MEASURE, stroke_width=3)
        flat = Dot(ORIGIN, radius=0.12, color=MEASURE)
        stage(layers, press)
        self.play_t(layers.animate.arrange(DOWN, buff=0.02).move_to(ORIGIN), run_time=1.0)
        self.play_t(FadeIn(flat), run_time=0.5)
        sub("前后的原子，落在同一个位置上")

        # 12
        self.cue("S04_12")
        self.play_t(FadeOut(flat), run_time=0.25)
        head("轻的弱，重的强")
        light = Dot(LEFT * 2.0, radius=0.09, color=MUTED)
        heavy = Dot(RIGHT * 0.2, radius=0.20, color=MEASURE)
        stage(light, heavy)
        sub("散射本领不同，亮度就不同")

        # 13
        self.cue("S04_13")
        head("STEM：逐点扫描")
        scan = VGroup(*[Line([-3.0, -1.2 + i * 0.28, 0], [1.4, -1.2 + i * 0.28, 0],
                             color=GRID, stroke_width=1).set_opacity(0.5) for i in range(7)])
        probe = Dot([-3.0, -1.2, 0], radius=0.10, color=BEAM)
        stage(scan, probe)
        self.play_t(probe.animate.move_to([1.2, 0.5, 0]), run_time=1.6)
        sub("收集高角散射的电子")

        # 14
        self.cue("S04_14")
        head("HAADF：Z 衬度")
        ring = Circle(radius=0.9, color=MEASURE, stroke_width=2).move_to(RIGHT * 2.0)
        z1 = Dot(RIGHT * 2.0, radius=0.16, color=MEASURE)
        z2 = Dot(RIGHT * 2.0 + LEFT * 0.5, radius=0.08, color=MUTED)
        stage(ring, z1, z2)
        sub("原子越重，信号通常越强")

        # 15
        self.cue("S04_15")
        head("仍不是照片")
        end = txt("它更像在数原子，\n但仍是一张由散射强度画出来的图。", 26, INK).move_to(DOWN * 0.2)
        stage(end)
        sub("高分辨像 = 相位 + 投影 + 模拟")
        self.finish()


# --------------------------------------------------------------------------- S05
class S05(TimelineScene):
    section_id = "S05"

    def construct(self):
        self.camera.frame.set(width=12.5, height=7.03)
        self.head = None
        self.sub = None
        self.stage_group = None
        sim = ASSETS / "sim" / "sim_srtio3_001_sr_under.png"
        over = ASSETS / "sim" / "sim_srtio3_001_sr_over.png"
        thick = ASSETS / "sim" / "sim_srtio3_001_sr_thick.png"

        def head(text, color=INK, size=38):
            new = title(text, font_size=size, color=color).move_to(UP * 2.55)
            if self.head is None:
                self.play_t(FadeIn(new), run_time=0.5)
            else:
                self.play_t(FadeOut(self.head), FadeIn(new), run_time=0.4)
            self.head = new

        def sub(text, color=INK, size=24):
            if not SHOW_SCENE_SUBS:
                return
            new = txt(text, size=size, color=color).move_to(DOWN * 2.7)
            if self.sub is None:
                self.play_t(FadeIn(new), run_time=0.4)
            else:
                self.play_t(FadeOut(self.sub), FadeIn(new), run_time=0.35)
            self.sub = new

        def stage(*mobs):
            new = Group(*mobs)
            if self.stage_group is not None:
                self.play_t(FadeOut(self.stage_group), FadeIn(new), run_time=0.5)
            else:
                self.play_t(FadeIn(new), run_time=0.6)
            self.stage_group = new

        # 01
        self.cue("S05_01")
        head("看一张图")
        img = ImageMobject(sim).set_height(4.8).move_to(RIGHT * 1.4 + DOWN * 0.1)
        stage(img)
        sub("按钛酸锶的结构算出来的高分辨像")

        # 02
        self.cue("S05_02")
        head("模拟计算 · 非实测")
        img = ImageMobject(sim).set_height(4.8).move_to(RIGHT * 1.4 + DOWN * 0.1)
        note = tag("只画锶原子列", 18, MEASURE).move_to(LEFT * 3.8 + DOWN * 0.4)
        stage(img, note)
        sub("不是实拍；亮点对应一列列原子")

        # 03
        self.cue("S05_03")
        head("间距 3.9 Å")
        img = ImageMobject(sim).set_height(4.4).move_to(RIGHT * 1.4 + DOWN * 0.1)
        ruler = Line([0.0, -1.9, 0], [2.8, -1.9, 0], color=MEASURE, stroke_width=2)
        rlab = tag("3.9 Å", 20, MEASURE).next_to(ruler, UP, buff=0.06)
        stage(img, ruler, rlab)
        sub("亮点对应一列列原子，间距三点九埃")

        # 04
        self.cue("S05_04")
        head("真实图不会一模一样")
        a = ImageMobject(sim).set_height(3.0).move_to(LEFT * 2.6 + DOWN * 0.2)
        b = ImageMobject(over).set_height(3.0).move_to(RIGHT * 2.6 + DOWN * 0.2)
        la = tag("离焦 −20 nm", 16, BEAM).next_to(a, DOWN, buff=0.06)
        lb = tag("离焦 +20 nm", 16, MEASURE).next_to(b, DOWN, buff=0.06)
        stage(a, b, la, lb)
        sub("离焦量、厚度、球差，都会改变亮点的样子")

        # 05
        self.cue("S05_05")
        head("参数一变，亮点就变")
        chips = VGroup(*[tag(t, 18, INK) for t in ["离焦", "厚度", "球差"]])
        chips.arrange(RIGHT, buff=0.25).move_to(DOWN * 0.2)
        stage(chips)
        sub("所以模拟图要带参数，才有意义")

        # 06
        self.cue("S05_06")
        head("模拟图 = 对照的尺子")
        img = ImageMobject(sim).set_height(4.0).move_to(RIGHT * 1.4 + DOWN * 0.1)
        ruler = Line([0.2, -1.7, 0], [2.6, -1.7, 0], color=MEASURE, stroke_width=2)
        stage(img, ruler)
        sub("实拍的图，要跟它对上，才敢往下读")

        # 07
        self.cue("S05_07")
        head("真实样品不会这么整齐")
        grid_a = VGroup(*[Dot([-3.6 + i * 0.42, -0.6 + j * 0.42, 0], radius=0.05,
                              color=INK).set_opacity(0.55) for i in range(6) for j in range(5)])
        grid_b = VGroup(*[Dot([-1.0 + i * 0.42, -0.6 + j * 0.42, 0], radius=0.05,
                              color=INK).set_opacity(0.55) for i in range(6) for j in range(5)])
        shift_line = Line([-1.0, -0.8, 0], [-1.0, 1.4, 0], color=MEASURE, stroke_width=2)
        stage(grid_a, grid_b, shift_line)
        sub("晶界、层错、表面，都会让局部错开")

        # 08
        self.cue("S05_08")
        head("局部缺陷，XRD 会平均掉")
        curve = ParametricFunction(lambda t: np.array([-4.8 + 9.6 * t,
                                                        -1.2 + 0.7 * math.exp(-((t - 0.35) / 0.08) ** 2)
                                                        + 0.5 * math.exp(-((t - 0.62) / 0.10) ** 2), 0]),
                                    t_range=[0, 1], color=MEASURE, stroke_width=2)
        stage(curve)
        sub("或者只剩一点展宽，缺陷位置丢了")

        # 09
        self.cue("S05_09")
        head("投影：亮点可能重叠")
        img1 = ImageMobject(sim).set_height(4.2).move_to(RIGHT * 1.4 + DOWN * 0.1)
        img2 = ImageMobject(sim).set_height(4.2).move_to(RIGHT * 1.4 + DOWN * 0.1)
        img2.set_opacity(0.35).shift(RIGHT * 0.30 + UP * 0.25)
        stage(img1, img2)
        sub("亮点密的地方，可能是几层原子正好重叠")

        # 10
        self.cue("S05_10")
        head("换一个带轴，再看一次")
        img = ImageMobject(thick).set_height(4.2).move_to(RIGHT * 1.4 + DOWN * 0.1)
        stage(img)
        self.play_t(Rotate(img, angle=0.12, about_point=img.get_center()), run_time=0.8)
        sub("转个角度，确认它到底是不是一列原子")
        self.finish()


# --------------------------------------------------------------------------- S06
class S06(TimelineScene):
    section_id = "S06"

    def construct(self):
        self.camera.frame.set(width=13.0, height=7.31)
        self.head = None
        self.sub = None
        self.stage_group = None

        def head(text, color=INK, size=38):
            new = title(text, font_size=size, color=color).move_to(UP * 2.7)
            if self.head is None:
                self.play_t(FadeIn(new), run_time=0.5)
            else:
                self.play_t(FadeOut(self.head), FadeIn(new), run_time=0.4)
            self.head = new

        def sub(text, color=INK, size=24):
            if not SHOW_SCENE_SUBS:
                return
            new = txt(text, size=size, color=color).move_to(DOWN * 2.75)
            if self.sub is None:
                self.play_t(FadeIn(new), run_time=0.4)
            else:
                self.play_t(FadeOut(self.sub), FadeIn(new), run_time=0.35)
            self.sub = new

        def stage(*mobs):
            new = Group(*mobs)
            if self.stage_group is not None:
                self.play_t(FadeOut(self.stage_group), FadeIn(new), run_time=0.5)
            else:
                self.play_t(FadeIn(new), run_time=0.6)
            self.stage_group = new

        # 01
        self.cue("S06_01")
        head("电子束不是旁观者")
        beam = ray(LEFT * 5.0 + UP * 1.8, LEFT * 2.6 + DOWN * 0.2, width=3)
        spot = radial_glow(LEFT * 2.6 + DOWN * 0.2, 0.7, MEASURE, layers=18, max_opacity=0.35)
        stage(beam, spot)
        sub("它打在样品上，样品也在被它改变")

        # 02
        self.cue("S06_02")
        head("撞离位置，打断化学键")
        atoms = VGroup(*[Dot([-3.6 + i * 0.55, 0.3, 0], radius=0.08, color=INK)
                         for i in range(8)])
        bonds = VGroup(*[Line(atoms[i].get_center(), atoms[i + 1].get_center(),
                              color=GRID, stroke_width=1.4) for i in range(7)])
        broken = Line(atoms[3].get_center(), atoms[4].get_center(),
                      color=MEASURE, stroke_width=2.5)
        shift = Arrow(atoms[3].get_center() + DOWN * 0.15, atoms[3].get_center() + DOWN * 0.9,
                      color=MEASURE, stroke_width=2)
        stage(atoms, bonds, broken, shift)
        sub("聚合物、生物样品、一些氧化物，尤其怕")

        # 03
        self.cue("S06_03")
        head("谁最怕电子束")
        tags = VGroup(tag("聚合物", 20, MUTED), tag("生物样品", 20, MUTED),
                      tag("部分氧化物", 20, MEASURE))
        tags.arrange(RIGHT, buff=0.25).move_to(DOWN * 0.2)
        stage(tags)
        sub("剂量稍大，结构就变了")

        # 04
        self.cue("S06_04")
        head("辐照会改变化学")
        before = card("GaOOH", ["羟基氧化镓"], BEAM, 3.4, 1.9).move_to(LEFT * 3.4)
        after = card("Ga2O3", ["氧化镓"], MEASURE, 3.4, 1.9).move_to(RIGHT * 3.4)
        arr = Arrow(LEFT * 1.2, RIGHT * 1.2, color=MEASURE, stroke_width=3)
        stage(before, after, arr)
        sub("一个常被提到的例子")

        # 05
        self.cue("S06_05")
        head("看着看着，它变了")
        frames = VGroup()
        for i, c in enumerate(["#1B4A3A", "#2E6E4E", "#8A6A32"]):
            frames.add(RoundedRectangle(width=2.2, height=1.4, corner_radius=0.08,
                                       stroke_color=MUTED, stroke_width=1.2,
                                       fill_color=c, fill_opacity=0.85)
                        .move_to(LEFT * 3.0 + RIGHT * i * 3.0))
        stage(frames)
        sub("你本来想看它，结果它已经被电子束改了")

        # 06
        self.cue("S06_06")
        head("低剂量成像")
        bars = VGroup(*[Rectangle(width=0.18, height=0.7 - i * 0.10, stroke_width=0,
                                  fill_color=BEAM, fill_opacity=0.7)
                         .move_to(LEFT * 4.0 + DOWN * 0.4 + RIGHT * i * 0.24)
                         for i in range(6)])
        det = RoundedRectangle(width=2.2, height=0.9, corner_radius=0.08,
                               stroke_color=BEAM, stroke_width=1.5,
                               fill_color="#101A28", fill_opacity=1).move_to(RIGHT * 2.2 + DOWN * 0.4)
        stage(bars, det)
        sub("电子数压到刚好够成像，用更灵敏的探测器")

        # 07
        self.cue("S06_07")
        head("冷冻电镜")
        cold = tag("液氮 / 液氦温度", 22, BEAM).move_to(DOWN * 0.2)
        stage(cold)
        sub("把样品冻起来，走的就是这条路")

        # 08
        self.cue("S06_08")
        head("更根本的限制：取样")
        bulk = RoundedRectangle(width=5.0, height=2.6, corner_radius=0.08,
                                stroke_color=MUTED, stroke_width=1.4,
                                fill_color="#101A28", fill_opacity=1).move_to(DOWN * 0.1)
        thin = Rectangle(width=0.9, height=0.8, color=BEAM, fill_color=BEAM,
                         fill_opacity=0.22).move_to(bulk.get_center() + RIGHT * 1.4)
        stage(bulk, thin)
        sub("电镜看的是薄区")

        # 09
        self.cue("S06_09")
        head("薄区 ≠ 整块材料")
        bulk = RoundedRectangle(width=5.0, height=2.6, corner_radius=0.08,
                                stroke_color=MUTED, stroke_width=1.4,
                                fill_color="#101A28", fill_opacity=1).move_to(DOWN * 0.1)
        regions = VGroup(*[Circle(radius=0.18, color=MEASURE, stroke_width=1.5)
                           .move_to(bulk.get_center() + np.array([x, y, 0]))
                           for x, y in [(-1.5, 0.6), (0.2, -0.5), (1.6, 0.4)]])
        stage(bulk, regions)
        sub("要多看几个区域，才敢说话")

        # 10
        self.cue("S06_10")
        head("X 射线：平均")
        xbeam = ray(LEFT * 5.4 + UP * 1.6, RIGHT * 4.0 + DOWN * 0.6, color=MEASURE, width=4)
        grains = VGroup(*[Dot([-2.0 + i * 0.45, 0.2 + (i % 3) * 0.25, 0],
                              radius=0.07, color=INK) for i in range(9)])
        stage(xbeam, grains)
        sub("束斑大，结果是平均")

        # 11
        self.cue("S06_11")
        head("一个给平均，一个给局部")
        a = card("X 射线", ["平均", "不会只挑薄区"], MEASURE, 4.2, 2.0).move_to(LEFT * 3.3)
        b = card("电镜", ["局部", "但可能改样品"], BEAM, 4.2, 2.0).move_to(RIGHT * 3.3)
        stage(a, b)
        sub("两种眼睛，看到的是两种真实")

        # 12/13
        self.cue("S06_12")
        head("薄的那个，还可能把样品改掉", MEASURE, 30)
        sub("这不是谁更高级，是回答的问题不同")
        self.finish()


# --------------------------------------------------------------------------- S07
class S07(TimelineScene):
    section_id = "S07"

    def construct(self):
        self.camera.frame.set(width=13.0, height=7.31)
        self.head = None
        self.sub = None
        self.stage_group = None

        def head(text, color=INK, size=38):
            new = title(text, font_size=size, color=color).move_to(UP * 2.7)
            if self.head is None:
                self.play_t(FadeIn(new), run_time=0.5)
            else:
                self.play_t(FadeOut(self.head), FadeIn(new), run_time=0.4)
            self.head = new

        def sub(text, color=INK, size=24):
            if not SHOW_SCENE_SUBS:
                return
            new = txt(text, size=size, color=color).move_to(DOWN * 2.75)
            if self.sub is None:
                self.play_t(FadeIn(new), run_time=0.4)
            else:
                self.play_t(FadeOut(self.sub), FadeIn(new), run_time=0.35)
            self.sub = new

        def stage(*mobs):
            new = Group(*mobs)
            if self.stage_group is not None:
                self.play_t(FadeOut(self.stage_group), FadeIn(new), run_time=0.5)
            else:
                self.play_t(FadeIn(new), run_time=0.6)
            self.stage_group = new

        # 01
        self.cue("S07_01")
        head("同一块材料，两种眼睛")
        block = RoundedRectangle(width=3.0, height=1.9, corner_radius=0.10,
                                 stroke_color=MUTED, stroke_width=1.4,
                                 fill_color="#101A28", fill_opacity=1).move_to(DOWN * 0.1)
        stage(block)
        sub("X 射线和电镜，看的是同一块材料的两个侧面")

        # 02
        self.cue("S07_02")
        head("X 射线说")
        xrd = card("X 射线", ["纯相", "晶粒 20 nm"], BEAM, 4.2, 2.2).move_to(LEFT * 3.2 + DOWN * 0.1)
        stage(xrd)
        sub("平均结构：物相和晶粒尺寸")

        # 03
        self.cue("S07_03")
        head("电镜说")
        tem = card("电镜", ["晶界第二相", "一颗大晶粒"], MEASURE, 4.2, 2.2).move_to(RIGHT * 3.2 + DOWN * 0.1)
        stage(tem)
        sub("局部结构：晶界、第二相、个别晶粒")

        # 04
        self.cue("S07_04")
        head("两个结果都没错")
        xrd = card("X 射线", ["纯相", "晶粒 20 nm"], BEAM, 4.2, 2.2).move_to(LEFT * 3.2 + DOWN * 0.1)
        tem = card("电镜", ["晶界第二相", "一颗大晶粒"], MEASURE, 4.2, 2.2).move_to(RIGHT * 3.2 + DOWN * 0.1)
        stage(xrd, tem)
        sub("它们回答的不是同一个问题")

        # 05
        self.cue("S07_05")
        head("哪一种真实？", BEAM, 42)
        q = txt("手里只有一张图时，\n你怎么知道它说的是哪一种真实？", 26, INK).move_to(DOWN * 0.2)
        nxt = tag("下一期：两种眼睛", 20, BEAM).move_to(DOWN * 1.8)
        stage(q, nxt)
        sub("看见原子 · 第二期")
        self.finish()

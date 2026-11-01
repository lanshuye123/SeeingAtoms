"""Black-background, upward-scrolling S02 end credits."""
from __future__ import annotations

import sys
from pathlib import Path

from manim import DOWN, LEFT, UP, Line, Scene, Text, VGroup, linear

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

INK = "#F4F1EA"
MUTED = "#AAB2C0"
AMBER = "#D8A657"
BLACK = "#000000"


def line(text: str, size: int = 20, color: str = INK):
    return Text(text, font="Source Han Sans CN", font_size=size, color=color)


class S02Credits(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        items = VGroup()

        def add(text: str, size: int = 20, color: str = INK):
            items.add(line(text, size=size, color=color))

        def gap(amount: float = 0.22):
            items.add(Line(UP * (amount / 2), DOWN * (amount / 2), stroke_opacity=0))

        add("看见原子", size=40, color=INK)
        add("第二期", size=24, color=AMBER)
        add("电子显微镜，如何把原子“拍”出来？", size=24, color=INK)
        gap(0.3)

        add("科学内容支持", size=22, color=AMBER)
        add("显微结构分析课程笔记", size=18, color=MUTED)
        add("X 射线晶体学课程笔记（第一期衔接）", size=18, color=MUTED)
        gap(0.25)

        add("字体", size=22, color=AMBER)
        add("思源黑体 / 思源宋体 — Adobe（SIL Open Font License 1.1）", size=18, color=MUTED)
        add("霞鹜文楷 — LXGW（SIL Open Font License 1.1）", size=18, color=MUTED)
        gap(0.25)

        add("工具", size=22, color=AMBER)
        add("Manim — Manim Community", size=18, color=MUTED)
        add("FFmpeg — Fabrice Bellard 与 FFmpeg 团队", size=18, color=MUTED)
        add("Qwen3-TTS — 阿里巴巴通义千问团队", size=18, color=MUTED)
        add("Stable Diffusion 1.5 — Stability AI / 社区权重", size=18, color=MUTED)
        add("LMMS + GeneralUser GS — LMMS 社区 / S. Christian Collins", size=18, color=MUTED)
        add("Python — Python Software Foundation", size=18, color=MUTED)
        add("TeX Live / XeLaTeX — TeX Users Group 与社区贡献者", size=18, color=MUTED)
        gap(0.25)

        add("图像素材", size=22, color=AMBER)
        add("CDC / C. Duncan，1965 年透射电镜照片（公共领域）", size=18, color=MUTED)
        add("NIST：石墨烯芯片、月尘颗粒 SEM 图（公共领域，Credit NIST）", size=18, color=MUTED)
        add("SrTiO₃ [001] 模拟高分辨像：本项目计算（非实测）", size=18, color=MUTED)
        add("AI 氛围插图：本项目以 Stable Diffusion 1.5 生成", size=18, color=MUTED)
        gap(0.25)

        add("AI 协作", size=22, color=AMBER)
        add("DeepSeek-V4.1-Flash-1017", size=20, color=INK)
        gap(0.25)

        add("参考资料（GB/T 7714）", size=22, color=AMBER)
        refs = [
            "[1] WILLIAMS D B, CARTER C B. Transmission electron microscopy:",
            "    a textbook for materials science[M]. 2nd ed. New York: Springer, 2009.",
            "[2] GRUENE T, MUGNAIOLI E. 3D electron diffraction for chemical analysis:",
            "    instrumentation developments and innovative applications[J].",
            "    Chemical Reviews, 2021, 121(19): 11823-11834.",
            "[3] COD 1577245. SrTiO3, Pm-3m, a = 3.90541 Å[DB/OL]. [2026-11-01].",
            "    https://www.crystallography.net/cod/1577245.html.",
            "[4] NIST. Electron microscopy image gallery[DB/OL]. [2026-11-01].",
            "    https://www.nist.gov/image-gallery.",
            "[5] The Nobel Prize in Chemistry 2017[EB/OL]. [2026-11-01].",
            "    https://www.nobelprize.org/prizes/chemistry/2017/summary/.",
        ]
        for r in refs:
            add(r, size=15, color=MUTED)
        gap(0.3)

        add("看见原子 · 第二期", size=24, color=INK)
        add("下一期：同一块材料，为什么两种“眼睛”看到的不一样？", size=20, color=AMBER)
        gap(0.4)
        add("感谢观看", size=20, color=MUTED)

        items.arrange(DOWN, buff=0.10, center=True)
        items.move_to(DOWN * (2.0 + items.height / 2))
        self.add(items)
        self.play(items.animate.shift(UP * (items.height + 6.0)),
                  run_time=68.0, rate_func=linear)

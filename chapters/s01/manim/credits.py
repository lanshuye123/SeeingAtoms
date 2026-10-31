"""Black-background, upward-scrolling end credits for S01."""
from __future__ import annotations

import sys
from pathlib import Path

from manim import DOWN, LEFT, UP, FadeIn, Line, Scene, Text, VGroup, linear

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.render.theme import COLORS  # noqa: E402

INK = "#F4F1EA"
MUTED = "#AAB2C0"
AMBER = "#D8A657"
BLACK = "#000000"


def line(text: str, size: int = 20, color: str = INK):
    return Text(text, font="Source Han Sans CN", font_size=size, color=color)


class S10Credits(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        items = VGroup()

        def add(text: str, size: int = 20, color: str = INK, buff: float = 0.12):
            t = line(text, size=size, color=color)
            t.set_opacity(0.96)
            items.add(t)

        def gap(amount: float = 0.25):
            spacer = Line(UP * (amount / 2), DOWN * (amount / 2), stroke_opacity=0)
            items.add(spacer)

        add("看见原子", size=40, color=INK)
        add("第一期", size=24, color=AMBER)
        add("一束 X 射线，如何读出原子排列？", size=24, color=INK)
        gap(0.25)

        add("字体", size=22, color=AMBER)
        add("思源黑体 / 思源宋体 — Adobe（SIL Open Font License 1.1）", size=18, color=MUTED)
        add("霞鹜文楷 — LXGW（SIL Open Font License 1.1）", size=18, color=MUTED)
        gap(0.25)

        add("工具", size=22, color=AMBER)
        add("FFmpeg — Fabrice Bellard 与 FFmpeg 团队", size=18, color=MUTED)
        add("Manim — Manim Community", size=18, color=MUTED)
        add("Qwen3-TTS — 阿里巴巴通义千问团队", size=18, color=MUTED)
        add("Python — Python Software Foundation", size=18, color=MUTED)
        add("TeX Live / XeLaTeX — TeX Users Group 与社区贡献者", size=18, color=MUTED)
        gap(0.25)

        add("AI 协作", size=22, color=AMBER)
        add("DeepSeek-V4.1-Flash-1017", size=20, color=INK)
        gap(0.25)

        add("开放晶体结构数据", size=22, color=AMBER)
        add("Crystallography Open Database (COD)：9008565、9004141", size=18, color=MUTED)
        add("原始文献：Wyckoff (1963)；Meagher & Lager (1979)", size=18, color=MUTED)
        gap(0.25)

        add("参考资料（GB/T 7714）", size=22, color=AMBER)
        refs = [
            "[1] 叶李华. 科普创作经验谈：技巧、原则与怀疑精神[EB/OL]. (2020-04-03)[2026-10-31].",
            "    https://www.chinawriter.com.cn/n1/2020/0403/c404080-31660301.html.",
            "[2] 网易号. 「AI 味」的本质是什么？你可能搞错了！[EB/OL]. (2026-01-05)[2026-10-31].",
            "    https://m.163.com/dy/article/KIGAVOME0511805E.html.",
            "[3] 阿里云开发者社区. 去不掉的 AI 味儿[EB/OL]. (2026-09-19)[2026-10-31].",
            "    https://developer.aliyun.com/article/1764611.",
            "[4] BRAGG W H, BRAGG W L. The reflexion of X-rays by crystals[J].",
            "    Proceedings of the Royal Society A, 1913, 88(605): 428-438.",
            "    DOI: 10.1098/rspa.1913.0040.",
            "[5] GRUENE T, MUGNAIOLI E. 3D electron diffraction for chemical analysis:",
            "    instrumentation developments and innovative applications[J].",
            "    Chemical Reviews, 2021, 121(19): 11823-11834. DOI: 10.1021/acs.chemrev.1c00207.",
            "[6] CULLITY B D, STOCK S R. Elements of X-ray diffraction[M]. 3rd ed.",
            "    Upper Saddle River: Prentice Hall, 2001.",
            "[7] WILLIAMS D B, CARTER C B. Transmission electron microscopy:",
            "    a textbook for materials science[M]. 2nd ed. New York: Springer, 2009.",
            "[8] WYCKOFF R W G. Crystal structures[M]. 2nd ed. New York:",
            "    Interscience Publishers, 1963: 7-83.",
            "[9] MEAGHER E P, LAGER G A. Polyhedral thermal expansion in the TiO2",
            "    polymorphs: refinement of the crystal structure of rutile and brookite",
            "    at high temperature[J]. The Canadian Mineralogist, 1979, 17: 77-85.",
            "[10] NIST. X-ray transition energies database[DB/OL]. [2026-10-31].",
            "     https://physics.nist.gov/PhysRefData/XrayTrans/Html/search.html.",
            "[11] OpenStax. University physics: volume 3[EB/OL]. [2026-10-31].",
            "     https://openstax.org/books/university-physics-volume-3/pages/4-6-x-ray-diffraction.",
        ]
        for r in refs:
            add(r, size=15, color=MUTED)
        gap(0.25)

        add("看见原子 · 第一期", size=24, color=INK)
        add("下期：电子显微镜，如何把原子“拍”出来？", size=20, color=AMBER)
        gap(0.4)
        add("感谢观看", size=20, color=MUTED)

        # Tight, film-credit-like spacing.
        items.arrange(DOWN, buff=0.10, center=True)
        items.move_to(DOWN * (2.0 + items.height / 2))
        self.add(items)
        self.play(
            items.animate.shift(UP * (items.height + 6.0)),
            run_time=70.0,
            rate_func=linear,
        )

#!/usr/bin/env python3
"""Apply the S02 duotone grade to the raw AI illustrations.

The raw SD images are desaturated on purpose; this script maps luminance
through a three-stop palette so every illustration shares the series colours
(deep navy shadows, teal midtones, amber or teal highlights).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "chapters" / "s02" / "assets" / "illustrations"

PALETTES = {
    "ai_01_copper_grid": ((11, 16, 32), (68, 54, 40), (216, 166, 87)),
    "ai_02_column": ((11, 16, 32), (28, 52, 58), (111, 211, 199)),
    "ai_03_beam_slab": ((8, 12, 26), (24, 58, 64), (111, 211, 199)),
    "ai_04_phase": ((11, 16, 32), (44, 88, 90), (216, 166, 87)),
    "ai_05_lab": ((11, 16, 32), (26, 48, 54), (111, 211, 199)),
    "ai_06_phosphor": ((5, 14, 12), (24, 70, 48), (126, 220, 160)),
}


def colorize(lum: np.ndarray, shadow, mid, highlight) -> np.ndarray:
    s = np.array(shadow, dtype=np.float32)
    m = np.array(mid, dtype=np.float32)
    h = np.array(highlight, dtype=np.float32)
    x = lum[..., None]
    low = s + (m - s) * np.clip(x / 0.5, 0, 1)
    high = m + (h - m) * np.clip((x - 0.5) / 0.5, 0, 1)
    return np.where(x < 0.5, low, high)


def main() -> int:
    for name, palette in PALETTES.items():
        src = OUT / f"{name}.png"
        if not src.exists():
            print(f"skip {name}: raw image missing")
            continue
        img = Image.open(src).convert("RGB").resize((1920, 1080), Image.LANCZOS)
        a = np.asarray(img).astype(np.float32) / 255.0
        lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
        lum = np.clip((lum - 0.08) * 1.15, 0, 1)
        graded = colorize(lum, *palette)
        graded = 0.78 * graded + 0.22 * a * 255.0
        yy, xx = np.mgrid[-1:1:1080j, -1:1:1920j]
        vignette = 1.0 - 0.38 * np.clip((xx ** 2 + yy ** 2) - 0.22, 0, 1)
        graded *= vignette[..., None]
        rng = np.random.default_rng(7)
        graded += rng.normal(0, 2.6, graded.shape)
        dst = OUT / f"{name}_graded.png"
        Image.fromarray(np.clip(graded, 0, 255).astype(np.uint8)).save(dst)
        print(f"graded {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

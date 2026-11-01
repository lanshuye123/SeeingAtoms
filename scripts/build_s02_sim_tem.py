#!/usr/bin/env python3
"""Simulate a teaching-grade HRTEM image of SrTiO3 along [001].

This is a weak-phase-object + CTF calculation, not a full multislice run and
not an experimental image. It is deliberately labelled as a simulation in the
video and in the metadata. It exists to explain three things:

1. bright dots sit on atomic columns, not on single atoms;
2. the dot pattern is a projection through the foil thickness;
3. defocus reverses the dot contrast.

For legibility the default model keeps only the Sr column (the heaviest one),
so the bright dots form a square lattice with the SrTiO3 lattice parameter
a = 3.905 A. A faint Ti/O contribution can be enabled with --full-columns.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "chapters" / "s02" / "assets" / "sim"

A = 3.905            # SrTiO3 lattice parameter, Angstrom
PIXEL = 0.08         # Angstrom per pixel
N = 512
LAMBDA = 0.0250793   # 200 kV electron wavelength, Angstrom
CS = 1.0e7           # spherical aberration, Angstrom (1 mm)
SIGMA = 0.26         # column envelope, Angstrom

SR_ONLY = [("Sr", 0.00, 0.00, 1.00)]
FULL = [
    ("Sr", 0.00, 0.00, 1.00),
    ("Ti+O", 0.50, 0.50, 0.52),
    ("O", 0.50, 0.00, 0.20),
    ("O", 0.00, 0.50, 0.20),
]


def projected_phase(thickness_nm: float, columns, seed: int = 7) -> np.ndarray:
    rng = np.random.default_rng(seed)
    half = N * PIXEL / 2
    xs = (np.arange(N) - N / 2) * PIXEL
    X, Y = np.meshgrid(xs, xs)
    phase = np.zeros((N, N), dtype=np.float64)
    scale = thickness_nm / 5.0

    cells = int(np.ceil(half / A)) + 2
    for i in range(-cells, cells + 1):
        for j in range(-cells, cells + 1):
            for _, fx, fy, amp in columns:
                cx = (i + fx) * A
                cy = (j + fy) * A
                if abs(cx) > half + 3 * SIGMA or abs(cy) > half + 3 * SIGMA:
                    continue
                phase += amp * scale * np.exp(
                    -((X - cx) ** 2 + (Y - cy) ** 2) / (2 * SIGMA ** 2))

    # A slight thickness wedge; real foils are never perfectly flat.
    wedge = 0.06 * (X / half) + 0.04 * (Y / half)
    phase *= 1.0 + wedge
    return phase


def ctf(defocus_nm: float, aperture: float) -> np.ndarray:
    kx = np.fft.fftfreq(N, d=PIXEL)
    KX, KY = np.meshgrid(kx, kx)
    k2 = KX ** 2 + KY ** 2
    k = np.sqrt(k2)
    df = defocus_nm * 10.0  # nm -> Angstrom
    chi = np.pi * LAMBDA * k2 * (0.5 * CS * LAMBDA ** 2 * k2 - df)
    edge = np.clip((aperture - k) / (0.08 * aperture), 0.0, 1.0)
    return np.sin(chi) * (k <= aperture) * edge


def render(thickness_nm: float, defocus_nm: float, aperture: float,
           dose: float, seed: int, columns) -> np.ndarray:
    phase = projected_phase(thickness_nm, columns, seed=seed)
    exit_wave = np.exp(1j * phase)
    image_wave = np.fft.ifft2(np.fft.fft2(exit_wave) * ctf(defocus_nm, aperture))
    intensity = np.abs(image_wave) ** 2

    scale = dose / max(intensity.mean(), 1e-9)
    counts = np.random.default_rng(seed + 1).poisson(intensity * scale)
    noisy = counts / scale

    yy, xx = np.mgrid[-1:1:N * 1j, -1:1:N * 1j]
    noisy *= 1.0 - 0.08 * (xx ** 2 + yy ** 2)

    lo, hi = np.percentile(noisy, [0.5, 99.5])
    out = np.clip((noisy - lo) / max(hi - lo, 1e-9), 0, 1)
    return (out ** 0.9 * 255).astype(np.uint8)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-columns", action="store_true",
                        help="include Ti/O columns (less legible, more realistic)")
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    columns = FULL if args.full_columns else SR_ONLY
    specs = [
        ("sim_srtio3_001_sr_under.png", 5.0, -20.0, 0.30, 2400.0, 7,
         "5 nm, defocus -20 nm, Sr column bright"),
        ("sim_srtio3_001_sr_over.png", 5.0, 20.0, 0.30, 2400.0, 7,
         "5 nm, defocus +20 nm, Sr column dark"),
        ("sim_srtio3_001_sr_thick.png", 12.0, -20.0, 0.30, 2400.0, 11,
         "12 nm, defocus -20 nm, projection through more cells"),
    ]
    meta = {
        "material": "SrTiO3",
        "zone_axis": "[001]",
        "accelerating_voltage_kV": 200,
        "electron_wavelength_A": LAMBDA,
        "lattice_parameter_A": A,
        "pixel_size_A": PIXEL,
        "field_of_view_A": [N * PIXEL, N * PIXEL],
        "cs_mm": CS / 1e7,
        "columns_rendered": "Sr only (default)" if not args.full_columns else "Sr + Ti + O",
        "model": "weak phase object + CTF (not multislice)",
        "note": "模拟计算，非实测；用于讲解原子列投影与相位衬度，不作为实验数据。"
                "默认只画锶原子列，所以亮点构成 3.905 埃的方格子；这不代表钛、氧不存在。",
        "images": [],
    }
    for name, thickness, defocus, aperture, dose, seed, label in specs:
        img = render(thickness, defocus, aperture, dose, seed, columns)
        Image.fromarray(img, mode="L").save(OUT / name)
        meta["images"].append({
            "file": name,
            "thickness_nm": thickness,
            "defocus_nm": defocus,
            "aperture_inv_A": aperture,
            "label": label,
        })
        print(f"wrote {OUT / name}")
    (OUT / "sim_srtio3_001.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

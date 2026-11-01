#!/usr/bin/env python3
"""Generate S02 atmosphere illustrations with a local Stable Diffusion 1.5.

These are *atmosphere* images only: copper grid, instrument silhouettes, beam,
phosphor glow. They never carry quantitative scientific information; all
diagrams and data stay in Manim / the simulated HRTEM set.

Model : Stable Diffusion v1.5 (single-file checkpoint, ModelScope mirror)
License: CreativeML Open RAIL-M; generated images are usable, the model is not
         redistributed with the video.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "chapters" / "s02" / "assets" / "illustrations"
CKPT = Path("/home/lanshuye/Projects/QwenTTS/sd15/sd15.safetensors")

NEGATIVE = (
    "text, watermark, logo, signature, letters, words, blurry, low quality, "
    "people, hands, face, cartoon, anime, 3d render, oversaturated, neon, "
    "sci-fi spaceship, glowing particles, clutter"
)

PROMPTS = [
    {
        "id": "ai_01_copper_grid",
        "prompt": "macro photograph of a small round copper electron microscopy grid with a thin "
                  "transparent sample in the center, held by stainless steel tweezers, dark navy "
                  "background, shallow depth of field, realistic, soft teal rim light, high detail",
        "seed": 101,
        "use": "S00 开场：铜网与薄片",
    },
    {
        "id": "ai_02_column",
        "prompt": "photograph of a tall transmission electron microscope column in a dark laboratory, "
                  "metallic instrument, small green screen glowing, cinematic, realistic, muted blue tones",
        "seed": 211,
        "use": "S00_02：样品杆与电镜",
    },
    {
        "id": "ai_03_beam_slab",
        "prompt": "extreme macro of a thin translucent crystal flake edge, backlit by a narrow teal "
                  "beam, faint amber lattice planes, dark navy background, abstract, realistic, "
                  "shallow depth of field",
        "seed": 307,
        "use": "S01/S02：电子穿过薄样品",
    },
    {
        "id": "ai_04_phase",
        "prompt": "abstract wave interference pattern, thin teal and amber lines on deep navy, "
                  "soft focus, fine ripples, minimalist scientific art, no objects",
        "seed": 401,
        "use": "S04：相位与波前",
    },
    {
        "id": "ai_05_lab",
        "prompt": "dark laboratory at night, tall metallic instrument silhouette, one small green "
                  "phosphor screen glowing, cinematic, muted, realistic, no people",
        "seed": 503,
        "use": "S00/S06：实验室氛围",
    },
    {
        "id": "ai_06_phosphor",
        "prompt": "macro close-up of a green phosphor screen glowing softly, fine grain, dark edges, "
                  "teal-green light, shallow depth of field, cinematic, realistic",
        "seed": 607,
        "use": "S00_03/S00_04：荧光屏绿光",
    },
]

def grade(src: Path, dst: Path) -> None:
    """Give all AI images the same deep-navy/teal grade as the series."""
    img = Image.open(src).convert("RGB").resize((1920, 1080), Image.LANCZOS)
    a = np.asarray(img).astype(np.float32)
    gray = a.mean(axis=2, keepdims=True)
    a = 0.45 * a + 0.55 * gray          # desaturate
    a = 0.78 * a + 0.22 * np.array([11, 16, 32], dtype=np.float32)  # navy lift
    a = np.clip((a - 128) * 1.12 + 128, 0, 255)  # contrast
    yy, xx = np.mgrid[-1:1:1080j, -1:1:1920j]
    vignette = 1.0 - 0.35 * np.clip((xx ** 2 + yy ** 2) - 0.25, 0, 1)
    a *= vignette[..., None]
    rng = np.random.default_rng(7)
    a += rng.normal(0, 3.0, a.shape)
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(dst)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    pipe = StableDiffusionPipeline.from_single_file(
        str(CKPT), torch_dtype=torch.float16, safety_checker=None,
        requires_safety_checker=False,
    )
    pipe = pipe.to("cuda")
    pipe.enable_attention_slicing()
    pipe.enable_vae_slicing()
    pipe.set_progress_bar_config(disable=True)

    records = []
    for item in PROMPTS:
        gen = torch.Generator("cuda").manual_seed(item["seed"])
        image = pipe(
            item["prompt"], negative_prompt=NEGATIVE,
            width=768, height=512, num_inference_steps=24, guidance_scale=7.0,
            generator=gen,
        ).images[0]
        path = OUT / f"{item['id']}.png"
        image.save(path)
        grade(path, OUT / f"{item['id']}_graded.png")
        records.append({**item, "file": path.name, "width": 768, "height": 512,
                        "model": "stable-diffusion-v1.5", "steps": 24,
                        "guidance": 7.0, "negative": NEGATIVE})
        print(f"wrote {path}")

    (OUT / "prompts.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Contact sheet for quick review.
    thumbs = []
    for r in records:
        img = Image.open(OUT / r["file"]).convert("RGB").resize((512, 341))
        thumbs.append(img)
    cols, rows = 2, 3
    sheet = Image.new("RGB", (cols * 512, rows * 341), (11, 16, 32))
    for i, img in enumerate(thumbs):
        sheet.paste(img, ((i % cols) * 512, (i // cols) * 341))
    sheet.save(OUT / "contact_sheet.png")
    print(f"contact sheet: {OUT / 'contact_sheet.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

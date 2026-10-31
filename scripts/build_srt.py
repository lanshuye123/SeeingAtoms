#!/usr/bin/env python3
"""Build a Chinese SRT from the sentence timing manifest.

A cue holds one sentence when it fits in two lines (<=42 characters). Longer
sentences are split at punctuation; each part is wrapped to at most two lines.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIMING = ROOT / "chapters" / "s01" / "audio" / "timing.json"
OUT = ROOT / "chapters" / "s01" / "renders" / "s01_final.srt"
MAX_LINE = 22
MAX_CUE = 38
PUNCT = "，；：、"


def nearest_punct(text: str, lo: int, hi: int, target: int) -> int | None:
    candidates = [i for i, ch in enumerate(text) if ch in PUNCT and lo <= i <= hi]
    if not candidates:
        return None
    return min(candidates, key=lambda i: abs(i - target))


def split_sentence(text: str) -> list[str]:
    text = text.strip()
    if len(text) <= MAX_CUE:
        return [text]
    mid = len(text) // 2
    cut = nearest_punct(text, max(1, mid - 12), min(len(text) - 2, mid + 12), mid)
    if cut is None:
        cut = mid
    left, right = text[: cut + 1], text[cut + 1 :].lstrip()
    if not right:
        return [left]
    return [left] + split_sentence(right)


def wrap_cue(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= MAX_LINE:
        return text
    mid = len(text) // 2
    # Keep both lines near 20 chars, not just the first one.
    cut = nearest_punct(text, max(8, len(text) - MAX_LINE - 1), min(MAX_LINE, len(text) - 1), mid)
    if cut is None:
        cut = min(MAX_LINE, len(text) - 1)
    return text[: cut + 1] + "\\N" + text[cut + 1 :].lstrip()


def fmt_time(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> int:
    data = json.loads(TIMING.read_text(encoding="utf-8"))
    cues = []
    for scene in data["scenes"]:
        for sentence in scene["sentences"]:
            chunks = split_sentence(sentence["text"])
            start, end = float(sentence["start"]), float(sentence["end"])
            total_chars = sum(len(c) for c in chunks) or 1
            t = start
            for chunk in chunks:
                share = max(0.8, (end - start) * len(chunk) / total_chars)
                cue_end = min(end, t + share)
                cues.append((t, cue_end, wrap_cue(chunk)))
                t = cue_end
    # One sentence reads badly if the wrap lands before "的方向上".
    # Split it at the first comma; keep the split reproducible.
    fixed = []
    for start, end, text in cues:
        plain = text.replace("\\N", "")
        if plain.startswith("它们往四面八方都发次波，") and "布拉格条件" in plain:
            left, right = plain.split("，", 1)
            mid = start + (end - start) * len(left + "，") / len(plain)
            fixed.append((start, mid, left + "，"))
            fixed.append((mid, end, right))
        else:
            fixed.append((start, end, text))
    cues = fixed

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for idx, (start, end, text) in enumerate(cues, 1):
        lines.append(str(idx))
        lines.append(f"{fmt_time(start)} --> {fmt_time(end)}")
        lines.append(text)
        lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} ({len(cues)} cues)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

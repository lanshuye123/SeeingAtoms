#!/usr/bin/env python3
"""Convert S02 SRT to a styled ASS for 1920x1080 burn-in."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRT = ROOT / "chapters" / "s02" / "renders" / "s02_narration.srt"
ASS = ROOT / "chapters" / "s02" / "renders" / "s02_final.ass"

HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Source Han Sans CN,46,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,80,80,42,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def ts(t: str) -> str:
    h, m, rest = t.split(":")
    s, ms = rest.split(",")
    return f"{int(h)}:{int(m):02d}:{int(s):02d}.{int(ms)//10:02d}"


def main() -> int:
    lines = [HEADER]
    for block in re.split(r"\n\s*\n", SRT.read_text(encoding="utf-8").strip()):
        parts = block.splitlines()
        if len(parts) < 3:
            continue
        times = parts[1].split(" --> ")
        lines.append(f"Dialogue: 0,{ts(times[0])},{ts(times[1])},Default,,0,0,0,,"
                     f"{chr(10).join(parts[2:])}")
    ASS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {ASS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

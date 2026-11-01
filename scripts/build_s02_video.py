#!/usr/bin/env python3
"""Assemble the S02 master: trim/pad scenes to timing, concat, mux, burn subs."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S02 = ROOT / "chapters" / "s02"
SEG = S02 / "renders" / "segments"
TIMING = S02 / "audio" / "timing.json"
AUDIO = S02 / "audio" / "s02_mix.wav"
ASS = S02 / "renders" / "s02_final.ass"
OUT = S02 / "renders" / "s02_final.mp4"
SILENT = S02 / "renders" / "s02_silent.mp4"
CREDITS = ROOT / "media" / "videos" / "credits" / "1080p30" / "S02Credits.mp4"
CRED_LEN = 68.0


def run(cmd: list[str]):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def main() -> int:
    data = json.loads(TIMING.read_text(encoding="utf-8"))
    SEG.mkdir(parents=True, exist_ok=True)
    list_lines = []
    total = 0.0
    sections = data["sections"]
    total_nar = float(data["total_duration_s"])
    for idx, sec in enumerate(sections):
        sid = sec["id"]
        src = ROOT / "media" / "videos" / "scenes" / "1080p30" / f"{sid}.mp4"
        if not src.exists():
            raise SystemExit(f"missing scene render: {src}")
        # Section duration excludes the 0.65 s gap that the narration has
        # between sections; use the next section's start so video == audio.
        if idx + 1 < len(sections):
            dur = float(sections[idx + 1]["start"]) - float(sec["start"])
        else:
            dur = total_nar - float(sec["start"])
        dst = SEG / f"{sid}.mp4"
        # Pad with the last frame if short, trim if long; re-encode once to 1080p30.
        run(["ffmpeg", "-hide_banner", "-y", "-i", str(src),
             "-vf", "tpad=stop_mode=clone:stop_duration=2",
             "-t", f"{dur:.3f}", "-r", "30",
             "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-pix_fmt", "yuv420p", "-an", str(dst)])
        list_lines.append(f"file '{dst.resolve()}'")
        total += dur
        print(f"{sid}: {dur:.3f}s")

    if not CREDITS.exists():
        raise SystemExit(f"missing credits render: {CREDITS}")
    cred_dst = SEG / "S02Credits.mp4"
    run(["ffmpeg", "-hide_banner", "-y", "-i", str(CREDITS),
         "-vf", "tpad=stop_mode=clone:stop_duration=2",
         "-t", f"{CRED_LEN:.3f}", "-r", "30",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-pix_fmt", "yuv420p", "-an", str(cred_dst)])
    list_lines.append(f"file '{cred_dst.resolve()}'")
    total += CRED_LEN
    print(f"credits: {CRED_LEN:.3f}s; total video {total:.3f}s")

    concat_txt = S02 / "renders" / "concat.txt"
    concat_txt.write_text("\n".join(list_lines) + "\n", encoding="utf-8")
    run(["ffmpeg", "-hide_banner", "-y", "-f", "concat", "-safe", "0",
         "-i", str(concat_txt), "-c", "copy", str(SILENT)])

    run(["ffmpeg", "-hide_banner", "-y", "-i", str(SILENT), "-i", str(AUDIO),
         "-vf", f"ass={ASS}:fontsdir={ROOT/'assets'/'fonts'}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "19",
         "-pix_fmt", "yuv420p", "-r", "30",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
         "-movflags", "+faststart", "-shortest",
         "-metadata", "title=看见原子 · 第二期", str(OUT)])
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

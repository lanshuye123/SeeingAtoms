#!/usr/bin/env python3
"""Normalize narration/music and build the final S01 audio timeline.

Main narration: 505.485 s; pad to 506.0 s.
Credits: 70.0 s of original ambient bed.
Final: 576.0 s (main + credits), with music under the voice.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUD = ROOT / "chapters" / "s01" / "audio"
NAR = AUD / "s01_narration.wav"
MUS = AUD / "music_main.wav"
CRED = AUD / "music_credits.wav"
OUT = AUD / "s01_mix.wav"


def run(cmd: list[str]):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def main():
    nar_norm = AUD / "narration_norm.wav"
    mus_norm = AUD / "music_main_norm.wav"
    cred_norm = AUD / "music_credits_norm.wav"
    main_mix = AUD / "mix_main.wav"

    run([
        "ffmpeg", "-hide_banner", "-y", "-i", str(NAR),
        "-af", "highpass=f=70,loudnorm=I=-18:TP=-2.0:LRA=11",
        "-ar", "48000", "-ac", "1", str(nar_norm),
    ])
    run([
        "ffmpeg", "-hide_banner", "-y", "-i", str(MUS),
        "-af", "loudnorm=I=-30:TP=-8.0:LRA=8",
        "-ar", "48000", "-ac", "1", str(mus_norm),
    ])
    run([
        "ffmpeg", "-hide_banner", "-y", "-i", str(CRED),
        "-af", "loudnorm=I=-28:TP=-6.0:LRA=8,afade=t=in:st=0:d=2,afade=t=out:st=66:d=4",
        "-ar", "48000", "-ac", "1", str(cred_norm),
    ])

    # Pad narration to 506.0 s, mix with the main bed (no amix normalization).
    run([
        "ffmpeg", "-hide_banner", "-y", "-i", str(nar_norm), "-i", str(mus_norm),
        "-filter_complex",
        "[0:a]apad=pad_dur=0.365,atrim=0:508.1[n];[1:a]atrim=0:508.1[m];"
        "[n][m]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0,"
        "loudnorm=I=-16:TP=-1.5:LRA=11[a]",
        "-map", "[a]", "-ar", "48000", "-ac", "1", "-t", "508.1", str(main_mix),
    ])

    run([
        "ffmpeg", "-hide_banner", "-y", "-i", str(main_mix), "-i", str(cred_norm),
        "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[a]",
        "-map", "[a]", "-ar", "48000", "-ac", "1", "-t", "578.1", str(OUT),
    ])
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

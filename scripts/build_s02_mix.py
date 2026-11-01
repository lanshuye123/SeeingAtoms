#!/usr/bin/env python3
"""Build the final S02 audio: narration + original music + credits bed."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUD = ROOT / "chapters" / "s02" / "audio"
MUS = ROOT / "chapters" / "s02" / "assets" / "music" / "s02_theme.wav"
NAR = AUD / "s02_narration.wav"
OUT = AUD / "s02_mix.wav"
MAIN_LEN = 553.09
CRED_LEN = 68.0


def run(cmd: list[str]):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def main():
    nar_norm = AUD / "narration_norm.wav"
    mus_norm = AUD / "music_main_norm.wav"
    cred_norm = AUD / "music_credits_norm.wav"
    main_mix = AUD / "mix_main.wav"

    run(["ffmpeg", "-hide_banner", "-y", "-i", str(NAR),
         "-af", "highpass=f=70,loudnorm=I=-18:TP=-2.0:LRA=11",
         "-ar", "48000", "-ac", "1", str(nar_norm)])

    # Loop the 99 s theme to the narration length, then level it as a bed.
    run(["ffmpeg", "-hide_banner", "-y", "-stream_loop", "-1", "-i", str(MUS),
         "-t", str(MAIN_LEN),
         "-af", "highpass=f=35,lowpass=f=11000,loudnorm=I=-30:TP=-8.0:LRA=8,"
                "afade=t=in:st=0:d=2,afade=t=out:st=548:d=5",
         "-ar", "48000", "-ac", "1", str(mus_norm)])

    run(["ffmpeg", "-hide_banner", "-y", "-i", str(nar_norm), "-i", str(mus_norm),
         "-filter_complex",
         "[0:a]apad=pad_dur=0.2,atrim=0:553.09[n];"
         "[1:a]atrim=0:553.09[m];"
         "[n][m]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0,"
         "loudnorm=I=-16:TP=-1.5:LRA=11[a]",
         "-map", "[a]", "-ar", "48000", "-ac", "1", "-t", "553.09", str(main_mix)])

    run(["ffmpeg", "-hide_banner", "-y", "-stream_loop", "-1", "-i", str(MUS),
         "-t", str(CRED_LEN),
         "-af", "highpass=f=35,lowpass=f=10000,loudnorm=I=-28:TP=-6.0:LRA=8,"
                "afade=t=in:st=0:d=2,afade=t=out:st=62:d=6",
         "-ar", "48000", "-ac", "1", str(cred_norm)])

    run(["ffmpeg", "-hide_banner", "-y", "-i", str(main_mix), "-i", str(cred_norm),
         "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[a]",
         "-map", "[a]", "-ar", "48000", "-ac", "1", "-t", "621.09", str(OUT)])
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Synthesize a simple original ambient bed (no third-party samples).

This is intentionally low-key: slow chord pads, a sub drone, and filtered noise.
The final mix keeps it well below the narration.
"""
from __future__ import annotations

import argparse
import wave
from pathlib import Path

import numpy as np
from scipy.signal import butter, lfilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "chapters" / "s01" / "audio"
SR = 48000

CHORDS = [
    [110.00, 164.81, 220.00, 261.63, 329.63],  # A minor-ish
    [87.31, 130.81, 174.61, 220.00, 261.63],    # F
    [130.81, 196.00, 261.63, 329.63, 392.00],   # C
    [98.00, 146.83, 196.00, 246.94, 293.66],    # G
]


def lowpass(x: np.ndarray, cutoff: float, order: int = 2) -> np.ndarray:
    b, a = butter(order, cutoff / (SR / 2), btype="low")
    return lfilter(b, a, x)


def make_bed(duration: float, seed: int = 1) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = int(round(duration * SR))
    t = np.arange(n, dtype=np.float64) / SR
    out = np.zeros(n, dtype=np.float64)

    # Chord pads, 8 s per chord, with a slow crossfade.
    seg = 8.0
    for start in np.arange(0, duration, seg):
        idx = int(start * SR)
        end = min(n, int((start + seg) * SR))
        if end <= idx:
            continue
        tt = t[idx:end] - t[idx]
        chord = CHORDS[int(start // seg) % len(CHORDS)]
        env = np.sin(np.pi * np.clip(tt / seg, 0, 1)) ** 2
        for k, f in enumerate(chord):
            amp = 1.0 / (k + 2)
            out[idx:end] += amp * env * np.sin(2 * np.pi * f * tt + k * 0.7)
            out[idx:end] += 0.35 * amp * env * np.sin(2 * np.pi * (f * 1.003) * tt + 1.1)

    # Sub drone and a very quiet high shimmer.
    out += 0.18 * np.sin(2 * np.pi * 55.0 * t)
    out += 0.035 * np.sin(2 * np.pi * 880.0 * t + 0.2) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.02 * t))

    # Filtered noise, slowly modulated.
    noise = lowpass(rng.normal(0, 1, n), 900.0, order=2)
    noise /= max(1e-9, np.max(np.abs(noise)))
    out += 0.05 * noise * (0.5 + 0.5 * np.sin(2 * np.pi * 0.013 * t + 0.7))

    # Slow breathing amplitude.
    out *= 0.70 + 0.12 * np.sin(2 * np.pi * 0.008 * t)

    # Fades.
    fade = min(4.0, duration / 4)
    nf = int(fade * SR)
    out[:nf] *= np.linspace(0, 1, nf)
    out[-nf:] *= np.linspace(1, 0, nf)
    out /= max(1e-9, np.max(np.abs(out)))
    return (out * 0.22).astype(np.float32)


def write_wav(path: Path, data: np.ndarray):
    pcm = np.clip(data, -1, 1)
    pcm = (pcm * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--main-duration", type=float, default=506.5)
    parser.add_argument("--credits-duration", type=float, default=70.0)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    write_wav(OUT / "music_main.wav", make_bed(args.main_duration, seed=3))
    write_wav(OUT / "music_credits.wav", make_bed(args.credits_duration, seed=9))
    print(f"wrote {OUT/'music_main.wav'} ({args.main_duration:.1f}s)")
    print(f"wrote {OUT/'music_credits.wav'} ({args.credits_duration:.1f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

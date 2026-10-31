#!/usr/bin/env python3
"""Build scene narration and a timing manifest from sentence-level TTS.

Sentence-level generation gives us exact per-sentence durations for subtitles.
The final narration is slowed slightly with atempo (default 0.95) and scenes are
joined with short pauses.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "chapters" / "s01" / "audio" / "sentences" / "manifest.json"
RAW_DIR = ROOT / "chapters" / "s01" / "audio" / "scenes_raw"
OUT_DIR = ROOT / "chapters" / "s01" / "audio" / "scenes_95"
FINAL = ROOT / "chapters" / "s01" / "audio" / "s01_narration.wav"
TIMING = ROOT / "chapters" / "s01" / "audio" / "timing.json"


def write_silence(path: Path, seconds: float, rate: int = 24000) -> None:
    frames = int(round(seconds * rate))
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(b"\x00\x00" * frames)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def duration(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip()
    return float(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tempo", type=float, default=0.95, help="atempo factor (<1 = slower)")
    parser.add_argument("--sentence-gap", type=float, default=0.30)
    parser.add_argument("--scene-gap", type=float, default=0.50)
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    silence_sentence = RAW_DIR / "sil_sentence.wav"
    silence_scene = RAW_DIR / "sil_scene.wav"
    write_silence(silence_sentence, args.sentence_gap, rate=24000)
    write_silence(silence_scene, args.scene_gap, rate=48000)

    items = json.loads(MANIFEST.read_text(encoding="utf-8"))
    scenes: dict[str, list[dict]] = {}
    for item in items:
        scene = item["id"].split("_")[0]
        scenes.setdefault(scene, []).append(item)

    timing_scenes = []
    scene_files = []
    cursor = 0.0
    all_sentences = 0
    for scene_id in sorted(scenes):
        scene_items = scenes[scene_id]
        concat_lines = []
        for i, item in enumerate(scene_items):
            concat_lines.append(f"file '{Path(item['path']).resolve()}'")
            if i < len(scene_items) - 1:
                concat_lines.append(f"file '{silence_sentence.resolve()}'")
        list_path = RAW_DIR / f"{scene_id}.txt"
        list_path.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")
        raw = RAW_DIR / f"{scene_id}.wav"
        run([
            "ffmpeg", "-hide_banner", "-y", "-f", "concat", "-safe", "0",
            "-i", str(list_path), "-c:a", "pcm_s16le", str(raw),
        ])
        out = OUT_DIR / f"{scene_id}.wav"
        run([
            "ffmpeg", "-hide_banner", "-y", "-i", str(raw),
            "-af", f"atempo={args.tempo}", "-ar", "48000", "-ac", "1",
            "-c:a", "pcm_s16le", str(out),
        ])
        dur = duration(out)
        scene_files.append(out)

        # Sentence timings: scale by tempo; correct a small encoder/padding drift.
        scaled = [(item, item["duration_s"] / args.tempo) for item in scene_items]
        gap = args.sentence_gap / args.tempo
        expected = sum(d for _, d in scaled) + gap * (len(scaled) - 1)
        factor = dur / expected if expected > 0 else 1.0
        sentence_times = []
        t = 0.0
        for item, d in scaled:
            dd = d * factor
            sentence_times.append({
                "id": item["id"],
                "text": item["text"],
                "start": round(cursor + t, 3),
                "end": round(cursor + t + dd, 3),
            })
            t += dd + gap * factor
        timing_scenes.append({
            "id": scene_id,
            "start": round(cursor, 3),
            "duration": round(dur, 3),
            "end": round(cursor + dur, 3),
            "sentences": sentence_times,
        })
        all_sentences += len(scene_items)
        print(f"{scene_id}: {len(scene_items)} sentences, {dur:.2f}s")
        cursor += dur + args.scene_gap
        if scene_id != sorted(scenes)[-1]:
            pass

    # Join scene files with the scene gap.
    final_list = RAW_DIR / "final.txt"
    lines = []
    for i, f in enumerate(scene_files):
        lines.append(f"file '{f.resolve()}'")
        if i < len(scene_files) - 1:
            lines.append(f"file '{silence_scene.resolve()}'")
    final_list.write_text("\n".join(lines) + "\n", encoding="utf-8")
    run([
        "ffmpeg", "-hide_banner", "-y", "-f", "concat", "-safe", "0",
        "-i", str(final_list), "-c:a", "pcm_s16le", str(FINAL),
    ])
    total = duration(FINAL)
    data = {
        "tempo": args.tempo,
        "sentence_gap_s": args.sentence_gap,
        "scene_gap_s": args.scene_gap,
        "total_duration_s": round(total, 3),
        "sentence_count": all_sentences,
        "scenes": timing_scenes,
    }
    TIMING.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"total narration: {total:.2f}s = {total/60:.2f} min")
    print(f"timing: {TIMING}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

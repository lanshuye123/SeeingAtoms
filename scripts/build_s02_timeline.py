#!/usr/bin/env python3
"""Build a sentence-locked timeline for S02.

S01 rendered each scene to a fixed target length and then dumped the remaining
time into a wait at the end of the scene. That is why the picture and the voice
"roughly" matched but drifted inside a scene.

This script fixes the cause, not the symptom:

1. every sentence has an exact start/end from the measured TTS wav;
2. every visual cue is attached to a sentence id, not to a fixed run_time;
3. the Manim scene waits until the cue's sentence starts before it animates;
4. the same timing.json drives the audio assembly, the subtitles and the QC.

Outputs:
  chapters/s02/audio/timing.json
  chapters/s02/audio/s02_narration.wav      (with --render-audio)
  chapters/s02/audio/sentences_timed/*.wav  (with --render-audio)
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S02 = ROOT / "chapters" / "s02"
SENTENCES = S02 / "script" / "sentences.json"
PROSODY = S02 / "script" / "prosody.json"
MANIFEST = S02 / "audio" / "sentences" / "manifest.json"
OUT_TIMING = S02 / "audio" / "timing.json"
OUT_WAV = S02 / "audio" / "s02_narration.wav"
TIMED_DIR = S02 / "audio" / "sentences_timed"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def duration(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)], text=True).strip()
    return float(out)


def write_silence(path: Path, seconds: float, rate: int = 48000) -> None:
    import wave
    frames = int(round(seconds * rate))
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(b"\x00\x00" * frames)


def load_prosody() -> dict:
    if PROSODY.exists():
        return json.loads(PROSODY.read_text(encoding="utf-8"))
    return {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--render-audio", action="store_true")
    parser.add_argument("--sentence-gap", type=float, default=0.35)
    parser.add_argument("--section-gap", type=float, default=0.65)
    parser.add_argument("--only-sections", default="", help="comma list, e.g. S00")
    args = parser.parse_args()

    sentences = json.loads(SENTENCES.read_text(encoding="utf-8"))
    manifest = {m["id"]: m for m in json.loads(MANIFEST.read_text(encoding="utf-8"))}
    prosody = load_prosody()

    wanted = {s.strip() for s in args.only_sections.split(",") if s.strip()}
    if wanted:
        sentences = [s for s in sentences if s["section"] in wanted]

    missing = [s["id"] for s in sentences if s["id"] not in manifest]
    if missing:
        print(f"missing {len(missing)} wav(s): {', '.join(missing[:8])}"
              + (" ..." if len(missing) > 8 else ""))
        return 2

    TIMED_DIR.mkdir(parents=True, exist_ok=True)
    sections: list[dict] = []
    cursor = 0.0
    timed_paths: list[Path] = []

    by_section: dict[str, list[dict]] = {}
    for s in sentences:
        by_section.setdefault(s["section"], []).append(s)

    for sid, items in by_section.items():
        section_start = cursor
        sentence_records = []
        for i, item in enumerate(items):
            info = manifest[item["id"]]
            src = ROOT / info["path"]
            override = prosody.get(item["id"], {})
            atempo = float(override.get("atempo", 1.0))
            pause_after = float(override.get("pause_after", args.sentence_gap))
            dur = float(info["duration_s"]) / atempo

            out_path = src
            if atempo != 1.0 or args.render_audio:
                out_path = TIMED_DIR / f"{item['id']}.wav"
                af = f"atempo={atempo}" if atempo != 1.0 else "anull"
                run(["ffmpeg", "-hide_banner", "-y", "-i", str(src),
                     "-af", af, "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le",
                     str(out_path)])
                dur = duration(out_path)
            timed_paths.append(out_path)

            sentence_records.append({
                "id": item["id"],
                "text": item["text"],
                "visual": item["visual"],
                "start": round(cursor, 3),
                "end": round(cursor + dur, 3),
                "duration": round(dur, 3),
                "atempo": atempo,
                "pause_after": pause_after,
            })
            cursor += dur
            if i < len(items) - 1:
                cursor += pause_after
        sections.append({
            "id": sid,
            "start": round(section_start, 3),
            "end": round(cursor, 3),
            "duration": round(cursor - section_start, 3),
            "sentences": sentence_records,
        })
        cursor += args.section_gap

    total = cursor - args.section_gap if sections else 0.0
    data = {
        "sentence_gap_s": args.sentence_gap,
        "section_gap_s": args.section_gap,
        "total_duration_s": round(total, 3),
        "sentence_count": sum(len(s["sentences"]) for s in sections),
        "sections": sections,
    }
    OUT_TIMING.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
    print(f"timing: {OUT_TIMING}")
    print(f"sections: {len(sections)}, sentences: {data['sentence_count']}, "
          f"total: {total:.1f}s = {total/60:.2f} min")

    if args.render_audio:
        section_file = S02 / "audio" / "sil_section.wav"
        write_silence(section_file, args.section_gap)
        sil_cache: dict[int, Path] = {}

        def silence_for(seconds: float) -> Path:
            key = int(round(seconds * 1000))
            if key not in sil_cache:
                path = S02 / "audio" / f"sil_{key:04d}.wav"
                write_silence(path, seconds)
                sil_cache[key] = path
            return sil_cache[key]

        concat_lines = []
        for si, section in enumerate(sections):
            for i, sent in enumerate(section["sentences"]):
                concat_lines.append(f"file '{(TIMED_DIR / (sent['id'] + '.wav')).resolve()}'")
                if i < len(section["sentences"]) - 1:
                    gap = silence_for(float(sent["pause_after"]))
                    concat_lines.append(f"file '{gap.resolve()}'")
            if si < len(sections) - 1:
                concat_lines.append(f"file '{section_file.resolve()}'")
        list_path = S02 / "audio" / "concat.txt"
        list_path.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")
        run(["ffmpeg", "-hide_banner", "-y", "-f", "concat", "-safe", "0",
             "-i", str(list_path), "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1",
             str(OUT_WAV)])
        print(f"narration: {OUT_WAV} ({duration(OUT_WAV):.1f}s)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

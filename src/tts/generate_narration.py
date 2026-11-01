#!/usr/bin/env python3
"""Generate Chinese narration with the local Qwen3-TTS CustomVoice model.

This wrapper deliberately keeps all environment-specific paths configurable.
It sets a writable numba cache before importing qwen_tts: the stock conda
environment otherwise fails to import librosa/numba when its site-packages
directory is not writable.

Examples
--------
Single take:
    python src/tts/generate_narration.py \
        --text-file chapters/s01/script/narration.txt \
        --out chapters/s01/audio/s01_full.wav

Segment batch (JSON list of {"id": "...", "text": "..."}):
    python src/tts/generate_narration.py \
        --segments-json chapters/s01/script/segments.json \
        --out-dir chapters/s01/audio/segments
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CACHE = ROOT / ".cache" / "numba"
DEFAULT_MODEL = Path("/home/lanshuye/Projects/QwenTTS/Qwen3-TTS-12Hz-0.6B-CustomVoice")
DEFAULT_INSTRUCT = "用沉稳、清晰、亲切的科普讲解语气，语速适中，句间停顿自然。"
# 0.6B CustomVoice silently drops `instruct`; only the 1.7B model honours it.
INSTRUCT_MODELS = {"1b7"}

# Must be set before importing qwen_tts, which imports librosa/numba.
DEFAULT_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("NUMBA_CACHE_DIR", str(DEFAULT_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(ROOT / ".cache" / "xdg"))

import torch  # noqa: E402
import soundfile as sf  # noqa: E402


def read_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"Text file is empty: {path}")
    return text


def load_segments(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError("segments JSON must be a non-empty list")
    seen = set()
    for item in data:
        if not isinstance(item, dict) or "id" not in item or "text" not in item:
            raise ValueError("each segment needs string fields 'id' and 'text'")
        if not str(item["id"]).strip() or not str(item["text"]).strip():
            raise ValueError("segment id/text must not be empty")
        if item["id"] in seen:
            raise ValueError(f"duplicate segment id: {item['id']}")
        seen.add(item["id"])
        for key in ("instruct", "speaker", "language"):
            if key in item and not isinstance(item[key], str):
                raise ValueError(f"{item['id']}: '{key}' must be a string")
    return data


def model_size(model_dir: Path) -> str:
    """Read tts_model_size from config.json ('0b6' or '1b7')."""
    try:
        cfg = json.loads((model_dir / "config.json").read_text(encoding="utf-8"))
        return str(cfg.get("tts_model_size", ""))
    except (OSError, json.JSONDecodeError):
        return ""


def resolve_device(requested: str) -> str:
    if requested == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    if requested == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but torch.cuda.is_available() is false")
    return requested


def build_model(model_dir: Path, device: str):
    from qwen_tts import Qwen3TTSModel

    dtype = torch.bfloat16 if device == "cuda" else torch.float32
    return Qwen3TTSModel.from_pretrained(
        str(model_dir),
        device_map=device,
        dtype=dtype,
        attn_implementation="sdpa",
    )


def synthesize(model, text: str, speaker: str, language: str, instruct: str) -> tuple:
    kwargs = dict(text=text, language=language, speaker=speaker)
    if instruct.strip():
        kwargs["instruct"] = instruct.strip()
    return model.generate_custom_voice(**kwargs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text-file", type=Path, help="UTF-8 text for one take")
    group.add_argument("--segments-json", type=Path, help="JSON list of narration segments")
    parser.add_argument("--out", type=Path, help="output WAV for a single take")
    parser.add_argument("--out-dir", type=Path, help="output directory for segment batch")
    parser.add_argument("--model-dir", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--speaker", default="serena")
    parser.add_argument("--language", default="Chinese")
    parser.add_argument("--instruct", default=DEFAULT_INSTRUCT)
    parser.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    parser.add_argument("--limit", type=int, default=0, help="only synthesize the first N segments")
    parser.add_argument("--seed", type=int, default=20261101)
    parser.add_argument("--keep-existing", action="store_true",
                        help="skip segments whose wav already exists")
    parser.add_argument("--dry-run", action="store_true", help="validate inputs and print the plan")
    args = parser.parse_args()

    if args.text_file and not args.out:
        parser.error("--text-file requires --out")
    if args.segments_json and not args.out_dir:
        parser.error("--segments-json requires --out-dir")

    if args.text_file:
        jobs = [{"id": args.text_file.stem, "text": read_text(args.text_file)}]
        out_dir = args.out.parent
    else:
        jobs = load_segments(args.segments_json)
        out_dir = args.out_dir

    if args.limit > 0:
        jobs = jobs[:args.limit]

    device = resolve_device(args.device)
    total_chars = sum(len(j["text"]) for j in jobs)
    size = model_size(args.model_dir)
    has_instruct = any((j.get("instruct") or "").strip() for j in jobs)
    print(f"device={device} speaker={args.speaker} jobs={len(jobs)} chars={total_chars}")
    print(f"model={args.model_dir} tts_model_size={size or 'unknown'}")
    print(f"numba_cache={os.environ.get('NUMBA_CACHE_DIR')}")
    if has_instruct and size and size not in INSTRUCT_MODELS:
        print("WARNING: this model ignores per-segment 'instruct'; use the 1.7B CustomVoice "
              "model if you need sentence-level tone control.", file=sys.stderr)
    if not args.model_dir.exists():
        print(f"ERROR: model directory not found: {args.model_dir}", file=sys.stderr)
        return 2

    if args.dry_run:
        for job in jobs:
            ins = (job.get("instruct") or args.instruct or "").strip()
            print(f"  {job['id']}: {job['text'][:60]}{'…' if len(job['text']) > 60 else ''}")
            if ins:
                print(f"      instruct: {ins}")
        print("dry run: no audio written")
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    model = build_model(args.model_dir, device)
    manifest = []
    for index, job in enumerate(jobs):
        target = out_dir / f"{job['id']}.wav" if args.segments_json else args.out
        target.parent.mkdir(parents=True, exist_ok=True)
        if args.keep_existing and target.exists():
            info = sf.info(str(target))
            manifest.append({
                "id": job["id"],
                "text": job["text"],
                "instruct": (job.get("instruct") or "").strip(),
                "path": str(target.relative_to(ROOT)) if target.is_relative_to(ROOT) else str(target),
                "sample_rate": info.samplerate,
                "duration_s": round(info.frames / info.samplerate, 3),
                "elapsed_s": 0.0,
            })
            print(f"  keep {target} ({info.frames / info.samplerate:.2f}s)")
            continue
        speaker = job.get("speaker") or args.speaker
        language = job.get("language") or args.language
        instruct = (job.get("instruct") if job.get("instruct") is not None else args.instruct) or ""
        torch.manual_seed(args.seed + index)
        started = time.time()
        wavs, sr = synthesize(model, job["text"], speaker, language, instruct)
        sf.write(str(target), wavs[0], sr)
        info = sf.info(str(target))
        elapsed = time.time() - started
        manifest.append(
            {
                "id": job["id"],
                "text": job["text"],
                "instruct": instruct.strip(),
                "path": str(target.relative_to(ROOT)) if target.is_relative_to(ROOT) else str(target),
                "sample_rate": info.samplerate,
                "duration_s": round(info.frames / info.samplerate, 3),
                "elapsed_s": round(elapsed, 2),
            }
        )
        print(f"  wrote {target} ({info.frames / info.samplerate:.2f}s, {elapsed:.1f}s compute)")

    if args.segments_json:
        manifest_path = out_dir / "manifest.json"
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

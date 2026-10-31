#!/usr/bin/env python3
"""Extract TTS-ready narration from chapters/s01/script.md.

Outputs
-------
- narration.txt        full narration, paragraphs only
- scene_segments.json  one item per storyboard scene (for timing)
- segments.json        sentence-level TTS jobs (for generate_narration.py)

Keeping these derived files generated avoids hand-copy drift between the
script, the timing plan, and the TTS batch.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "chapters" / "s01" / "script.md"
OUT_DIR = ROOT / "chapters" / "s01" / "script"


def split_sentences(paragraph: str) -> list[str]:
    # Keep terminal punctuation; split after Chinese sentence enders.
    parts = re.split(r"(?<=[。！？])", paragraph)
    return [p.strip() for p in parts if p.strip()]


def main() -> int:
    text = SCRIPT.read_text(encoding="utf-8")
    body = text.split("## 1. 旁白正文", 1)[1].split("\n## 2. ", 1)[0]
    sections: list[tuple[str, list[str]]] = []
    current_title: str | None = None
    current_lines: list[str] = []

    for raw in body.splitlines():
        line = raw.strip()
        if line.startswith("### "):
            if current_title is not None:
                sections.append((current_title, current_lines))
            current_title = line[4:].strip()
            current_lines = []
        elif line and current_title is not None:
            if line.startswith("（") and line.endswith("）"):
                continue
            current_lines.append(line)

    if current_title is not None:
        sections.append((current_title, current_lines))

    if not sections:
        raise SystemExit("No narration sections found")

    all_paragraphs: list[str] = []
    scene_segments = []
    tts_segments = []
    for scene_idx, (title, paragraphs) in enumerate(sections):
        if not paragraphs:
            continue
        all_paragraphs.append("\n\n".join(paragraphs))
        scene_id = f"s{scene_idx:02d}"
        scene_segments.append(
            {
                "id": scene_id,
                "title": title,
                "text": "\n\n".join(paragraphs),
            }
        )
        sentence_idx = 0
        for paragraph in paragraphs:
            for sentence in split_sentences(paragraph):
                sentence_idx += 1
                tts_segments.append(
                    {
                        "id": f"{scene_id}_{sentence_idx:02d}",
                        "scene": scene_id,
                        "text": sentence,
                    }
                )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "narration.txt").write_text("\n\n".join(all_paragraphs) + "\n", encoding="utf-8")
    (OUT_DIR / "scene_segments.json").write_text(
        json.dumps(scene_segments, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "segments.json").write_text(
        json.dumps(tts_segments, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    scene_chars = sum(len(s["text"].replace("\n", "")) for s in scene_segments)
    tts_chars = sum(len(s["text"]) for s in tts_segments)
    print(f"wrote {OUT_DIR / 'narration.txt'}")
    print(f"wrote {OUT_DIR / 'scene_segments.json'} ({len(scene_segments)} scenes)")
    print(f"wrote {OUT_DIR / 'segments.json'} ({len(tts_segments)} TTS jobs)")
    print(f"scene_chars={scene_chars} tts_chars={tts_chars}")
    for s in scene_segments:
        print(f"  {s['id']}: {s['title']} ({len(s['text'])} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

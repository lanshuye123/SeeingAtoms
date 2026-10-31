#!/usr/bin/env python3
"""Advisory checker for AI-ish narration patterns and L0 information leaks.

This is a writing aid, not a detector. A hit is a prompt to re-read the line,
not proof that the line is bad.

Usage:
    python3 scripts/check_copy.py chapters/s01/script/narration.txt
"""
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

AI_PATTERNS = {
    "list_transition": r"(?:首先|其次|最后)[，,、]",
    "numbered_list": r"第[一二三]，",
    "empty_transition": r"(?:值得注意的是|不难发现|综上所述|由此可见|众所周知|显而易见)",
    "host_voice": r"(?:让我们|你一定想不到|见证奇迹|接下来，我们)",
    "not_but": r"不是.{0,24}而是",
    "not_only": r"不仅.{0,24}而且",
    "big_word": r"(?:极其重要|深远影响|不可或缺|至关重要的)",
}

L0_FORBIDDEN = [
    "/home/", "manim", "Manim", "ffmpeg", "conda", "venv", ".py",
    "python", "终端", "命令行", "日志", "环境变量", "pip install", "uv ",
]

SENTENCE_SPLIT = re.compile(r"(?<=[。！？])")


def sentences(text: str) -> list[str]:
    out: list[str] = []
    for para in text.splitlines():
        para = para.strip()
        if not para:
            continue
        out.extend(s.strip() for s in SENTENCE_SPLIT.split(para) if s.strip())
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("text_file", type=Path)
    parser.add_argument("--strict", action="store_true", help="fail on AI-pattern hits too")
    args = parser.parse_args()

    text = args.text_file.read_text(encoding="utf-8")
    sents = sentences(text)
    chars = len("".join(text.split()))
    print(f"file: {args.text_file}")
    print(f"chars (no whitespace): {chars}; sentences: {len(sents)}")

    hits: list[tuple[str, str]] = []
    for name, pattern in AI_PATTERNS.items():
        for m in re.finditer(pattern, text):
            line = text.count("\n", 0, m.start()) + 1
            hits.append((name, f"line {line}: {m.group(0)}"))

    long_sents = [s for s in sents if len(s) > 45]
    starts = Counter(s[:2] for s in sents if len(s) >= 2)
    repeated = [(k, v) for k, v in starts.most_common() if v >= 3]

    print("\n-- AI-ish pattern (advisory) --")
    if hits:
        for name, detail in hits:
            print(f"  [{name}] {detail}")
    else:
        print("  none")

    print("\n-- long sentences (>45 chars) --")
    if long_sents:
        for s in long_sents:
            print(f"  {len(s)}: {s}")
    else:
        print("  none")

    print("\n-- repeated sentence starts (>=3) --")
    if repeated:
        for k, v in repeated:
            print(f"  {k!r}: {v}")
    else:
        print("  none")

    print("\n-- L0 information leak --")
    leaks = [s for s in L0_FORBIDDEN if s in text]
    if leaks:
        for s in leaks:
            print(f"  FORBIDDEN: {s!r}")
    else:
        print("  none")

    if leaks:
        return 1
    if args.strict and hits:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

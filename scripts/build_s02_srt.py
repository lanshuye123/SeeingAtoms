#!/usr/bin/env python3
"""Build a draft SRT and a timing QC report from S02's sentence-locked timing."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S02 = ROOT / "chapters" / "s02"
TIMING = S02 / "audio" / "timing.json"
AUDIO = S02 / "audio" / "s02_narration.wav"
OUT_SRT = S02 / "renders" / "s02_narration.srt"
OUT_REPORT = S02 / "renders" / "sync_report.md"


def ts(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def chunks(text: str, width: int = 22) -> list[str]:
    """Split a sentence into <=width-character subtitle chunks.

    Prefer punctuation boundaries; hard-split only when a single clause is
    longer than the width. Two-line subtitles are avoided so each entry stays
    readable at 1080p.
    """
    import re
    if len(text) <= width:
        return [text]
    clauses = [c for c in re.split(r"(?<=[。；！？，、])", text) if c]
    out: list[str] = []
    buf = ""
    for clause in clauses:
        if len(clause) > width:
            if buf:
                out.append(buf)
                buf = ""
            for i in range(0, len(clause), width):
                out.append(clause[i:i + width])
            continue
        if len(buf) + len(clause) <= width:
            buf += clause
        else:
            if buf:
                out.append(buf)
            buf = clause
    if buf:
        out.append(buf)
    return [c for c in out if c.strip()]


def srt_time(s: float, e: float) -> str:
    return f"{ts(s)} --> {ts(e)}"


def main() -> int:
    data = json.loads(TIMING.read_text(encoding="utf-8"))
    OUT_SRT.parent.mkdir(parents=True, exist_ok=True)
    lines, idx = [], 0
    rows = []
    for section in data["sections"]:
        for sent in section["sentences"]:
            parts = chunks(sent["text"])
            total = sum(len(p) for p in parts) or 1
            acc = 0.0
            for raw in parts:
                n = len(raw)
                start = sent["start"] + sent["duration"] * acc / total
                end = sent["start"] + sent["duration"] * (acc + n) / total
                part = raw.rstrip("，、；：")
                if part:
                    idx += 1
                    lines.append(str(idx))
                    lines.append(srt_time(start, end))
                    lines.append(part)
                    lines.append("")
                acc += n
            rows.append((sent["id"], section["id"], sent["start"], sent["end"],
                         sent["duration"], sent["text"]))
    OUT_SRT.write_text("\n".join(lines), encoding="utf-8")

    def dur(path: Path) -> float:
        return float(subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(path)], text=True).strip())

    audio_d = dur(AUDIO) if AUDIO.exists() else 0.0
    timing_d = float(data["total_duration_s"])
    max_overlap = 0.0
    prev_end = 0.0
    for _, _, start, end, _, _ in rows:
        max_overlap = max(max_overlap, prev_end - start)
        prev_end = end

    report = [
        "# S02 时间轴与字幕自检",
        "",
        f"- 句数：{len(rows)}",
        f"- `timing.json` 总长：{timing_d:.2f} s（{timing_d/60:.2f} min）",
        f"- `s02_narration.wav` 实测：{audio_d:.2f} s",
        f"- 差值：{abs(audio_d - timing_d):.3f} s（目标 ≤ 0.05 s）",
        f"- 句间最大重叠：{max_overlap:.3f} s（目标 ≤ 0）",
        "",
        "## 分场",
        "",
        "| 场 | 起 | 止 | 时长 | 句数 |",
        "|---|---|---|---|---|",
    ]
    for section in data["sections"]:
        report.append(
            f"| {section['id']} | {section['start']:.2f} | {section['end']:.2f} | "
            f"{section['duration']:.2f} | {len(section['sentences'])} |")
    report += [
        "",
        "## 句级锚点（前 12 条）",
        "",
        "| 句号 | 起 | 止 | 时长 | 文本 |",
        "|---|---|---|---|---|",
    ]
    for sid, sec, start, end, d, text in rows[:12]:
        report.append(f"| {sid} | {start:.2f} | {end:.2f} | {d:.2f} | {text[:38]} |")
    report += [
        "",
        "## 说明",
        "",
        "- 字幕由 `timing.json` 生成，与音频共用同一组句间停顿；正式制作前需人工校对断句。",
        "- 句级同步的最终验证以 `renders/sync_demo.mp4` 为准；本报告只检查时间轴自洽。",
        "",
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(f"wrote {OUT_SRT} ({idx} entries)")
    print(f"wrote {OUT_REPORT}")
    print(f"timing={timing_d:.2f}s audio={audio_d:.2f}s diff={abs(audio_d-timing_d):.3f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

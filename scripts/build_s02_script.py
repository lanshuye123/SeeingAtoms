#!/usr/bin/env python3
"""Build S02 narration artifacts from the sentence table.

Input : chapters/s02/script/narration.tsv
Output: chapters/s02/script/sentences.json
        chapters/s02/script/narration.txt
        chapters/s02/script.md

The TSV is the single source of truth: text, per-sentence TTS instruction and
the visual anchor used by the storyboard and the sentence-locked timeline.
"""
from __future__ import annotations

import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S02 = ROOT / "chapters" / "s02"
TSV = S02 / "script" / "narration.tsv"

SECTION_TITLES = OrderedDict([
    ("S00", "铜网、绿屏，和一句“这是原子列”"),
    ("S01", "为什么非得磨到几十纳米"),
    ("S02", "波长够短，为什么还是看不清"),
    ("S03", "一台机器，两种看法"),
    ("S04", "亮点不是原子的影子"),
    ("S05", "拿一张算出来的图，当尺子"),
    ("S06", "电子束会改样品，也会骗人"),
    ("S07", "下一期：两种真实打架"),
])

SECTION_NOTES = {
    "S00": "从可拍摄的物件和操作进入，先给现象，再提问。",
    "S01": "用电子与物质作用强解释“薄”的必然性；制样步骤给具体动作，不给清单。",
    "S02": "把 S01 的“波长不够”换成“透镜不够好”，这是本期最大的认知转折。",
    "S03": "从分辨率转到信息类型：成像与衍射，以及电子衍射和 S01 倒易空间的接续。",
    "S04": "解释高分辨像的相位衬度与投影，纠正“亮点=原子照片”。",
    "S05": "用模拟像做对照尺，讲清读图的前提和边界。",
    "S06": "辐照损伤与取样偏差；与 XRD 的平均结果对照，落到“两种真实”。",
    "S07": "用一个具体冲突把下一期钩子做实，不再空泛提问。",
}


def char_count(text: str) -> int:
    """Count Chinese characters and ASCII words roughly as spoken units."""
    han = len(re.findall(r"[\u4e00-\u9fff]", text))
    words = len(re.findall(r"[A-Za-z]+", text))
    digits = len(re.findall(r"\d+(?:\.\d+)?", text))
    return han + words + digits


def load_rows() -> list[dict]:
    rows = []
    seen = set()
    for lineno, line in enumerate(TSV.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        if lineno == 1 and line.startswith("id\t"):
            continue
        parts = line.split("\t")
        if len(parts) != 5:
            raise ValueError(f"line {lineno}: expected 5 columns, got {len(parts)}")
        sid, section, text, instruct, visual = [p.strip() for p in parts]
        if sid in seen:
            raise ValueError(f"duplicate id: {sid}")
        seen.add(sid)
        if not re.fullmatch(r"S\d{2}_\d{2}", sid):
            raise ValueError(f"bad id: {sid}")
        if not text:
            raise ValueError(f"{sid}: empty text")
        rows.append({"id": sid, "section": section, "text": text,
                     "instruct": instruct, "visual": visual})
    if not rows:
        raise ValueError("no rows")
    return rows


def main() -> int:
    rows = load_rows()
    total_chars = sum(char_count(r["text"]) for r in rows)
    per_section = OrderedDict()
    for r in rows:
        per_section.setdefault(r["section"], []).append(r)

    out = []
    for r in rows:
        out.append({
            "id": r["id"],
            "section": r["section"],
            "text": r["text"],
            "instruct": r["instruct"],
            "visual": r["visual"],
            "chars": char_count(r["text"]),
        })
    (S02 / "script" / "sentences.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (S02 / "script" / "narration.txt").write_text(
        "\n".join(r["text"] for r in rows) + "\n", encoding="utf-8")

    lines = []
    lines.append("# S02 旁白稿（v0.2 · 待审定）")
    lines.append("")
    lines.append("> 系列：看见原子")
    lines.append("> 第二期：电子显微镜，如何把原子“拍”出来？")
    lines.append(f"> 旁白字数：约 {total_chars} 字（汉字 + 英文词 + 数字，按 220–235 字/分钟估算约 "
                 f"{total_chars/235:.1f}–{total_chars/220:.1f} 分钟）")
    lines.append("> 版本：v0.2，供操作员审定文案、语气与素材方向；尚未进入正式制作。")
    lines.append("> 逐句语气标注与画面锚点见 `script/sentences.json`；本稿由 `script/narration.tsv` 生成。")
    lines.append("")
    lines.append("## 1. 本期一句话")
    lines.append("")
    lines.append("电子波长足够短，短到能看见原子；真正挡住视线的是磁透镜的像差、样品厚度和电子束本身的破坏性。"
                 "高分辨像不是原子照片，而是相位衬度加投影之后、需要模拟才能读懂的一张图。")
    lines.append("")
    lines.append("## 2. 逻辑链（针对“逻辑跳跃”的修改）")
    lines.append("")
    lines.append("本期每一节只回答上一节留下的问题，转折处都给一句“为什么现在说这个”：")
    lines.append("")
    chain = [
        ("看到原子列", "屏幕上的线从哪来？", "先看电子在样品里经历了什么"),
        ("电子穿不透", "为什么样品必须薄到几十纳米？", "厚度决定了能不能出来、出来的是不是单次散射"),
        ("样品薄了", "波长这么短，为什么实际分辨率只有 1.9 Å？", "瓶颈从波长换成透镜像差"),
        ("分辨率够了", "看到的是像，还是衍射？", "中间镜焦面决定信息类型"),
        ("知道是像", "像上的亮点是不是原子？", "相位衬度 + 投影，需要模拟对照"),
        ("会读图了", "这张图能代表整块材料吗？", "辐照损伤与取样偏差"),
        ("知道边界了", "那和 XRD 是什么关系？", "平均与局部，引出下一期的冲突"),
    ]
    lines.append("| 观众刚接受的 | 自然产生的问题 | 下一节怎么接 |")
    lines.append("|---|---|---|")
    for a, b, c in chain:
        lines.append(f"| {a} | {b} | {c} |")
    lines.append("")
    lines.append("## 3. 旁白正文")
    lines.append("")
    for section, items in per_section.items():
        lines.append(f"### {section} {SECTION_TITLES[section]}")
        lines.append("")
        lines.append(f"*{SECTION_NOTES[section]}*")
        lines.append("")
        for r in items:
            lines.append(r["text"])
            lines.append("")
    lines.append("## 4. 逐句语气控制（Qwen3-TTS 1.7B CustomVoice）")
    lines.append("")
    lines.append("0.6B CustomVoice 会忽略 `instruct`；本期改用 1.7B CustomVoice，逐句传 `instruct`，"
                 "并在合成后按句微调停顿与语速。下表是给 TTS 的原始指令，不是最终听感。")
    lines.append("")
    lines.append("| 句号 | 旁白 | 语气指令 | 画面锚点 |")
    lines.append("|---|---|---|---|")
    for r in rows:
        lines.append(f"| {r['id']} | {r['text']} | {r['instruct']} | {r['visual']} |")
    lines.append("")
    lines.append("## 5. 与第一期的衔接")
    lines.append("")
    lines.append("- 第一期结尾说“电子束波长更短、跟物质作用更狠、能被磁透镜聚成像”，本期逐条兑现，不重复 X 射线衍射的推导。")
    lines.append("- 第一期用“尺子”讲波长；本期把“尺子够细”作为前提，把矛盾移到“透镜不够好”，避免同一解释用两遍。")
    lines.append("- 倒易空间只在 S03 用一次，直接接第一期的“三维倒易点阵的一维投影”，不重新讲布拉格公式。")
    lines.append("")
    lines.append("## 6. 反“AI 味”改动（相对初稿）")
    lines.append("")
    lines.append("- 删掉“首先/其次/最后”“第一/第二/第三”的清单推进；制样步骤用动作串起来，不编号。")
    lines.append("- 删掉段尾“所以这告诉我们……”式总结；S02 结尾只留“两件事”，S06 结尾只留“一个给平均，一个给局部”。")
    lines.append("- 把“不是……而是……”改成更松的口语：能拆就拆，能省就省；全稿只保留少量必要对照。")
    lines.append("- 加入可核实的现场细节：三毫米铜网、一毫米切片、十几微米、一微米、离子束穿孔、ZnS:Cu 绿光。")
    lines.append("- 允许毛边：短句、停顿、半句话；不把每个概念都解释干净，留给画面。")
    lines.append("- 不编造个人经历；“科学家说”“一个常被提到的例子”都是可核实的转述。")
    lines.append("")
    lines.append("## 7. 待操作员确认")
    lines.append("")
    lines.append("1. 标题是否用《电子显微镜，如何把原子“拍”出来？》；“拍”字是否加引号。")
    lines.append("2. 旁白长度约 8.5–9 分钟（不含片尾）是否合适；若要压到 8 分钟，优先删 S05 的读图细节。")
    lines.append("3. 是否接受“高分辨像不是原子照片”这一核心判断；这会占用约 2 分钟，但能避免最常见的科学误读。")
    lines.append("4. 真实显微图：是用 CC0/PD 实拍图，还是用自算模拟图 + 明确标注；两者在素材集里都已准备候选。")
    lines.append("5. 片尾是否出现具体姓名/单位；沿用第一期待确认项。")
    lines.append("")
    lines.append("## 8. 科学事实核对")
    lines.append("")
    lines.append("逐条见 `chapters/s02/fact_check.md`。本稿涉及的核心数字：")
    lines.append("")
    lines.append("- 200 kV 电子波长 0.0250793 Å（约 0.025 Å）。")
    lines.append("- Cu Kα X 射线 1.5406 Å，约为电子波长的 61 倍。")
    lines.append("- 200 kV 理论分辨率 0.05 Å；常规电镜实际约 1.9 Å；球差校正后约 1 Å，好的可到 0.5 Å。")
    lines.append("- 电子衍射样品 50–100 nm；高分辨像 <10 nm，理想 <3 nm；>150 nm 非弹性弥散散射明显。")
    lines.append("- 电子散射强度约为 X 射线的数十万倍；电子衍射 1–2 s，X 射线数十分钟。")
    lines.append("- 电子衍射角约 1°，X 射线约几十度。")
    lines.append("- 荧光屏 ZnS:Cu 发 550 nm 绿光。")
    lines.append("- 钛酸锶 a = 3.905 Å；模拟像按 [001] 带轴计算，标注“模拟计算，非实测”。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"统计：{len(rows)} 句，{total_chars} 字；按 220–235 字/分钟约 "
                 f"{total_chars/235:.1f}–{total_chars/220:.1f} 分钟（不含停顿与片尾）。")
    lines.append("")

    (S02 / "script.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"sentences: {len(rows)}, chars: {total_chars}, "
          f"est: {total_chars/235:.1f}-{total_chars/220:.1f} min")
    for section, items in per_section.items():
        print(f"  {section}: {len(items)} sentences, "
              f"{sum(char_count(r['text']) for r in items)} chars")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

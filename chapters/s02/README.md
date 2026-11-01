# S02 制作页

> 系列：看见原子
> 第二期：电子显微镜，如何把原子“拍”出来？
> 状态：**制作完成，待操作员验收。**
> 成片：[`renders/s02_final.mp4`](renders/s02_final.mp4)（10:21，1920×1080 / 30 fps）
> 封面：[`renders/cover.png`](renders/cover.png)（16:9，中心 4:3 安全区）
> 质检：[`renders/qc_report.md`](renders/qc_report.md)
> 旁白：90 句，约 9 分 13 秒（`audio/s02_narration_norm.wav`）；配乐床轨 99 秒循环。

## 1. 本期内容

一片三毫米铜网，上面挂着一块磨到几十纳米厚的样品。电子束打上去，荧光屏发绿光；图像从糊到清，出现一排排亮点。科学家说，那是原子列。

可电子没有眼睛。波长只有 0.025 Å，比 X 射线短六十倍，理论上早该看见原子；实际分辨率却只有 1.9 Å，瓶颈是磁透镜的球差。球差校正把分辨率推到 1 Å 上下。再往下，问题变成：屏幕上的亮点，是不是原子？

不是。高分辨像记录的是相位衬度，再沿厚度方向压成投影；一个亮点是一整列原子。要读懂它，得知道电压、球差、离焦、厚度，还要拿模拟图对照。电子束还会把样品改掉，薄区也未必代表整块材料。于是，电镜给局部，X 射线给平均——下一期，两种真实开始打架。

## 2. 请先看这几样

| 顺序 | 看什么 | 文件 | 重点 |
|---|---|---|---|
| 0 | **成片** | [`renders/s02_final.mp4`](renders/s02_final.mp4) | 整体节奏、音画同步、字幕、片尾、封面 |
| 1 | 旁白稿 | [`script.md`](script.md) | 逻辑是否还跳；哪些句子像“模型在解释” |
| 2 | 动效样片 | [`renders/sync_demo.mp4`](renders/sync_demo.mp4) | 运镜/光效是否够“华丽”、是否过火；动作是否落在句子开口处 |
| 3 | 逐句语气 | [`audio/tts_samples_reel.wav`](audio/tts_samples_reel.wav)、[`audio/tts_samples/tts_samples.md`](audio/tts_samples/tts_samples.md) | 哪一组语气最接近想要的效果 |
| 4 | 整稿旁白 | [`audio/s02_narration_norm.wav`](audio/s02_narration_norm.wav) | 9:13 是否太长；语速/停顿是否自然 |
| 5 | 配乐 | [`assets/music/s02_theme.wav`](assets/music/s02_theme.wav) | 是否太“new age”/太薄；要不要换配器 |
| 6 | AI 插图 | [`assets/illustrations/contact_sheet_graded.png`](assets/illustrations/contact_sheet_graded.png) | 风格是否能接受；哪几张要弃用/重做 |
| 7 | 模拟 HRTEM | [`assets/sim/sim_srtio3_001_sr_under.png`](assets/sim/sim_srtio3_001_sr_under.png) | 是否接受“模拟计算，非实测”的用法 |
| 8 | 分镜 | [`storyboard.md`](storyboard.md) | 镜头节奏、信息密度、字幕位置 |

## 3. 文件索引

| 文件/目录 | 内容 |
|---|---|
| [`script.md`](script.md) | 旁白正文、逻辑链、逐句语气表、反 AI 味改动、待确认 |
| [`script/narration.tsv`](script/narration.tsv) | 单一事实源：句号、文本、语气指令、画面锚点 |
| [`script/sentences.json`](script/sentences.json) | 供 TTS/时间轴/分镜使用的结构化句子表 |
| [`script/prosody.json`](script/prosody.json) | 逐句 `atempo` 与句后停顿 |
| [`storyboard.md`](storyboard.md) | 分镜、声音设计、句级同步方案、素材映射 |
| [`fact_check.md`](fact_check.md) | 逐条科学事实核对与“避免说法” |
| [`plan.md`](plan.md) | 六条反馈的处理、制作阶段、风险、待确认 |
| [`audio/s02_narration_norm.wav`](audio/s02_narration_norm.wav) | 整稿旁白，48 kHz 单声道，9:13 |
| [`audio/timing.json`](audio/timing.json) | 句级/场景级时间轴（音画同步的唯一依据） |
| [`audio/tts_samples/`](audio/tts_samples/) | 15 条同句不同语气的 A/B/C 样音 |
| [`audio/tts_samples_reel.wav`](audio/tts_samples_reel.wav) | 样音连播（约 101 s） |
| [`assets/sim/`](assets/sim/) | SrTiO₃ [001] 模拟高分辨像 3 张 + 参数 JSON |
| [`assets/cc0/`](assets/cc0/) | CDC 1965 TEM、NIST 石墨烯芯片、NIST 月尘 SEM + 许可证 |
| [`assets/illustrations/`](assets/illustrations/) | 6 张 AI 氛围插图（原图 + 调色版 + prompts） |
| [`assets/music/`](assets/music/) | 原创 MIDI、LMMS 工程、渲染 WAV、波形/频谱 |
| [`renders/sync_demo.mp4`](renders/sync_demo.mp4) | 41 秒句级同步小样（720p，含旁白，仅测试） |
| [`renders/s02_final.mp4`](renders/s02_final.mp4) | 成片，10:21，1920×1080 / 30 fps / H.264 + AAC |
| [`renders/cover.png`](renders/cover.png) | 16:9 封面；核心内容在居中 4:3 安全区 |
| [`renders/cover_4x3_preview.png`](renders/cover_4x3_preview.png) | 封面中心 4:3 裁切检查图 |
| [`renders/s02_narration.srt`](renders/s02_narration.srt) | 字幕，157 条，单行 ≤22 字 |
| [`renders/s02_final.ass`](renders/s02_final.ass) | 1080p 烧录用样式字幕 |
| [`renders/qc_report.md`](renders/qc_report.md) | 交付前自检报告 |
| [`renders/sync_report.md`](renders/sync_report.md) | 时间轴自洽检查 + 小样对照表 |
| [`manim/README.md`](manim/README.md) | 3b1b 参考、S00 动效手法、边界与缓存注意 |

## 4. 六条反馈，分别落在哪

| 反馈 | 处理 | 证据 |
|---|---|---|
| 用其他生图模型做插图 | 本地 SD1.5，6 张氛围图 + 统一调色 | `assets/illustrations/`、`prompts.json` |
| 引入 CC0/类似 CC 图像 | 3 张 PD/CC0 实拍，逐张记录 | `assets/cc0/LICENSES.md` |
| MIDI 自己做音乐 | 原创 28 小节，LMMS + SF2 Player | `assets/music/s02_theme.mmp` |
| 进一步去 AI 味 | 90 句口语稿、句长不均、具体操作细节；视频不用模板科技感 | `script.md`、`make copy-check` |
| QwenTTS 逐句微操 | 换 1.7B CustomVoice，逐句 `instruct`；0.6B 会忽略 instruct | `audio/tts_samples/`、`src/tts/generate_narration.py` |
| 音画对不上 | 句级时间轴 + `TimelineScene.cue()`；误差目标 ≤0.15 s | `audio/timing.json`、`manim/sync_demo.py` |
| 逻辑跳跃 | 每节只回答上一节留下的问题；转折句显式写出 | `script.md` §2、`storyboard.md` |

## 5. 复现命令

```bash
cd "/home/lanshuye/文档/科普视频"
source scripts/env.sh

# 文案 → 结构化句子
python3 scripts/build_s02_script.py

# 逐句 TTS（1.7B；已生成，可 --keep-existing 只补改动句）
NUMBA_CACHE_DIR="$PWD/.cache/numba" \
  /home/lanshuye/miniconda3/envs/qwen3-tts/bin/python \
  src/tts/generate_narration.py \
  --segments-json chapters/s02/script/sentences.json \
  --out-dir chapters/s02/audio/sentences \
  --model-dir /home/lanshuye/Projects/QwenTTS/Qwen3-TTS-12Hz-1.7B-CustomVoice \
  --device cuda --keep-existing

# 句级时间轴 + 整稿旁白
.venv/bin/python scripts/build_s02_timeline.py --render-audio

# 模拟 HRTEM
.venv/bin/python scripts/build_s02_sim_tem.py

# AI 插图（需 GPU；与 TTS 分时跑）
HF_ENDPOINT=https://hf-mirror.com \
  /home/lanshuye/miniconda3/envs/qwen3-tts/bin/python \
  scripts/build_s02_illustrations.py
.venv/bin/python scripts/grade_s02_illustrations.py

# 原创 MIDI + LMMS 渲染
.venv/bin/python scripts/build_s02_music.py --render

# 同步小样
.venv/bin/manim -qm --fps 30 --media_dir media \
  chapters/s02/manim/sync_demo.py S02SyncDemo

# 成片：混音 + ASS + 拼接/烧字幕
.venv/bin/python scripts/build_s02_mix.py
.venv/bin/python scripts/build_s02_ass.py
.venv/bin/python scripts/build_s02_video.py

# 封面
.venv/bin/manim -qh --fps 30 -s --media_dir media \
  chapters/s02/manim/cover.py S02Cover
ffmpeg -y -i media/images/cover/S02Cover_ManimCE_v0.19.0.png \
  -vf "crop=1440:1080:240:0" chapters/s02/renders/cover_4x3_preview.png
```

## 6. 待操作员确认

1. **成片**：整体节奏、音画同步、字幕断句、片尾与封面；是否还有需要重做的镜头。
2. **语气**：样音里哪组最接近；整稿还有没有“播音腔”。
3. **素材**：AI 氛围图是否接受；CC0/PD 三张图是否合适；是否必须用真实 HRTEM 实拍。
4. **配乐**：风格/配器是否合适；是否要更“实验室”、更少旋律。
5. **同步**：小样的句级同步是否达到要求；全片是否按此方案制作。
6. **片尾**：是否出现具体姓名/单位；是否沿用 S01 滚动样式。

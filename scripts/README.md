# 脚本与复现命令

> 所有命令默认在项目根目录执行：
> `cd "/home/lanshuye/文档/科普视频"`
> 渲染/生成前先 `source scripts/env.sh`：它会设置 TeX Live PATH 和项目内缓存目录。

## 1. 首次准备

```bash
source scripts/env.sh

uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python manim==0.19.0 gemmi==0.7.5
mkdir -p .cache/uv .cache/xdg .cache/mpl .cache/numba
```

说明：
- `UV_CACHE_DIR` 必须在项目内，默认 `~/.cache/uv` 在当前环境只读。
- 首次安装 Manim 时如遇 `ccache` 只读错误，设置 `CCACHE_DISABLE=1`。
- 字体已放入 `assets/fonts/`，无需联网下载。

## 1.1 字体二进制（默认不入库）

```bash
make fonts
# 或
bash scripts/fetch_fonts.sh
```

从本机字体目录复制思源黑体/宋体、霞鹜文楷，并校验 SHA-256。字体二进制不入 Git；许可证文本在 `assets/fonts/`。

## 2. 环境检查

```bash
bash scripts/check_env.sh
cat logs/environment_check.txt
```

检查内容：ffmpeg/ffprobe、libx264/aac/loudnorm/subtitles、Manim、XeLaTeX/dvisvgm、字体与许可证、TTS 环境与模型、课程笔记、GPU 状态。

预期：`RESULT: PASS`，0 失败、0 警告（2026-10-31 实测）。

## 3. Manim 冒烟测试

```bash
source scripts/env.sh

.venv/bin/manim -qh --fps 30 -s --media_dir media \
  src/render/manim_smoke_test.py CJKSmokeTest
```

输出：

```text
media/images/manim_smoke_test/CJKSmokeTest_ManimCE_v0.19.0.png
```

检查：中文无缺字、`×` 正常、1920×1080、标题层级清楚。

## 3.1 XeLaTeX 公式冒烟

```bash
source scripts/env.sh
.venv/bin/manim -qh --fps 30 -s --media_dir media \
  src/render/tex_smoke_test.py TeXSmokeTest
```

输出：

```text
media/images/tex_smoke_test/TeXSmokeTest_ManimCE_v0.19.0.png
```

检查：`2d sinθ = nλ` 与中文 `晶面间距` 无缺字、无乱码。

## 3.2 文案自查（反 AI 味 + 信息泄漏）

```bash
make copy-check
```

检查：清单腔、对称句、空泛转折、过长句、重复句首、L0 禁用词。  
它是**提示工具**，不是检测器；命中后人工判断，不要机械改写。

## 4. TTS 检查

只检查参数、不加载模型：

```bash
/home/lanshuye/miniconda3/envs/qwen3-tts/bin/python \
  src/tts/generate_narration.py \
  --segments-json chapters/s01/script/segments.json \
  --out-dir chapters/s01/audio/segments \
  --device auto --dry-run
```

实际生成单段：

```bash
/home/lanshuye/miniconda3/envs/qwen3-tts/bin/python \
  src/tts/generate_narration.py \
  --text-file chapters/s01/script/narration.txt \
  --out chapters/s01/audio/s01_full.wav \
  --device auto
```

分段批量（阶段三使用）：

```bash
/home/lanshuye/miniconda3/envs/qwen3-tts/bin/python \
  src/tts/generate_narration.py \
  --segments-json chapters/s01/script/segments.json \
  --out-dir chapters/s01/audio/segments \
  --device auto
```

说明：
- 当前 CUDA 可用（RTX 3060 Laptop，6 GB），4.32 秒音频约 3.9 秒计算。
- 6 GB 显存下不要与 Manim 渲染同时跑；OOM 时改 `--device cpu`（约 5–6 倍实时）。
- `NUMBA_CACHE_DIR` 已由脚本自动设置；不要在导入 `qwen_tts` 后再设置。
- “X 射线”已试听确认读“埃克斯”，不需要改写。

## 5. 渲染与合成（已执行）

> 场景文件已存在；以下命令可复现成片。公式场景使用 `S01_TEX_TEMPLATE`。

参考谱线：

```bash
make patterns
```

音频/字幕：

```bash
make audio
make srt
```

封面（16:9，核心内容在居中 4:3）：

```bash
make cover
```

全场景 + 片尾 + 合成：

```bash
make scenes
make credits
make concat
make final
```

单场景预览（先加载 TeX 路径）：

```bash
source scripts/env.sh
.venv/bin/manim -ql --fps 30 --media_dir media \
  chapters/s01/manim/scene_01.py S01_01_Scale
```

单场景终稿：

```bash
source scripts/env.sh
.venv/bin/manim -qh --fps 30 --media_dir media \
  chapters/s01/manim/scene_01.py S01_01_Scale
```

拼接 silent segments：

```bash
printf "file '%s'\n" chapters/s01/renders/segments/*.mp4 > chapters/s01/renders/concat.txt
ffmpeg -hide_banner -y -f concat -safe 0 -i chapters/s01/renders/concat.txt \
  -c copy chapters/s01/renders/s01_silent.mp4
```

响度测量（第一遍）：

```bash
ffmpeg -hide_banner -i chapters/s01/audio/s01_mix.wav \
  -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null -
```

按测量值做第二遍标准化，再与静音视频合成。字幕烧录与最终转码命令见 `docs/technical_route.md` 第 4.3 节。

## 6. 质检

```bash
# 流信息
ffprobe -v error -show_entries \
  format=duration,size,bit_rate:stream=codec_name,width,height,r_frame_rate,sample_rate,channels \
  -of json chapters/s01/renders/s01_final.mp4

# 抽帧
mkdir -p chapters/s01/renders/qc
ffmpeg -hide_banner -y -i chapters/s01/renders/s01_final.mp4 \
  -vf "fps=1/30,scale=640:-1" chapters/s01/renders/qc/frame_%03d.jpg

# 字幕时间轴检查
ffmpeg -hide_banner -i chapters/s01/renders/s01_final.srt -f null -
```

人工检查：
- 画面无路径、命令、环境名、终端、代码、日志、工具水印。
- 字幕无错别字，术语统一，断句自然，音画同步。
- 配乐不压过旁白；整体响度约 −16 LUFS。
- 片尾署名简洁，许可证信息在文档中。

## 7. 常见问题

### `Could not acquire lock` / `Read-only file system`（uv）

把 `UV_CACHE_DIR` 指到项目内：

```bash
export UV_CACHE_DIR="$PWD/.cache/uv"
```

### `ccache: error: Read-only file system`（pycairo）

```bash
export CCACHE_DISABLE=1
```

并优先使用 Python 3.11。

### `cannot cache function '__o_fold'`（numba/librosa）

```bash
export NUMBA_CACHE_DIR="$PWD/.cache/numba"
```

必须在导入 `qwen_tts` 之前设置；`src/tts/generate_narration.py` 已处理。

### `manim: command not found`

使用项目内二进制：

```bash
.venv/bin/manim --version
```

### 字幕中文变成方框

确认 `fontsdir=assets/fonts`，且 `FontName` 与字体族名一致：
- `Source Han Sans CN`
- `Source Han Serif CN`
- `LXGW WenKai`

## 8. S02 工作流（2026-11-01）

### 8.1 文案 → 句子表

```bash
python3 scripts/build_s02_script.py
```

输入 `chapters/s02/script/narration.tsv`（句号/文本/语气指令/画面锚点），输出：

- `chapters/s02/script/sentences.json`
- `chapters/s02/script/narration.txt`
- `chapters/s02/script.md`

### 8.2 逐句 TTS（1.7B CustomVoice）

```bash
source scripts/env.sh
NUMBA_CACHE_DIR="$PWD/.cache/numba" \
  /home/lanshuye/miniconda3/envs/qwen3-tts/bin/python \
  src/tts/generate_narration.py \
  --segments-json chapters/s02/script/sentences.json \
  --out-dir chapters/s02/audio/sentences \
  --model-dir /home/lanshuye/Projects/QwenTTS/Qwen3-TTS-12Hz-1.7B-CustomVoice \
  --device cuda --keep-existing
```

- `--keep-existing` 只补缺失/删除的句，适合改一两句后重录。
- 0.6B CustomVoice 会忽略 `instruct`；要逐句语气必须用 1.7B。
- 6 GB 显存峰值约 4.4 GB；不要与 SD/Manim 同时跑。

### 8.3 句级时间轴 + 整稿旁白

```bash
.venv/bin/python scripts/build_s02_timeline.py --render-audio
```

输出 `chapters/s02/audio/timing.json` 与 `s02_narration.wav`；两者总长必须一致。

### 8.4 模拟 HRTEM

```bash
.venv/bin/python scripts/build_s02_sim_tem.py
```

输出 `chapters/s02/assets/sim/*.png` 与参数 JSON；画面标“模拟计算 · 非实测”。

### 8.5 AI 氛围插图

```bash
HF_ENDPOINT=https://hf-mirror.com \
  /home/lanshuye/miniconda3/envs/qwen3-tts/bin/python \
  scripts/build_s02_illustrations.py
.venv/bin/python scripts/grade_s02_illustrations.py
```

依赖：`diffusers==0.31.0`、`transformers==4.57.3`、`Pillow==10.4.0`（Manim 的 `ImageMobject` 在 Pillow 13 下报 `Invalid mode for data type`，S02 已回退到 10.4.0）。

### 8.6 原创 MIDI 配乐

```bash
.venv/bin/python scripts/build_s02_music.py --render
```

输出 `chapters/s02/assets/music/` 下的 `.mid`、`.mmp`、`.wav`。无界面 LMMS 渲染依赖 `QT_QPA_PLATFORM=offscreen`。

### 8.7 字幕/同步报告/小样

```bash
.venv/bin/python scripts/build_s02_srt.py
.venv/bin/manim -qm --fps 30 --media_dir media \
  chapters/s02/manim/sync_demo.py S02SyncDemo
```

- `renders/s02_narration.srt`：草稿字幕，需人工校对断句。
- `renders/sync_report.md`：时间轴自洽 + 小样对照。
- `renders/sync_demo.mp4`：S00 的 7 句、约 41 秒，句级同步测试。

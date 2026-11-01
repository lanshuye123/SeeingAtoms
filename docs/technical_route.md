# 技术路线与环境记录

> 状态：阶段一实测记录 + S01 制作完成后的技术记录。
> 更新日期：2026-10-31（CUDA 与 TeX Live 已重新实测）
> 所有命令均在项目根目录 `/home/lanshuye/文档/科普视频` 下执行；路径含中文与空格，命令中一律加引号。
> 相关：[反 AI 味工作法](writing_guide.md)、[三级信息架构](information_architecture.md)。

## 1. 当前环境实测

| 项目 | 结果 | 记录 |
|---|---|---|
| 操作系统 | Linux（KDE Wayland） | 工作区位于 `/home/lanshuye/文档/科普视频` |
| `ffmpeg` | 可用，版本 9.0.2 | 含 `libx264`、`aac`、`loudnorm`、`subtitles`/`libass` |
| `ffprobe` | 可用 | 用于时长、流信息、响度检查 |
| `uv` | 可用，版本 0.13.6 | 缓存默认目录只读，需设置 `UV_CACHE_DIR` 到工作区 |
| 系统 Python | 3.14.8 | 不作为 Manim 运行环境 |
| 项目 Manim 环境 | `.venv`，Python 3.11.15，Manim 0.19.0 | 已成功渲染 1920×1080 中文测试帧 |
| LaTeX / `dvisvgm` | 可用 | TeX Live 2025：`/home/lanshuye/Apps/texlive/2025/bin/x86_64-linux`；`xelatex`、`latex`、`dvisvgm` 均可用 |
| TTS conda 环境 | `/home/lanshuye/miniconda3/envs/qwen3-tts`，Python 3.12.13 | 环境存在 |
| TTS 模型 | `Qwen3-TTS-12Hz-0.6B-CustomVoice` | 路径见下；模型文件约 2.4 GB |
| GPU | **可用** | NVIDIA RTX 3060 Laptop，6144 MiB，驱动 615.78.08；`torch.cuda.is_available()` 为 True |
| TTS GPU 推理 | 可用 | 4.32 秒音频约 3.9 秒计算，接近实时；6 GB 显存足够 0.6B 模型 |
| CPU 回退 | 可用 | 6.4 秒音频约 37 秒计算；约 5–6 倍实时 |
| 字体 | 思源黑体/宋体、霞鹜文楷 | 已复制到 `assets/fonts/`，含 OFL 许可证 |
| 磁盘 | 约 76 GB 可用 | 渲染中间帧需及时清理 |

### 1.1 Manim 安装记录

第一次尝试用系统 Python 3.13 创建环境时，`pycairo` 需要从源码编译，`ccache` 默认缓存目录位于只读文件系统，导致编译失败。处理方式：

```bash
export UV_CACHE_DIR="$PWD/.cache/uv"
export CCACHE_DISABLE=1
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python manim==0.19.0
```

结果：Manim 0.19.0 安装成功，中文 `Text` 渲染正常。

### 1.2 TTS 环境问题与处理

原始 conda 环境在导入 `qwen_tts` 时，`librosa` 触发 `numba` 缓存定位错误：

```text
RuntimeError: cannot cache function '__o_fold': no locator available
```

原因是 `numba` 默认缓存位置不可写/不可定位。未修改模型代码，处理方式是在导入前设置工作区内缓存目录：

```bash
export NUMBA_CACHE_DIR="$PWD/.cache/numba"
```

设置后 `qwen_tts` 可正常导入。GPU 已可用：`--device auto` 会选择 CUDA；CPU 仍保留为回退路径。环境会提示 `flash-attn` 未安装，当前使用 PyTorch SDPA，功能正常。

### 1.3 XeLaTeX 配置

- 运行前 `source scripts/env.sh`，把 `/home/lanshuye/Apps/texlive/2025/bin/x86_64-linux` 放到 `PATH`；`src/render/tex.py` 导入时也会补一次，避免遗漏。
- `src/render/tex.py` 定义 `S01_TEX_TEMPLATE`：`xelatex` + `.xdv` + `xeCJK`，中文字体为 `Source Han Sans CN`。
- 公式写法：

```python
from src.render.tex import S01_TEX_TEMPLATE
from manim import MathTex

formula = MathTex(r"2d\sin\theta = n\lambda", tex_template=S01_TEX_TEMPLATE)
```

- 中文 TeX 标签：

```python
from manim import Tex
Tex("晶面间距", tex_template=S01_TEX_TEMPLATE)
```

- 验证：`make tex-smoke`，输出 `media/images/tex_smoke_test/TeXSmokeTest_ManimCE_v0.19.0.png`。

### 1.4 已完成的冒烟测试

- Manim 中文测试帧：`media/images/manim_smoke_test/CJKSmokeTest_ManimCE_v0.19.0.png`
  - 1920×1080，思源黑体，中文与 `×` 符号显示正常。
- TTS 短句测试：`logs/tts_cpu_smoke.wav`、`logs/tts_wrapper_smoke.wav`
  - 24 kHz、单声道、16-bit PCM；6.24 秒音频约 32.6 秒计算（CPU）。
- TTS GPU 测试：`logs/tts_gpu_smoke.wav`
  - 4.32 秒音频约 3.9 秒计算（RTX 3060 Laptop）。
- XeLaTeX 公式测试：`media/images/tex_smoke_test/TeXSmokeTest_ManimCE_v0.19.0.png`
  - `MathTex(r"2d\sin\theta=n\lambda")` 与中文 `Tex("晶面间距")` 均正常。
- 环境检查脚本：`scripts/check_env.sh`。
- COD 参考谱线：`chapters/s01/assets/xrd_patterns.json`；Si 7 条、金红石 25 条（I≥1 显示）；测试命令 `make patterns`。

### 1.5 制作结果

- 成片：`chapters/s01/renders/s01_final.mp4`，9:38，1920×1080/30 fps，H.264/AAC。
- 旁白：100 个句子级片段，atempo=0.95，共 8:28；GPU 生成。
- 字幕：`s01_final.srt`（103 条）+ `s01_final.ass`（1920×1080 样式烧录）。
- 片尾：`chapters/s01/manim/credits.py`，黑底向上滚动 70 秒。
- 质检：`chapters/s01/renders/qc_report.md`。

### 1.6 S02 阶段实测（2026-11-01）

| 项 | 结论 |
|---|---|
| Qwen3-TTS 1.7B CustomVoice | 可用；RTX 3060 6 GB 上峰值约 4.4 GB；7 秒音频约 6–7 秒计算；逐句 `instruct` 生效 |
| Qwen3-TTS 0.6B CustomVoice | **会静默忽略 `instruct`**；S01 的 `--instruct` 实际未生效；S02 改用 1.7B |
| 逐句 `atempo` | 可行；`ffmpeg atempo` 逐句处理后与 `timing.json` 对齐；当前整稿 9:13 |
| Stable Diffusion 1.5 | 可用；`from_single_file` + 本地 `v1-inference.yaml` + `HF_ENDPOINT=https://hf-mirror.com`；768×512/24 步约 8 秒/张，峰值约 2.8 GB |
| 生图依赖 | `diffusers==0.31.0`、`transformers==4.57.3`（与 qwen-tts 兼容）；更晚的 diffusers 会要求 huggingface-hub ≥1.32，与 TTS 环境冲突 |
| LMMS | 1.2.2；无界面渲染用 `QT_QPA_PLATFORM=offscreen lmms render project.mmp -o out.wav`；SF2 Player 可用 |
| SoundFont | 本机 `GeneralUser-GS.sf2`、`FluidR3_GM.sf2`；License v2.0，允许音乐创作使用 |
| 句级同步 | `scripts/build_s02_timeline.py` 产出 `timing.json` + 整稿；音频总长与 timing 一致（553.1 s） |
| 动效层 | `MovingCameraScene` + `effects.py`（等距晶格、原子柱、径向辉光）；S00 样片 41 s |
| 模拟 HRTEM | 弱相位物体 + CTF；512×512，0.08 Å/px；只画 Sr 列，标“模拟计算，非实测” |

S02 新增脚本：

```text
scripts/build_s02_script.py        # TSV -> sentences.json / narration.txt / script.md
scripts/build_s02_timeline.py      # 逐句 TTS -> timing.json + 整稿旁白
scripts/build_s02_sim_tem.py       # SrTiO3 [001] 模拟 HRTEM
scripts/build_s02_illustrations.py # SD1.5 氛围插图
scripts/grade_s02_illustrations.py # 统一调色
scripts/build_s02_music.py         # MIDI + LMMS 工程 + 渲染
chapters/s02/manim/common.py       # TimelineScene：句级 cue + 相机推拉
chapters/s02/manim/effects.py      # 等距晶格、原子柱、辉光、标签底板
chapters/s02/manim/sync_demo.py    # S00 动效样片
chapters/s02/manim/README.md       # 3b1b 参考与动效规范
```

> Manim 会缓存 partial movie。修改 `self.remove()` 等非动画语句后，需要删除
> `partial_movie_files/S02SyncDemo/` 再渲染，否则会看到旧帧。

## 2. 工具链

| 环节 | 工具 | 用途 |
|---|---|---|
| 环境隔离 | `uv` + `.venv` | Manim/Python 渲染依赖，不污染系统 |
| 旁白 | Qwen3-TTS **1.7B** CustomVoice + conda `qwen3-tts` | 中文旁白，逐句生成；逐句 `instruct` 语气控制 |
| 生图 | Stable Diffusion 1.5（本地 GPU） | 氛围插图；不承担科学信息 |
| 配乐 | MIDI + LMMS 1.2.2 + SF2 Player（GeneralUser GS） | 原创配乐，可编辑 `.mmp`/`.mid` |
| 图形/动画 | Manim 0.19.0 | 矢量示意图、数学公式、动画、字幕安全区 |
| 公式排版 | XeLaTeX + `dvisvgm` | 通过 `src/render/tex.py` 的 `S01_TEX_TEMPLATE` 调用 |
| 数据处理 | Python 3.11 + numpy/scipy + gemmi 0.7.5 | 解析 COD CIF、计算结构因子/参考谱线、几何计算、时间轴 |
| 参考谱线 | `scripts/build_xrd_patterns.py` | COD Si/金红石 → 运动学近似棒状谱；画面标注“非实测” |
| 音频处理 | `ffmpeg`/`ffprobe` | 拼接、降噪、响度标准化、配乐压低 |
| 字幕 | SRT + `ffmpeg` `subtitles`/`libass` | 生成/烧录中文字幕 |
| 合成 | `ffmpeg` | 视频拼接、音画合成、H.264/AAC 转码 |
| 质量检查 | `ffprobe`、抽帧、脚本检查 | 时长、流、黑帧、响度、禁用词 |

## 3. 目录结构

```text
科普视频/
├── assets/
│   └── fonts/                 # 思源黑体/宋体、霞鹜文楷及 OFL 许可证
├── chapters/
│   └── s01/
│       ├── README.md          # 本期状态、交付物、审阅清单
│       ├── plan.md            # 制作规划、素材/TTS/渲染/合成计划
│       ├── script.md          # 旁白稿、术语、事实核对
│       ├── storyboard.md      # 分镜、画面、字幕、时长
│       ├── fact_check.md      # 逐条事实核对表
│       ├── assets/            # 本期专用素材（合成图、参考帧）
│       ├── audio/             # 旁白、配乐、混音中间文件
│       ├── manim/             # 本期 Manim 场景源码
│       └── renders/           # 预览、最终视频、SRT
├── docs/
│   ├── program_mainline.md
│   ├── technical_route.md
│   ├── references.md
│   ├── assets_and_licenses.md
│   ├── credits.md
│   ├── writing_guide.md       # 反“AI 味”工作法
│   ├── information_architecture.md  # 三级信息架构
│   └── operator_notes.md
├── logs/                      # 环境检查、渲染、TTS、合成日志
├── media/                     # Manim 默认输出（中间产物）
├── scripts/                   # 环境检查、渲染、合成、质检脚本
│   ├── env.sh                 # 统一 PATH/缓存入口
│   └── README.md
├── src/
│   ├── render/                # 主题、TeX 模板、Manim 场景、渲染辅助
│   └── tts/                   # TTS 封装
├── .venv/                      # 项目 Python 环境（不提交）
└── .cache/                     # uv/numba/matplotlib 缓存（不提交）
```

## 4. 渲染流程

### 4.1 旁白生成

1. 用 `scripts/extract_narration.py` 从句稿生成 `segments.json`（句子级，约 5–15 秒一段）与 `scene_segments.json`（场景级，用于时间轴）。
2. 用 `src/tts/generate_narration.py` 逐段生成 24 kHz 单声道 WAV。
3. 检查：发音、断句、语速、段落间停顿；必要时只重生成问题段落。
4. 用 `ffprobe` 读取每段时长，写入 `chapters/s01/audio/manifest.json`。
5. 按时间轴拼接，段间留 0.25–0.45 秒自然停顿；长句不强行加速。

命令示例（阶段三）：

```bash
source scripts/env.sh
/home/lanshuye/miniconda3/envs/qwen3-tts/bin/python \
  src/tts/generate_narration.py \
  --segments-json chapters/s01/script/segments.json \
  --out-dir chapters/s01/audio/segments \
  --device auto
```

当前默认 `--device auto` 会使用 CUDA；如显存不足或驱动异常，改为 `--device cpu`。

### 4.2 Manim 场景

- 每个镜头一个 `Scene` 或一个 `Scene` 内的 `play` 段；场景名与分镜 ID 对应（如 `S01_03_Bragg`）。
- 使用 `src/render/theme.py` 的统一颜色/字体/字号。
- 公式使用 `MathTex(..., tex_template=S01_TEX_TEMPLATE)`；中文标签用 `Text` 或 `Tex(..., tex_template=S01_TEX_TEMPLATE)`。
- 必须先 `source scripts/env.sh`，让 `xelatex`/`dvisvgm` 进入 `PATH`；否则 Manim 会找不到编译器。
- 所有示意图在角落标注“示意”或“模型数据，非实测”。
- 渲染质量：预览 `-ql`；终稿 `-qh --fps 30`；需要透明叠加时用 `--transparent`。
- 输出 silent segments 到 `chapters/s01/renders/segments/`，最后统一拼接。

命令示例：

```bash
source scripts/env.sh

.venv/bin/manim -ql --fps 30 \
  --media_dir media \
  chapters/s01/manim/scene_01.py S01_01_Scale

.venv/bin/manim -qh --fps 30 \
  --media_dir media \
  chapters/s01/manim/scene_01.py S01_01_Scale
```

### 4.3 拼接与混音

1. 用 `ffmpeg concat` 拼接 silent segments；确保分辨率、帧率、像素格式一致。
2. 旁白做轻降噪/高通（80 Hz）、段落间静音、整体响度标准化。
3. 配乐：项目自制合成 ambient pad，无第三方采样；音量压到旁白以下。
4. 侧链压缩（可选）：旁白出现时配乐自动下压 2–4 dB。
5. 目标响度：综合响度约 −16 LUFS，真峰值 ≤ −1.5 dBTP；配乐单独约 −28 至 −24 LUFS。
6. 字幕：先生成 SRT，再转成 1920×1080 的 ASS；用 `ass` 滤镜烧录，指定 `fontsdir`。

命令示例：

```bash
# 两遍 loudnorm，第二遍用第一遍测得的数值
ffmpeg -hide_banner -i narration.wav \
  -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json \
  -f null -

ffmpeg -hide_banner -y \
  -i chapters/s01/renders/s01_silent.mp4 \
  -i chapters/s01/audio/s01_mix.wav \
  -vf "ass=chapters/s01/renders/s01_final.ass:fontsdir=assets/fonts" \
  -c:v libx264 -preset fast -crf 19 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart -shortest \
  chapters/s01/renders/s01_final.mp4
```

### 4.3.1 封面生成与 4:3 检查

封面是 16:9，但核心内容必须位于居中 4:3 区域（1920×1080 画布上为 1440×1080，x=240–1680）。

```bash
source scripts/env.sh
make cover
```

产物：
- `chapters/s01/renders/cover.png`（1920×1080，16:9）
- `chapters/s01/renders/cover_4x3_preview.png`（中心 1440×1080 裁切，仅用于质检）

生成脚本：`chapters/s01/manim/cover.py`。封面属于可重复生成的发布素材，按 `docs/repository_policy.md` 不入 Git。

### 4.4 画面安全区

- 标题/主体：左右各留 8%，顶部留 10%。
- 字幕：底部 12% 为字幕带；关键图形不要压到字幕带。
- 片尾署名：居中，字号不小于 20 px（1080p 下约 20–24 px）。

## 5. 字体与素材版权

- 字体：思源黑体 CN、思源宋体 CN、霞鹜文楷，均为 SIL OFL 1.1；文件与许可证在 `assets/fonts/`，记录在 `docs/assets_and_licenses.md`。
- Manim 使用 `manimpango.register_font()` 显式注册文件；ffmpeg 字幕使用 `fontsdir` + `FontName`。
- 画面素材：目前全部为项目自制矢量图/合成数据，不使用来源不明的网络图片。
- 配乐：优先项目自制合成音；若改用外部素材，必须是 CC0/公共领域或明确允许嵌入的许可证，并记录 URL、作者、许可证、下载日期。
- 不使用需登录、付费、限制嵌入、版权不明的素材。

## 6. 质量检查

### 6.1 技术检查

- `ffprobe`：分辨率 1920×1080、30 fps、H.264、AAC、时长与预期一致。
- 抽帧：每个场景至少 1 帧，检查中文字体、对齐、无裁切、无黑帧。
- 音频：`loudnorm` 统计、波形峰值、旁白/配乐比例；无爆音、无长静音。
- 字幕：逐条对照旁白，检查错别字、术语、断句、时间轴；不使用机器翻译式表达。
- 禁用内容扫描：路径、命令、环境名、终端、代码、日志、工具水印、调试坐标。
- 文案自查：`make copy-check`（AI 味提示 + L0 泄漏扫描）。
- 信息层级：按 `docs/information_architecture.md` 检查 L0 成片只含观众需要的内容。

### 6.2 科学检查

- 逐条对照 `chapters/s01/fact_check.md`。
- 公式、单位、数量级、历史年份至少两源交叉。
- 示意图与旁白一致；示意图标注“示意/模型数据”。
- 不把“平均结构”说成“单晶照片”；不把“峰宽”只说成“粒径”。

## 7. 风险与替代方案

| 风险 | 影响 | 处理 |
|---|---|---|
| TeX Live 路径未加入 `PATH` | `MathTex` 报找不到 `xelatex`/`dvisvgm` | 先 `source scripts/env.sh`；`scripts/check_env.sh` 会检查 |
| 6 GB 显存吃紧 | TTS/渲染同时跑可能 OOM | TTS 与 Manim 分开跑；TTS 失败时 `--device cpu` |
| TTS 读法不稳定 | 公式符号、英文缩写可能读错 | 先做短句试听；旁白不念符号；必要时改写为中文说法 |
| 公式字体与正文字体不一致 | 数学公式为衬线体，正文为黑体 | 可接受；若需统一，改用 `unicode-math` + 无衬线数学字体，先做样张确认 |
| 中文路径/空格 | 命令易断 | 所有路径加引号；脚本内用 `Path`；不依赖 shell 拼接 |
| 磁盘剩余约 77 GB | 1080p 中间帧占用大 | 用 `-s`/低质量预览；及时清理 `media/videos` 中间文件；保留终稿 |
| 网络下载不稳定 | 外部素材/许可证页可能失败 | 字体已本地化；素材自制；许可证文本本地保存 |
| 科学细节争议 | 误导观众 | 按 `fact_check.md` 逐条核对；不确定处先问操作员 |
| 字幕遮挡画面 | 关键信息被挡 | 分镜阶段预留底部字幕带；字幕最多两行 |
| 电子显微内容过多 | 第一期超时/失焦 | S01 只做桥接；细节留给 S02 |

## 8. 复现命令

```bash
# 0. 进入项目并加载环境
cd "/home/lanshuye/文档/科普视频"
source scripts/env.sh

# 1. 环境检查
bash scripts/check_env.sh

# 2. Manim 中文冒烟测试
.venv/bin/manim -qh --fps 30 -s --media_dir media \
  src/render/manim_smoke_test.py CJKSmokeTest

# 3. XeLaTeX 公式冒烟测试
.venv/bin/manim -qh --fps 30 -s --media_dir media \
  src/render/tex_smoke_test.py TeXSmokeTest

# 4. TTS 参数检查（不加载模型）
/home/lanshuye/miniconda3/envs/qwen3-tts/bin/python \
  src/tts/generate_narration.py \
  --segments-json chapters/s01/script/segments.json \
  --out-dir chapters/s01/audio/segments \
  --device auto --dry-run
```

完整构建命令见 `chapters/s01/README.md`、`scripts/README.md` 和 `Makefile`；S01 已按这些命令完成。

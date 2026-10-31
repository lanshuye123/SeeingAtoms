# 版本控制策略

> 目的：让 Git 仓库只保留“人写的/必须固定的源”，不把可由脚本重复生成的音频、视频、字幕、图片和中间产物塞进历史。
> 适用：本仓库所有期数；S01 已按此策略执行。

## 1. 入库（track）

| 类别 | 内容 |
|---|---|
| 文档 | `README.md`、`docs/*.md`、`chapters/s01/*.md` |
| 构建入口 | `Makefile`、`scripts/*.sh`、`scripts/*.py`、`scripts/README.md` |
| 源码 | `src/**/*.py`、`chapters/s01/manim/*.py` |
| 字体许可证 | `assets/fonts/LICENSE-*.txt`、`OFL-LXGWWenKai.txt` |
| 开放结构数据 | `chapters/s01/assets/cif/*.cif`（体积小、带原始文献署名） |
| 质检摘要 | `chapters/s01/renders/qc_report.md`（人工可读的交付记录） |

字体二进制是构建必需的第三方资产，但不是程序生成物；为了控制仓库体积，**默认不入库**，只保留许可证与获取脚本 `scripts/fetch_fonts.sh`。在新机器上先运行 `make fonts`（从本机字体目录复制并校验 SHA-256），或按 `docs/assets_and_licenses.md` 的上游地址安装。

CIF 是外部开放数据（COD），体积只有几 KB；入库可以让构建不依赖不稳定的网络，但必须保留 COD 编号与原始文献署名。

## 2. 不入库（ignore）

| 类别 | 路径/模式 | 生成方式 |
|---|---|---|
| Python 环境/缓存 | `.venv/`、`.cache/`、`__pycache__/` | `uv`/Python |
| 日志 | `logs/` | 运行脚本 |
| 中间媒体 | `media/` | Manim |
| 旁白/配乐/混音 | `chapters/s01/audio/`、`*.wav` | 千问 TTS、合成脚本、ffmpeg |
| 成片/字幕/渲染段 | `chapters/s01/renders/*`（`qc_report.md` 除外）、`*.mp4`、`*.srt`、`*.ass` | Manim、ffmpeg |
| 字体二进制 | `assets/fonts/*.otf`、`*.ttf` | 系统字体包/上游字体项目；`make fonts` |
| 风格样张 | `chapters/s01/assets/style_frame_*.png` | Manim |
| 计算谱线 | `chapters/s01/assets/xrd_patterns.json` / `.txt` | `scripts/build_xrd_patterns.py` |
| 派生文本 | `chapters/s01/script/narration.txt`、`segments.json`、`scene_segments.json` | `scripts/extract_narration.py` |

`chapters/s01/renders/qc_report.md` 是唯一保留在 `renders/` 下的文件；它记录最终成片的规格、校验和与已知问题，供验收用。

## 3. 为什么这样分

1. **单一事实源**：旁白以 `chapters/s01/script.md` 为准；`segments.json`、`narration.txt` 都是派生文件，改稿后重新生成即可。
2. **仓库体积**：S01 的音频、视频、中间帧约 500 MB；全放进来会让 clone 和 diff 变得不可用。
3. **可复现**：所有被忽略的资源都能由 `Makefile`/`scripts/` 重建；命令见 `scripts/README.md`。
4. **许可证**：成片里用到的字体/COD 数据/音乐来源都记录在 `docs/assets_and_licenses.md`；入库的是许可证与小型源数据，不是生成物。
5. **交付分离**：最终 MP4/SRT 是“发布产物”，通过文件分发或 release artifact 交付，不靠 Git 历史保存。

## 4. 复现被忽略的资源

```bash
cd "/home/lanshuye/文档/科普视频"
source scripts/env.sh

make fonts      # 字体二进制（默认不入库）
make patterns   # COD CIF -> xrd_patterns.json
make audio      # TTS 片段 -> 场景音频 -> 配乐 -> s01_mix.wav
make srt        # timing.json -> SRT -> ASS
make scenes     # Manim -> renders/segments/S00..S09.mp4
make credits    # Manim -> renders/segments/S10_credits.mp4
make concat     # 拼接 silent.mp4
make final      # 烧字幕 + 混音 -> s01_final.mp4
```

## 5. 提交前检查

```bash
git status --short
git check-ignore -v chapters/s01/renders/s01_final.mp4
git check-ignore -v chapters/s01/audio/s01_mix.wav
git check-ignore -v chapters/s01/assets/style_frame_01.png
```

如果生成物出现在 `git status` 里，先检查 `.gitignore`，不要把大文件 `git add -f` 进去。

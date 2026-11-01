# 素材与许可证记录

> 更新日期：2026-11-01
> 原则：所有进入成片的第三方素材必须有明确来源与许可证；无法确认的素材不用。
> 当前阶段：S01 仅使用项目自制图形与本地开源字体；S02 新增 CC0/PD 实拍图、AI 氛围插图、原创 MIDI 配乐与模拟 HRTEM（见 §8）。

## 1. 字体

字体文件均已复制到 `assets/fonts/`，Manim 与 ffmpeg 字幕统一从该目录读取。字体二进制默认不入 Git（体积约 63 MB），只保留许可证与 `scripts/fetch_fonts.sh`；新机器运行 `make fonts` 从本机字体目录复制并校验 SHA-256。

| 文件 | 字体名 | 来源 | 许可证 | 本地许可证 | SHA-256 |
|---|---|---|---|---|---|
| `SourceHanSansCN-Regular.otf` | 思源黑体 CN / Source Han Sans CN | Adobe Source Han Sans；本机 `/usr/share/fonts/adobe-source-han-sans/`；上游 https://github.com/adobe-fonts/source-han-sans | SIL Open Font License 1.1 | `assets/fonts/LICENSE-SourceHanSans.txt` | `e2bc8a2e7f37474b774fff8db758681ece40bb6947a90d571bce9dd60671a8e4` |
| `SourceHanSansCN-Bold.otf` | 思源黑体 CN Bold | 同上 | SIL OFL 1.1 | 同上 | `62383707c086a32f3afd5e293f34c7eff64c7fea31f579fdc6cbe34d920519a6` |
| `SourceHanSerifCN-Regular.otf` | 思源宋体 CN / Source Han Serif CN | Adobe Source Han Serif；本机 `/usr/share/fonts/adobe-source-han-serif/`；上游 https://github.com/adobe-fonts/source-han-serif | SIL OFL 1.1 | `assets/fonts/LICENSE-SourceHanSerif.txt` | `3754ea669c530e2473354f8f6d9f79680a44d7e26ec7d00eeabee4a7e0753c5d` |
| `SourceHanSerifCN-SemiBold.otf` | 思源宋体 CN SemiBold | 同上 | SIL OFL 1.1 | 同上 | `50d3f12201ce2dd840650b6bfa47ebb8572ecf767eec0e5ccb20a247b5bfa805` |
| `LXGWWenKai-Regular.ttf` | 霞鹜文楷 / LXGW WenKai | LXGW WenKai；本机 `/usr/share/fonts/lxgw-wenkai-v1.522/`；上游 https://github.com/lxgw/LxgwWenKai | SIL OFL 1.1 | `assets/fonts/OFL-LXGWWenKai.txt` | `39ad71264b588165b469e35e6afb162a378dacd1f95348160240ba9038ac3009` |

### 1.1 署名与合规

- OFL 允许嵌入、分发字体，要求保留版权与许可证；本项目在 `assets/fonts/` 保留完整许可证。
- 片尾用一行简洁署名即可：
  > 字体：思源黑体 / 思源宋体 / 霞鹜文楷（SIL Open Font License 1.1）
- 不在画面中放许可证全文；全文见本文件与 `assets/fonts/`。
- 不修改字体文件，不单独售卖字体。

## 1.2 开放晶体结构数据（COD）

| 文件 | 结构 | COD | 原始文献 | 许可/使用条件 | SHA-256 |
|---|---|---|---|---|---|
| `chapters/s01/assets/cif/Si_9008565.cif` | Si，金刚石立方，Fd-3m，a=5.4307 Å | [9008565](http://www.crystallography.net/cod/9008565.html) | Wyckoff R W G. *Crystal Structures*, 2nd ed., 1963, 1: 7–83. 原始数据 AMCSD 0011243 | COD 条目要求对原始文献作 proper attribution | `46fb44ccdf93d1c3c1ecbe5b04ab0dea28c786bac20467b3a7511199af50e386` |
| `chapters/s01/assets/cif/Rutile_9004141.cif` | TiO2 金红石，P42/mnm，a=4.593 Å，c=2.959 Å，25 °C | [9004141](http://www.crystallography.net/cod/9004141.html) | Meagher E P, Lager G A. *The Canadian Mineralogist*, 1979, 17: 77–85. 原始数据 AMCSD 0005164 | 同上 | `ce9abab142351e802bde3eb40dbb554bb3ccec08e8c6ddc4299c0c532e9794ce` |

- 计算谱线：`chapters/s01/assets/xrd_patterns.json` / `.txt`，由 `scripts/build_xrd_patterns.py` 生成；`gemmi 0.7.5`，Cu Kα1=1.5406 Å，运动学近似。
- 片尾/说明栏保留 COD 编号与原始文献；不把计算谱线说成实测数据。
- COD 首页：http://www.crystallography.net/ ；条目页含完整元数据。

## 2. 项目自制素材

以下素材由本项目生成，不含第三方图像/音频采样：

| 素材 | 位置 | 说明 | 许可/状态 |
|---|---|---|---|
| Manim 中文冒烟测试帧 | `media/images/manim_smoke_test/CJKSmokeTest_ManimCE_v0.19.0.png` | 仅用于技术验证，不进入成片 | 项目自制 |
| S01 标题风格样张 | `chapters/s01/assets/style_frame_01.png` | 视觉方向参考；含“非成片”标记 | 项目自制 |
| S01 布拉格公式样张 | `chapters/s01/assets/style_frame_02_bragg.png` | 视觉方向参考；含“示意·非成片”标记 | 项目自制 |
| S01 配乐 bed | `chapters/s01/audio/music_main.wav`、`music_credits.wav` | Python 合成 ambient pad，无第三方采样 | 项目自制 |
| S01 成片/字幕 | `chapters/s01/renders/s01_final.mp4`、`.srt`、`.ass` | 最终交付物；含 COD 数据与第三方工具署名 | 项目自制（素材见 1.2） |
| S01 封面 | `chapters/s01/renders/cover.png`、`cover_4x3_preview.png` | 16:9 封面及中心 4:3 裁切检查图 | 项目自制 |
| XeLaTeX 公式测试帧 | `media/images/tex_smoke_test/TeXSmokeTest_ManimCE_v0.19.0.png` | 公式/中文 TeX 验证，不进入成片 | 项目自制 |
| TTS 冒烟测试音频 | `logs/tts_cpu_smoke.wav`、`logs/tts_wrapper_smoke.wav` | 仅用于环境验证，不进入成片 | 项目自制 |
| 主题色/字体配置 | `src/render/theme.py` | 视觉规范代码 | 项目自制 |
| S01 概念图/动画 | `chapters/s01/manim/`（阶段三生成） | 晶体、波、衍射圆锥、图谱等 | 项目自制 |
| S01 合成衍射数据 | `chapters/s01/assets/`（阶段三生成） | 简单立方模型数据，画面标注“模型数据，非实测” | 项目自制 |

## 3. 配乐与音效

### 当前状态

- 阶段二未使用任何第三方配乐/音效。
- 成片计划使用**项目自制合成 ambient pad**：用 Python 生成低频持续音、柔和和声与轻度滤波噪声，不含采样材料。
- 这样处理的原因：避免版权不明、登录/付费限制、CC-BY 归属信息缺失等风险。

### 如果改用外部素材

必须先在操作员日志中记录，再使用；记录字段如下：

| 字段 | 要求 |
|---|---|
| 作品名 | 原名称 |
| 作者 | 作者/演奏者 |
| 来源 URL | 可直接访问的原始页面 |
| 许可证 | CC0 / Public Domain / CC-BY 4.0 等，附许可证链接 |
| 下载日期 | YYYY-MM-DD |
| 修改 | 是否剪辑、变调、混音 |
| 署名要求 | 是否需要在片尾署名；署名文案 |
| 文件哈希 | SHA-256 |

禁止使用：版权不明、需登录、付费、限制嵌入、仅“免费试听”、来源为搬运/二传的素材。

## 4. 第三方图片/视频

当前：使用 COD 的 Si/金红石 CIF 数据，按原始文献署名；未使用论文插图、厂商图或网络图片。

如后续需要真实显微照片或衍射图，优先顺序：

1. 项目自制合成图（标注“示意/模型数据”）；
2. 公共领域（PD）或 CC0 素材；
3. CC-BY 素材（片尾与说明栏署名）；
4. 获得书面授权的素材。

不使用期刊封面、论文插图、厂商宣传图、社交媒体图片，除非有明确再使用许可。

## 5. 软件与工具许可证（操作员可见）

| 工具 | 版本 | 许可证/说明 |
|---|---|---|
| Manim Community | 0.19.0 | MIT License |
| FFmpeg | 9.0.2 | LGPL/GPL（按发行版编译选项）；本项目仅调用命令行 |
| Qwen3-TTS | 本地模型/代码 | 以模型仓库与代码仓库许可证为准；本项目不修改模型代码，仅调用推理接口 |
| Python | 3.11.15（项目）/ 3.12.13（TTS） | PSF License |
| 思源黑体/宋体 | 本地版本 | SIL OFL 1.1 |
| TeX Live 2025 | 本地安装 | TeX Live 发行版（含 LPPL 等自由许可证）；本项目仅调用 `xelatex`/`dvisvgm`，不随视频再分发 |
| 霞鹜文楷 | 本地版本 | SIL OFL 1.1 |

> 说明：软件许可证不影响视频内容的版权，但再分发本项目时需保留相应许可证文本。当前交付物为视频与文档，不包含软件二进制。

## 6. 片尾署名草案

见 `docs/credits.md`。原则：只列必要署名，不列 URL、DOI、内部路径、软件安装信息。

## 7. 待确认

1. 片尾是否出现具体作者/单位/指导教师姓名；如需要，请提供准确写法。
2. 是否接受项目自制配乐；如希望使用特定风格/曲目，请提供可授权来源。
3. 是否需要把课程笔记作者/课程名称写入片尾；当前只写“课程笔记支持”，不写个人姓名。

## 8. S02 新增素材（2026-11-01）

### 8.1 第三方图像（CC0 / 公共领域）

| 文件 | 内容 | 来源/作者 | 许可证 | 修改 | 署名 |
|---|---|---|---|---|---|
| `chapters/s02/assets/cc0/cdc_tem_1965.jpg` | 1965 年 CDC 透射电镜历史照片 | CDC / C. Duncan；<http://www.publicdomainfiles.com/show_file.php?id=13515915019118> | 公共领域（美国联邦政府作品） | 未修改；正式使用时可能裁切/去色 | 建议 “CDC / C. Duncan, 1965” |
| `chapters/s02/assets/cc0/nist_graphene_chips.jpg` | NIST 石墨烯芯片与硬币比例照片 | NIST；<https://www.nist.gov/image/graphene-chipsjpg> | 公共领域（Credit NIST） | 未修改；可能裁切 | “Credit: NIST” |
| `chapters/s02/assets/cc0/nist_moon_dust_sem.png` | NIST 月尘颗粒 SEM 图（1 µm 标尺） | NIST；<https://www.nist.gov/image/moon-dust-particle-4-4> | 公共领域（Credit NIST） | 未修改；画面标“SEM，非原子级” | “Credit: NIST” |

- 哈希、逐张说明、使用边界见 `chapters/s02/assets/cc0/LICENSES.md` 与 `SHA256SUMS.txt`。
- 未使用来源不明的论文插图、厂商图、社交媒体图。

### 8.2 项目自制：模拟 HRTEM

| 文件 | 内容 | 生成方式 | 标注 |
|---|---|---|---|
| `chapters/s02/assets/sim/sim_srtio3_001_sr_under.png` | SrTiO₃ [001] 模拟高分辨像，Sr 列亮 | 弱相位物体 + CTF，200 kV，Cs=1 mm，离焦 −20 nm，5 nm | “模拟计算 · 非实测” |
| `..._sr_over.png` | 同上，离焦 +20 nm，亮点/暗点反转 | 同上 | 同上 |
| `..._sr_thick.png` | 同上，厚度 12 nm，投影叠加更多 | 同上 | 同上 |
| `..._params.json` | 参数、模型、边界说明 | 脚本 `scripts/build_s02_sim_tem.py` | — |

- 只画 Sr 原子列，所以亮点构成 3.905 Å 方格子；不代表 Ti/O 不存在。
- 不是 multislice，不用于定量匹配；只用于讲解“亮点=原子列投影”和“离焦反转”。
- 若操作员要求真实 HRTEM：需要一张明确 CC0/PD 或书面授权的材料学图像；当前未找到满足条件的图，故不冒充实拍。

### 8.3 项目自制：AI 氛围插图

| 文件 | 内容 | 生成方式 | 许可/状态 |
|---|---|---|---|
| `chapters/s02/assets/illustrations/*.png` | 铜网、电镜、薄片、相位、实验室、荧光屏 6 组氛围图 | Stable Diffusion v1.5，本地 GPU，txt2img；参数见 `prompts.json` | 生成图，项目自制；模型许可 CreativeML Open RAIL-M；模型权重不随视频分发 |
| `..._graded.png` | 统一调色版（1920×1080） | `scripts/grade_s02_illustrations.py` | 项目自制 |
| `contact_sheet_graded.png` | 六张联系表 | PIL | 仅供审阅 |

- AI 图只做背景/质感，不承担科学信息；画面角落标“氛围插图 · 非科学数据”。
- 如操作员不接受 AI 图，可整组弃用，不影响科学内容。

### 8.4 项目自制：原创配乐

| 文件 | 内容 | 制作方式 | 许可 |
|---|---|---|---|
| `chapters/s02/assets/music/s02_theme.mid` | 原创 MIDI，28 小节 | `scripts/build_s02_music.py` | 项目原创 |
| `s02_theme.mmp` | LMMS 1.2.2 工程，4 条 SF2 Player 轨道 | 由脚本生成 | 项目原创 |
| `s02_theme.wav` / `_norm.wav` | LMMS 渲染 / −23 LUFS 床轨 | LMMS + GeneralUser GS | 项目原创 |
| 音色库 | GeneralUser GS v1.471 | S. Christian Collins；License v2.0 | 用于渲染，不随视频再分发；细节见 `chapters/s02/assets/music/README.md` |

- 没有使用商业录音采样；没有使用 AI 生成音乐服务。
- 片尾建议署名：“音乐：本片原创（LMMS + GeneralUser GS）”。

### 8.5 TTS 与模型

| 项目 | 版本/路径 | 许可/说明 |
|---|---|---|
| Qwen3-TTS 1.7B CustomVoice | `/home/lanshuye/Projects/QwenTTS/Qwen3-TTS-12Hz-1.7B-CustomVoice` | 以模型仓库许可证为准；本项目只调用推理，不修改模型代码，不再分发权重 |
| Qwen3-TTS 0.6B CustomVoice | 同上（旧） | 0.6B 会忽略 `instruct`；S02 改用 1.7B |
| Stable Diffusion 1.5 | `/home/lanshuye/Projects/QwenTTS/sd15/sd15.safetensors` | CreativeML Open RAIL-M；模型权重不随视频分发 |

- 旁白、样音、整稿音频均为项目自制（TTS 生成 + 剪辑），不包含第三方录音。
- 若未来把 TTS 音频单独再分发，需同时核对模型许可证的再分发条款。

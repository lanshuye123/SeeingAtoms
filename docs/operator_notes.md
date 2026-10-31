# 操作员说明与工作日志

> 本文档面向操作员/制作者，不进入最终视频。
> 记录环境、问题、决策与复现方式；最终观众不应看到本文件内容。
> 信息层级规则见 [`information_architecture.md`](information_architecture.md)。

## 1. 当前阶段

- 阶段一（初始化/工具验证/理论验证）：已完成。
- 阶段二（S01 文案/分镜/规划）：v0.3 已完成。
- 阶段三（正式制作）：已完成；成片 `chapters/s01/renders/s01_final.mp4`（9:38），待验收。

## 2. 环境与工具结论（2026-10-31 23:10 更新）

| 项 | 结论 |
|---|---|
| ffmpeg / ffprobe | 可用，9.0.2；含 libx264、AAC、loudnorm、libass |
| uv | 可用，0.13.6；缓存需指向工作区 |
| Manim | 项目 `.venv` 内 0.19.0，Python 3.11.15；中文渲染通过 |
| LaTeX | **可用**：TeX Live 2025，`/home/lanshuye/Apps/texlive/2025/bin/x86_64-linux`；`xelatex`/`latex`/`dvisvgm` 均可用 |
| TTS conda 环境 | 存在，Python 3.12.13；模型存在 |
| GPU | **可用**：RTX 3060 Laptop，6 GB；`torch.cuda.is_available()` 为 True |
| TTS GPU | 4.32 秒音频约 3.9 秒计算，接近实时 |
| 成片 | 9:38，1920×1080/30 fps，H.264/AAC，约 −16 LUFS |
| TTS CPU 回退 | 6.4 秒音频约 37 秒计算，约 5–6 倍实时 |
| 字体 | 已本地化到 `assets/fonts/`，OFL 许可证齐全 |
| 课程笔记 | 两个部分均可读，已记录行号 |

> 统一入口：渲染/生成前先 `source scripts/env.sh`，它会设置 TeX Live PATH、uv/numba 缓存目录。

## 3. 已解决的问题

### 3.1 Manim 安装失败（pycairo / ccache）

**现象**：Python 3.13 环境下 `pycairo` 从源码编译，`ccache` 报 `Read-only file system`，安装中断。

**处理**：
- 改用 Python 3.11（`uv venv --python 3.11`）；
- 设置 `CCACHE_DISABLE=1`；
- 设置 `UV_CACHE_DIR` 到项目内 `.cache/uv`。

**结果**：Manim 0.19.0 安装成功，冒烟测试通过。

### 3.2 TTS 导入失败（numba cache locator）

**现象**：
```text
RuntimeError: cannot cache function '__o_fold': no locator available
```

**原因**：`numba` 默认缓存目录不可写/不可定位；与模型代码无关。

**处理**：在导入 `qwen_tts` 前设置 `NUMBA_CACHE_DIR` 到项目内 `.cache/numba`。未修改模型代码。

**结果**：导入成功；CPU/GPU 推理均成功。

### 3.3 GPU 曾不可用（已解决）

**历史现象**：早期会话中 `nvidia-smi` 无法连接驱动；`torch.cuda.is_available()` 为 False。

**现状（2026-10-31 23:10）**：驱动恢复，RTX 3060 Laptop 可见，CUDA 可用。TTS GPU 短测通过。

**处理**：脚本 `--device auto` 默认走 CUDA；保留 `--device cpu` 回退。6 GB 显存下不要把 TTS 与 Manim 渲染同时跑。

### 3.4 LaTeX 未在默认 PATH（已解决）

**现象**：系统默认 PATH 中没有 TeX Live；Manim 直接调用 `xelatex` 会失败。

**处理**：
- 新增 `scripts/env.sh`，把 `/home/lanshuye/Apps/texlive/2025/bin/x86_64-linux` 放到 PATH 前面；
- 新增 `src/render/tex.py`，定义 `S01_TEX_TEMPLATE`（XeLaTeX + xeCJK + 思源黑体）；
- 新增 `src/render/tex_smoke_test.py`，验证公式与中文 TeX 标签。

**结果**：`2d sinθ = nλ` 与“晶面间距”均正常渲染，测试帧在 `media/images/tex_smoke_test/`。

### 3.5 网络下载不稳定

**现象**：从 GitHub raw 下载字体许可证时连接超时。

**处理**：字体从本机已安装版本复制；OFL 全文从本机霞鹜文楷许可证提取，并加上 Adobe 版权头；未依赖外部下载完成关键路径。

## 4. 已完成的冒烟测试

| 测试 | 命令/产物 | 结果 |
|---|---|---|
| Manim 中文 | `.venv/bin/manim -qh --fps 30 -s ... CJKSmokeTest` | 1920×1080 PNG，中文正常 |
| XeLaTeX 公式 | `src/render/tex_smoke_test.py` | 公式 + 中文 TeX 标签正常 |
| TTS CPU | Qwen3-TTS，6.4 秒音频 | 37.3 秒计算，24 kHz 单声道 |
| TTS GPU | `logs/tts_gpu_smoke.wav` | 4.32 秒音频，3.9 秒计算 |
| 环境检查 | `scripts/check_env.sh` | 通过；0 失败、0 警告 |

产物在 `logs/`、`media/images/manim_smoke_test/`、`media/images/tex_smoke_test/`，仅用于验证，不进入成片。

## 4.1 发音试听样本

为确认“X 射线”的读法，生成了以下短样本（仅用于试听，不进入成片）：

- `logs/tts_pron/A_x.wav`：`这是X射线。`
- `logs/tts_pron/B_aikesi.wav`：`这是艾克斯射线。`
- `logs/tts_pron/C_cha.wav`：`这是叉射线。`
- `logs/tts_pron/D_xguang.wav`：`这是X光。`
- `logs/tts_pron/E_x.wav`：`X`
- `logs/tts_pron/F_aikesi.wav`：`艾克斯`
- `logs/tts_pron/G_cha.wav`：`叉`

**操作员已试听确认**：Qwen3-TTS 读作“埃克斯”，可用。该待确认项关闭。

## 5. 关键决策

1. **第一期只讲 X 射线衍射**，不把电子显微细节塞进同一期；结尾只做桥接。
2. **用“读出”而不是“看见”**描述 X 射线晶体学，避免把反演结构说成直接照片。
3. **画面全部自制矢量图**，不使用来源不明的论文插图/厂商图。
4. **配乐计划自制**，避免 CC-BY 归属遗漏和版权风险。
5. **公式用 XeLaTeX**：本地 TeX Live 已可用，使用 `S01_TEX_TEMPLATE`；中文标签用 `Text`/`Tex`。
6. **字幕计划烧录 + 单独 SRT**，兼顾观看与可编辑性。
7. **旁白反 AI 味**：按 `docs/writing_guide.md` 重写；少清单腔、少对称句、多具体场景。
8. **三级信息架构**：按 `docs/information_architecture.md` 分离观众内容、操作员文档、内部工作流。

## 5.1 制作结果（2026-11-01 00:00 左右）

- 旁白：100 个句子级片段，atempo=0.95，共 8:28；GPU 生成。
- 成片：9:38（含 70 秒滚动片尾），1920×1080/30 fps，H.264 + AAC。
- 数据：COD 9008565（Si）、9004141（金红石 25 °C）；`scripts/build_xrd_patterns.py` 计算，标注“COD 结构计算 · 非实测”。
- 字幕：103 条 SRT + styled ASS。
- 片尾：黑底向上滚动；字体、FFmpeg、Manim、Qwen3-TTS、Python、TeX Live、DeepSeek-V4.1-Flash-1017、COD 与 GB/T 7714 参考文献。
- 质检：见 `chapters/s01/renders/qc_report.md`。

## 6. 待操作员确认

1. 系列名、第一期标题、目标时长（9 分 38 秒，含片尾）。
2. 旁白语气是否仍有“AI 味”；哪些句子需要再口语化。
3. 片尾是否出现具体姓名/单位。
4. 是否需要在片中给出真实材料案例（如锐钛矿/金红石）；当前 S01 用“简单立方模型”避免真实数据争议。
5. 是否保留“反射 ≠ 镜面反射”的纠偏镜头。

已关闭：GPU 可用性、LaTeX 可用性、“X 射线”TTS 读法、CPU 时间成本。

## 7. 复现入口

```bash
cd "/home/lanshuye/文档/科普视频"
source scripts/env.sh
bash scripts/check_env.sh
cat logs/environment_check.txt

# 中文冒烟
make smoke

# XeLaTeX 冒烟
make tex-smoke

# TTS 参数检查
make tts-dry
```

完整构建命令见 `chapters/s01/README.md`、`scripts/README.md` 与 `Makefile`；S01 已按这些命令完成。

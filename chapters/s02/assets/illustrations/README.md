# S02 AI 氛围插图

> 用途：背景/质感/转场，不承担任何科学信息。
> 模型：Stable Diffusion v1.5（单文件 checkpoint，ModelScope 镜像）。
> 生成脚本：`scripts/build_s02_illustrations.py`；调色脚本：`scripts/grade_s02_illustrations.py`。

## 1. 为什么用 AI 图

S01 的画面全部是矢量示意图，干净但偏“讲义”。S02 需要一点“真实实验室的空气”：铜网的金属反光、绿屏的余光、暗房间里的仪器轮廓。这些不涉及定量信息，适合用生图模型做氛围层。

AI 图不用于：
- 电镜内部结构（磁透镜、光阑、光路）；
- 衍射图、高分辨像、能谱；
- 任何需要标注数字、角度、晶面指数的画面。

这些仍由 Manim 与计算生成。

## 2. 清单

| ID | 内容 | 计划用途 | 建议 |
|---|---|---|---|
| `ai_01_copper_grid` | 铜网/网格 macro 纹理 | S00 开场背景 | 可用；建议再叠一层矢量铜环，避免被当成真实样品 |
| `ai_02_column` | 暗室里的电镜轮廓 | S00_02 样品杆/电镜 | 可用；调色后偏青，适合做背景 |
| `ai_03_beam_slab` | 薄片边缘 + 光束 | S01/S02 过渡 | 可用；不要用它解释布拉格 |
| `ai_04_phase` | 相位波纹 | S04 相位段 | 可用；抽象，不误导 |
| `ai_05_lab` | 暗室管道/仪器 | S06 氛围 | 备选；偏“工厂”，需重做或只取局部 |
| `ai_06_phosphor` | 绿色荧光屏纹理 | S00_03/04 | 备选；偏“织物”，建议重做或只用局部光斑 |

- `*_graded.png`：1920×1080，已按系列色（深墨蓝/青绿/琥珀）做三段映射、暗角、轻颗粒。
- `contact_sheet_graded.png`：六张调色版的联系表，方便一眼筛选。
- `prompts.json`：模型、种子、步数、CFG、负面词、用途；可复现。

## 3. 使用规则

1. 作为背景时，不透明度 ≤35%，并且压暗；不与前景矢量图抢主体。
2. 画面角落标“氛围插图 · 非科学数据”（若停留超过 3 秒）。
3. 不与真实照片混用在同一构图里冒充“实拍”；AI 图就是 AI 图。
4. 若操作员不接受 AI 图，整组可弃用，不影响科学内容。

## 4. 许可

- 模型：Stable Diffusion v1.5，CreativeML Open RAIL-M。生成图可用于本项目；模型权重不随视频分发。
- 生成图：本项目生成，不包含第三方受版权保护的图像输入（text-to-image，无图生图）。
- 若未来改用 SDXL/Flux 或在线服务，需要重新记录模型许可与服务条款。

## 5. 复现

```bash
cd "/home/lanshuye/文档/科普视频"
HF_ENDPOINT=https://hf-mirror.com \
  /home/lanshuye/miniconda3/envs/qwen3-tts/bin/python \
  scripts/build_s02_illustrations.py
.venv/bin/python scripts/grade_s02_illustrations.py
```

依赖：`diffusers==0.31.0`、`transformers==4.57.3`、`torch`（CUDA）、`Pillow`、`numpy`。 checkpoint 路径见脚本顶部 `CKPT`。

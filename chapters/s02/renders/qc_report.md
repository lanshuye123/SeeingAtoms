# S02 交付前自检报告

> 日期：2026-11-02
> 成片：`chapters/s02/renders/s02_final.mp4`
> 字幕：`chapters/s02/renders/s02_narration.srt` / `s02_final.ass`
> 封面：`chapters/s02/renders/cover.png` / `cover_4x3_preview.png`

## 1. 技术规格

| 项 | 结果 |
|---|---|
| 容器/编码 | MP4 / H.264 High + AAC LC |
| 分辨率 | 1920×1080 |
| 帧率 | 30 fps |
| 时长 | 621.08 s（10:21.08；旁白 9:13 + 片尾 1:08） |
| 文件大小 | 约 45.9 MB |
| 视频码率 | 约 0.39 Mbps（大量平涂矢量画面，CRF 19） |
| 音频 | 48 kHz，双声道，192 kbps |
| 综合响度 | −16.2 LUFS |
| 峰值 | 约 −4.3 dBFS |
| 解码测试 | `ffmpeg -f null -` 通过 |
| 字幕 | 157 条 SRT；ASS 烧录正常 |
| 封面 | 1920×1080（16:9）；中心 4:3 裁切 1440×1080 检查通过 |
| SHA-256（成片） | `4163183bf29cf646ddcff3e2aaa270e2ae2d017fd562bd85aec70d83648f5c4b` |
| SHA-256（封面） | `c713b3788e2c3325eb04202c3a8634777e40dbf078b4fae2b37bbb725cd984e3` |

## 2. 时间轴

场景段按 `timing.json` 的“下一场景起点 − 当前起点”取长度，因此包含场景之间的 0.65 s 停顿；成片总长与音频一致。

| 场景 | 起 | 时长 | 内容 |
|---|---|---|---|
| S00 | 0.00 | 41.97 | 铜网、样品杆、绿屏、ZnS 颗粒、模糊→清晰、原子列 |
| S01 | 41.97 | 83.35 | 电子与样品作用、厚度、制样五步、薄区 |
| S02 | 125.31 | 91.54 | 波长、理论/实际分辨率、磁透镜、球差、校正器 |
| S03 | 216.85 | 83.76 | 成像/衍射模式、选区光阑、衍射角、倒易杆 |
| S04 | 300.61 | 99.41 | 相位衬度、离焦反转、投影、参数、模拟对照、HAADF |
| S05 | 400.02 | 58.80 | 模拟像、3.9 Å、参数、缺陷、投影重叠、倾转 |
| S06 | 458.82 | 67.66 | 辐照损伤、低剂量、冷冻、取样、XRD 平均 |
| S07 | 526.48 | 26.61 | 两张结果卡、问题、下一期钩子 |
| 片尾 | 553.09 | 68.00 | 黑底滚动字幕 |

## 3. 音画同步

- 旁白：90 句逐句 TTS，句级 `timing.json`；整稿 553.09 s。
- 视频：各场景段按句级时间轴裁切/补帧；段间 0.65 s 停顿与音频一致。
- 音轨：旁白 −18 LUFS，配乐床轨 −30 LUFS，混后 −16.2 LUFS。
- 已核对：成片 621.08 s = 旁白 553.09 s + 片尾 68.00 s − 0.01 s 取整。
- 句级视觉锚点在渲染时由 `TimelineScene.cue()` 等待该句 `start`；片尾前无旁白。

## 4. 字幕

- 157 条，按句切分；单行 ≤22 字，无双行超长。
- 字体：思源黑体 CN；字号 46（1080p）；底部居中，MarginV 42。
- 时间轴与旁白共用同一 `timing.json`；片尾无字幕。
- 术语统一：X 射线、电子显微镜、球差、相位衬度、选区电子衍射、倒易杆、HAADF、Z 衬度。
- 已知：字幕按语义切分，不逐字对齐；正式发布前建议人工通读一遍。

## 5. 封面

- 1920×1080，16:9；核心标题、模拟像、角标均在居中 4:3 安全区（x=240–1680）。
- 封面图像为 SrTiO₃ [001] **模拟计算**，右下角标“模拟计算 · 非实测”。
- 中心 4:3 裁切 `cover_4x3_preview.png` 检查通过：标题、图像、角标均完整。

## 6. 内容与版权检查

- 成片未出现：终端、代码、路径、环境名、安装日志、工具水印、调试网格。
- 工具名只在片尾出现；正文只有科学概念、公式、单位和数据来源。
- 第三方图像：CDC 1965 TEM、NIST 石墨烯芯片、NIST 月尘 SEM；许可与哈希见 `assets/cc0/LICENSES.md`。
- 模拟 HRTEM 标“模拟计算 · 非实测”；S05 开篇即标注，不冒充实拍。
- 配乐：原创 MIDI + LMMS + GeneralUser GS；无商业录音采样。
- AI 氛围插图只做背景/质感；不承担科学结构示意。

## 7. 已知问题

1. S04/S05 以文字与单张示意图为主，部分镜头静止 4–8 秒；这是为了让观众读图，不是渲染错误。
2. S00 的铜网/电镜是 AI 氛围插图，不是实拍；画面已用标签与实拍图区分，但“铜网”质感仍偏纹理。
3. S01/S02/S03 的示意图为教学级简化（透镜、球差、倒易杆），不按厂商光路比例绘制。
4. 视频码率较低（平涂画面），在极低码率平台二次转码时可能出现色带；本地母版无此问题。
5. 片尾 68 s，字幕字号 15–18，1080p 可读，小屏偏小。

## 8. 复现

```bash
cd "/home/lanshuye/文档/科普视频"
source scripts/env.sh
make s02-script
make s02-timeline
make s02-srt
.venv/bin/python scripts/build_s02_srt.py
.venv/bin/python scripts/build_s02_mix.py
.venv/bin/python scripts/build_s02_ass.py
# 渲染 S00–S07、片尾、封面：
.venv/bin/manim -qh --fps 30 --media_dir media chapters/s02/manim/scenes.py S00
# … S01–S07 同上
.venv/bin/manim -qh --fps 30 --media_dir media chapters/s02/manim/credits.py S02Credits
.venv/bin/manim -qh --fps 30 -s --media_dir media chapters/s02/manim/cover.py S02Cover
.venv/bin/python scripts/build_s02_video.py
```

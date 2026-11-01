# S02 原创配乐（MIDI + LMMS + SF2）

> 状态：v0.1，供审听；不是最终混音。
> 作曲/编曲：本项目原创；没有使用任何商业录音采样。
> 音色：GeneralUser GS SoundFont v1.471（S. Christian Collins），通过 LMMS 1.2.2 的 SF2 Player 演奏。

## 1. 结构

| 段 | 小节 | 和声 | 作用 |
|---|---|---|---|
| A | 1–8 | Am9 / Fmaj7 / Cmaj7 / G6 | 开场：铜网、绿屏、问题 |
| B | 9–16 | Dm9 / Am9 / Fmaj7 / Esus4 → E7sus4 | 原理：透镜、球差、相位 |
| A' | 17–24 | Am9 / Fmaj7 / Cmaj7 / G6 | 读图与边界 |
| Tail | 25–28 | Am9 / Fmaj7 / Am9 | 收束、留给下一期 |

- 速度：68 BPM，4/4；28 小节约 98.8 s。
- 配器：钢琴（program 0）、暖 pad（89）、大提琴（42）、钟琴（9）。
- 写法：钢琴用 8 分音符琶音，力度 68–105，带 ±5 tick 的人性化偏移；pad 两小节一换；大提琴只走根音；钟琴只在段落转折处出现。
- 没有鼓、没有 riser、没有“史诗”式堆叠；目标是“有人在旁边轻轻弹”，不是预告片。

## 2. 文件

| 文件 | 用途 |
|---|---|
| `s02_theme.mid` | 标准 MIDI，可在任意 DAW 改 |
| `s02_theme.mmp` | LMMS 1.2.2 工程，四条 SF2 Player 轨道，可直接打开 |
| `s02_theme.wav` | LMMS 原始渲染，48 kHz 立体声 |
| `s02_theme.norm.wav` | 床轨版：−23 LUFS，高低通 + 淡入淡出 |
| `waveform.png` / `spectrum.png` | 质检用波形/频谱 |
| `README.md` | 本文件 |

## 3. 在 LMMS 里改

```bash
lmms chapters/s02/assets/music/s02_theme.mmp
```

- 四条轨道分别对应 Piano / Pad / Cello / Bell；每条轨道的乐器是 `sf2player`，`src` 指向本机 GeneralUser GS。
- 如果换机器，把 `sf2player` 的 `src` 改成新路径，或在 LMMS 里重新加载 SoundFont。
- 想加混响：在轨道 FX 里加 LADSPA `Plate2x2` 或 Calf Reverb；当前只用了 SF2 自带的轻混响。
- 渲染：`lmms render s02_theme.mmp -o out.wav`（无界面时加 `QT_QPA_PLATFORM=offscreen`）。

## 4. 许可与署名

- **作品**：本项目原创，随视频使用；不需要第三方音乐授权。
- **音色库**：GeneralUser GS v1.471，License v2.0。原文要点：
  - 可用于个人/商业音乐创作，可修改；
  - 内含采样的权利随原采样；作者声明未使用商业 SoundFont/采样 CD，但无法 100% 追溯所有采样来源；
  - 本项目只把音色库用于渲染，不随视频再分发 SoundFont 文件。
- **署名建议**：片尾写“音乐：本片原创（LMMS + GeneralUser GS）”；许可证细节放 `docs/assets_and_licenses.md`，不放进画面。
- 如果未来要商用发行且需要更干净的采样链，可改用 FluidR3_GM（本机也有）或全合成音色重做；当前版本先用于审听。

## 5. 质检

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 s02_theme.wav
ffmpeg -hide_banner -i s02_theme.wav -af astats=metadata=1:reset=0 -f null -
ffmpeg -hide_banner -i s02_theme.norm.wav -af ebur128 -f null -
```

当前：原始峰值约 −9.5 dBFS，RMS 约 −24 dBFS；床轨约 −23 LUFS。混入旁白时建议再压 2–4 dB，或用侧链。

## 6. 待确认

1. 风格是否太“new age”、太薄；要不要减少钢琴、增加低频 drone。
2. 钟琴是否太亮；要不要换成电钢琴/马林巴。
3. 28 小节 loop 是否够用；正式制作时按场景做 3 段变体（开场/原理/边界），而不是一条 loop 铺到底。

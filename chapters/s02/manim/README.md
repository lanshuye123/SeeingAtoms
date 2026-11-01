# S02 Manim 动效层

> 目标：让镜头承担叙述，而不是给每句话配一个“出现动画”。
> 参考：3Blue1Brown 的 Manim 用法、Manim `MovingCameraScene` 文档、以及社区整理的 3b1b 风格实践。
> 原则：华丽来自**连续运动与信息层级**，不是堆特效；一个镜头只推进一步。

## 1. 参考与方法

| 参考 | 用到的做法 |
|---|---|
| [Manim `MovingCameraScene`](https://docs.manim.community/en/stable/reference/manim.scene.moving_camera_scene.html) | `self.camera.frame.animate.set(width=..., height=...).move_to(...)`：连续推拉/平移，保持 16:9 |
| [Manim PR #1037](https://github.com/ManimCommunity/manim/pull/1037)（`TransformMatchingTex` / `FadeTransform` 来自 3b1b/manim） | 公式/标签之间的“同源变换”，而不是淡出再淡入 |
| [3b1b/videos 源码镜像](https://github.com/www2341/3Blue1Brown.com_videos_animation_source_python) | 相机运动 + 单一连续变换 + 颜色编码；不依赖花哨转场 |
| [3b1b manim 仓库](https://github.com/3b1b/manim) | 早期 `ZoomedScene`、`ThreeDScene` 的镜头语言 |

3b1b 的做法可以概括成三句话：

1. **镜头是叙述者**：推近表示“注意这里”，拉远表示“看整体关系”。
2. **一个镜头一个念头**：不在同一秒里同时换背景、换文字、换图表。
3. **连续变换优于切镜**：能用一个 `Transform` 讲清楚的，不用淡入淡出。

## 2. S00 实际用到的手法

| 手法 | 文件/函数 | 作用 |
|---|---|---|
| 相机推拉 | `TimelineScene.camera_to()` | 从 16 单位宽推到 5.8，模拟“走进样品” |
| 等距 3D 晶格 | `effects.lattice_3d()` | 背景空间感；深度排序，不抢主体 |
| 原子柱旋转 | `effects.column_3d()` + `always_redraw` | 从俯视（一列原子叠成一个点）转到侧视（一列点） |
| 径向辉光 | `effects.radial_glow()` | 荧光屏/电子束的柔光；用多层圆避免图片 alpha 问题 |
| 颗粒逐颗点亮 | `LaggedStart(..., lag_ratio=0.07)` | ZnS:Cu 颗粒不是一起亮，像真实屏的颗粒感 |
| 中心闪光 | `Flash(..., num_lines=12)` | 只用于“聚焦/命中”两个时刻 |
| 文字写入 | `Write` / `FadeIn(shift=...)` | 问题与标签；不逐字念 |
| 暗底字幕 | `Rectangle(fill_color=BG, fill_opacity=0.85)` | 保证问题压在晶格上仍可读 |

## 3. 不要做的事

- 不做“粒子飞散 + 镜头光晕 + 电子音效”的通用科技片头。
- 不在同一镜头里同时做相机运动、对象形变、文字写入；留一个主动作。
- 不用每秒都在动的“呼吸感”；允许 0.5–1 s 静止，让观众读图。
- 不让装饰性 3D 压过科学内容：晶格是背景，原子柱是解释，主体仍是样品/屏幕/图像。
- 不把模拟图做成“实拍感”；角标“模拟计算 · 非实测”必须保留。

## 4. 代码入口

```text
chapters/s02/manim/common.py     TimelineScene：句级 cue + 相机推拉
chapters/s02/manim/effects.py    辉光、3D 晶格、原子柱、标签底板
chapters/s02/manim/sync_demo.py  S00 动效样片
chapters/s02/manim/scenes.py     S00–S07 正式场景（TimelineScene）
```

渲染：

```bash
cd "/home/lanshuye/文档/科普视频"
source scripts/env.sh
.venv/bin/manim -qm --fps 30 --media_dir media \
  chapters/s02/manim/sync_demo.py S02SyncDemo
```

> 注意：Manim 会缓存 partial movie；改了 `self.remove()` 这类非动画语句后，必须删
> `partial_movie_files/S02SyncDemo/` 再渲染，否则会看到旧帧。

## 5. 与系列风格的关系

S01 的视觉语言是“细线矢量 + 少动效”，S02 在此基础上加了三样：

- **空间**：等距晶格、样品/屏幕的前后层次；
- **连续镜头**：推近、拉远、平移，而不是硬切；
- **光的质感**：荧光屏的绿光、电子束的柔光。

仍然保留：深墨蓝底、暖白字、青绿/琥珀语义色、公式只出现一次、字幕安全区。

# S01 制作页

> 系列：看见原子
> 第一期：一束 X 射线，如何读出原子排列？
> 状态：**制作完成，待操作员验收。**
> 成片：`chapters/s01/renders/s01_final.mp4`
> 字幕：`chapters/s01/renders/s01_final.srt`（另附烧录用 `s01_final.ass`）

## 1. 本期内容

一小堆白色粉末，装在样品槽里。可见光看不见原子；换成波长为 1.54 埃的 X 射线，晶体把入射波散射成一幅衍射图。峰位告诉我们晶胞多大，峰高透露原子种类和位置，峰宽则和晶粒尺寸、应变、缺陷、仪器展宽纠缠在一起。随后用开放晶体结构数据库（COD）的单晶硅与金红石计算谱线做对照：峰位组合像指纹，物相鉴定靠的就是这个。它很擅长“平均结构”，但没法告诉你缺陷在哪颗晶粒里。结尾桥接到电子显微镜。

## 2. 交付物

| 文件 | 内容 |
|---|---|
| [`renders/s01_final.mp4`](renders/s01_final.mp4) | 最终成片，1920×1080 / 30 fps / H.264 / AAC，约 9:38 |
| [`renders/s01_final.srt`](renders/s01_final.srt) | 中文字幕，103 条 |
| [`renders/s01_final.ass`](renders/s01_final.ass) | 烧录用样式字幕（1920×1080） |
| [`renders/cover.png`](renders/cover.png) | 16:9 封面；核心内容在居中 4:3 安全区 |
| [`renders/cover_4x3_preview.png`](renders/cover_4x3_preview.png) | 封面中心 4:3 裁切检查图（非发布物） |
| [`script.md`](script.md) | 旁白稿、反 AI 味说明、术语、待确认项 |
| [`storyboard.md`](storyboard.md) | 分镜、画面、动画、字幕、计划时间轴 |
| [`fact_check.md`](fact_check.md) | 逐条科学事实核对 |
| [`plan.md`](plan.md) | 制作规划与风险记录 |
| [`assets/style_frame_01.png`](assets/style_frame_01.png) | 标题视觉样张（非成片） |
| [`assets/style_frame_02_bragg.png`](assets/style_frame_02_bragg.png) | 布拉格公式样张（非成片） |
| [`assets/cif/`](assets/cif/) | COD 单晶硅/金红石 CIF |
| [`assets/xrd_patterns.json`](assets/xrd_patterns.json) | COD 结构计算谱线数据 |

## 3. 规格

- 成片：约 9 分 38 秒（旁白 8:28 + 片尾 1:10）
- 画幅：1920×1080，30 fps
- 视频：H.264 High，yuv420p，CRF 19
- 音频：AAC 192 kbps，48 kHz，双声道；综合响度约 −16 LUFS
- 字幕：中文 SRT + 烧录 ASS；单行 ≤22 字，最多两行
- 配乐：项目自制 ambient pad（无第三方采样），低于旁白
- 字体：思源黑体/宋体、霞鹜文楷（SIL OFL 1.1）
- 公式：XeLaTeX + `S01_TEX_TEMPLATE`
- 晶体数据：COD 9008565（Si）、COD 9004141（金红石，25 °C）
- 片尾：黑色背景向上滚动，约 70 秒
- 封面：1920×1080，16:9；核心内容位于居中 1440×1080（4:3）安全区

## 4. 验收重点

1. **整体听感**：旁白是否自然、是否有“AI 味”；语速/停顿是否合适。
2. **科学表述**：布拉格条件、峰位/峰高/峰宽、Si/金红石峰位与“计算谱非实测”的标注。
3. **信息层级**：成片是否出现路径、命令、环境名、终端、日志、工具水印。
4. **字幕**：错别字、术语、断句、音画同步；字幕是否遮挡关键图形。
5. **片尾**：字体/工具/AI 协作/参考资料是否齐全；是否按要求不出现课程笔记、单位/学校。
6. **音画**：配乐是否压过旁白；片尾音乐是否自然收束。

## 5. 复现命令

```bash
cd "/home/lanshuye/文档/科普视频"
source scripts/env.sh

# 环境
bash scripts/check_env.sh

# 旁白片段（已生成）
python3 scripts/extract_narration.py
python3 scripts/build_audio.py
python3 scripts/build_srt.py
python3 scripts/build_ass.py

# 配乐
python3 scripts/build_music.py --main-duration 508.2 --credits-duration 70.0
python3 scripts/mix_audio.py

# 场景（已渲染）
make scenes        # 如 Makefile 已加入；否则按 docs/technical_route.md 的单场景命令
make credits

# 合成
make final
```

> 具体命令以 `scripts/README.md` 与 `Makefile` 为准。

## 6. 已知问题

- 5.3 的峰宽段按“先肯定晶粒尺寸关系，再补仪器/应变/缺陷”改写；如仍觉得否定感强，可再调语序。
- 片尾参考文献较长，字号 15；1080p 下可读，但在手机小屏上偏小。
- 字幕 103 条，个别长句拆成两条；需人工通读一遍。
- 成片中的“COD 结构计算”标注是数据来源说明，不是实测数据。
- 单位/学校/指导教师按操作员要求留到最后一期，本期不出现。

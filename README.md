# 看见原子

一套以 X 射线衍射与电子显微为主题的科普视频项目。项目把“观众看到的成片”与“操作员可见的技术文档”分开管理：最终视频只保留科学内容、必要署名与字幕；命令、路径、环境、日志和素材许可证都在 `docs/`、`scripts/` 和 `logs/` 中。

## 当前状态

- 阶段一：环境/工具/理论验证完成。
- 阶段二：S01 v0.3 文案、分镜、事实核对、制作规划完成。
- 阶段三：S01 已制作完成，成片在 `chapters/s01/renders/s01_final.mp4`，待操作员验收。

## 快速入口

| 目的 | 文件 |
|---|---|
| 系列定位与风格 | [`docs/program_mainline.md`](docs/program_mainline.md) |
| 反“AI 味”写作 | [`docs/writing_guide.md`](docs/writing_guide.md) |
| 三级信息架构 | [`docs/information_architecture.md`](docs/information_architecture.md) |
| 工具链与环境实测 | [`docs/technical_route.md`](docs/technical_route.md) |
| 参考资料与事实依据 | [`docs/references.md`](docs/references.md) |
| 字体/素材许可证 | [`docs/assets_and_licenses.md`](docs/assets_and_licenses.md) |
| 操作员日志 | [`docs/operator_notes.md`](docs/operator_notes.md) |
| 版本控制策略 | [`docs/repository_policy.md`](docs/repository_policy.md) |
| S01 制作页 | [`chapters/s01/README.md`](chapters/s01/README.md) |
| S01 旁白稿 | [`chapters/s01/script.md`](chapters/s01/script.md) |
| S01 分镜 | [`chapters/s01/storyboard.md`](chapters/s01/storyboard.md) |
| S01 成片 | [`chapters/s01/renders/s01_final.mp4`](chapters/s01/renders/s01_final.mp4) |

## 环境检查

```bash
cd "/home/lanshuye/文档/科普视频"
source scripts/env.sh
make fonts       # 字体二进制默认不入库
bash scripts/check_env.sh
cat logs/environment_check.txt
```

## 目录

```text
assets/fonts/       开源中文字体与许可证
chapters/s01/       第一期脚本、分镜、素材、音频、Manim、成片
docs/               系列设定、技术路线、参考、许可证、署名
logs/               环境检查与运行日志
scripts/            环境检查、旁白提取、构建/合成/质检脚本
src/                TTS 封装、Manim 主题与可复用代码
```

## 重要约定

- 成片不出现终端、代码、路径、环境名、安装日志、调试信息、工具水印。
- 科学结论以课程笔记为主，可靠来源交叉验证；不确定处先问操作员。
- 字体使用思源系列/霞鹜系列，许可证记录在 `docs/assets_and_licenses.md`。
- 未经操作员明确批准，不进入正式制作。

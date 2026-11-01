# S02 第三方图像素材与许可证

> 下载日期：2026-11-01
> 原则：只用公共领域（PD）、CC0 或明确允许再使用的素材；来源、作者、许可证、修改方式、哈希全部记录。
> 本目录中的图像只作为“真实物件/真实照片”的锚点；所有定量示意图仍由项目自制（Manim/计算）。

## 1. 已入库素材

| 文件 | 内容 | 作者/来源 | 许可证 | 署名要求 | 计划用途 |
|---|---|---|---|---|---|
| `cdc_tem_1965.jpg` | 1965 年 CDC 的透射电镜（TEM）历史照片，700×898 | CDC / C. Duncan；页面：<http://www.publicdomainfiles.com/show_file.php?id=13515915019118> | 公共领域（美国联邦政府作品） | 建议标注 “CDC / C. Duncan, 1965” | S02 开场/历史对照；说明“电镜是一台很大的仪器” |
| `nist_graphene_chips.jpg` | NIST 的石墨烯芯片与硬币比例照片，1430×1445 | NIST；页面：<https://www.nist.gov/image/graphene-chipsjpg> | 公共领域（美国联邦政府作品；页面标注 Credit NIST） | “Credit: NIST” | 说明“薄样品/器件”的真实尺度；可作转场 |
| `nist_moon_dust_sem.png` | NIST 的月尘颗粒扫描电镜（SEM）图，1024×768，含 1 µm 标尺与仪器信息栏 | NIST；页面：<https://www.nist.gov/image/moon-dust-particle-4-4> | 公共领域（美国联邦政府作品；页面标注 Credit NIST） | “Credit: NIST” | 与高分辨像对照：SEM 看形貌，TEM/HRTEM 看内部原子列 |

校验：

```text
c30f198102717571d188e4c63bce8fea7c244b89deed6f39535d88a1a6989775  cdc_tem_1965.jpg
7261483e9edeadbe4b113d7a26cb8e02aaf2b12f6b82890533c85c35388c6244  nist_graphene_chips.jpg
9f20dc8f56315b0ea6ae4645337b80857884d3ebef926dd6a34ca577886a60e7  nist_moon_dust_sem.png
```

## 2. 使用边界

- `cdc_tem_1965.jpg`：只作为历史仪器照片；不声称它是现代球差校正电镜。
- `nist_graphene_chips.jpg`：只是尺度参照；不是 S02 讨论的钛酸锶样品。
- `nist_moon_dust_sem.png`：是 SEM 形貌图，不是原子级图像；画面必须标注“SEM 形貌，非原子级”，避免与 HRTEM 混淆。
- 所有第三方图像在成片中均加极简来源标注；完整 URL、作者、许可证只放在本文件与视频说明栏。
- 如后续发现 NIST 页面存在第三方版权标注（Credit 非 NIST），立即替换，不进入成片。

## 3. 待补充

- 若操作员希望使用真实的原子级 HRTEM 实拍图：需要一张明确 CC0/PD 或书面授权的图像，并记录材料、带轴、加速电压、来源。当前项目没有找到满足条件的材料学 HRTEM 实拍图，因此 S05 使用**自算模拟图**（`assets/sim/`，标注“模拟计算，非实测”），不冒充实拍。
- 若使用 CC-BY 素材：需在片尾与说明栏写作者、作品名、许可证链接；当前未使用。

## 4. 相关文件

- 模拟 HRTEM：`../sim/sim_srtio3_001_sr_under.png`、`../sim/sim_srtio3_001_sr_over.png`、`../sim/sim_srtio3_001_sr_thick.png`、`../sim/sim_srtio3_001.json`
- AI 氛围插图：`../illustrations/`（生成参数、模型、种子、许可说明见该目录 `PROMPTS.md`）
- 配乐：`../music/`（原创 MIDI；音色来自 GeneralUser GS SoundFont，许可证见 `../music/README.md`）

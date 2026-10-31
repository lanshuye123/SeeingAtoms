# 片尾署名与滚动字幕

> 用于 S01 成片最后的黑色背景、向上滚动字幕（约 70 秒）。
> 画面只保留署名与参考资料；许可证全文、素材 URL 明细在 `docs/assets_and_licenses.md`。
> 按操作员 5.4：不出现课程笔记致谢；单位/学校留到最后一期；感谢字体及作者、工具及作者/机构、AI 协作，并列 GB/T 7714 格式参考资料。

## 1. 滚动内容

```text
看见原子
第一期
一束 X 射线，如何读出原子排列？

字体
思源黑体 / 思源宋体 — Adobe（SIL Open Font License 1.1）
霞鹜文楷 — LXGW（SIL Open Font License 1.1）

工具
FFmpeg — Fabrice Bellard 与 FFmpeg 团队
Manim — Manim Community
Qwen3-TTS — 阿里巴巴通义千问团队
Python — Python Software Foundation
TeX Live / XeLaTeX — TeX Users Group 与社区贡献者

AI 协作
DeepSeek-V4.1-Flash-1017

开放晶体结构数据
Crystallography Open Database (COD)：9008565、9004141
原始文献：Wyckoff (1963)；Meagher & Lager (1979)

参考资料（GB/T 7714）
[1] 叶李华. 科普创作经验谈：技巧、原则与怀疑精神[EB/OL]. (2020-04-03)[2026-10-31].
    https://www.chinawriter.com.cn/n1/2020/0403/c404080-31660301.html.
[2] 网易号. 「AI 味」的本质是什么？你可能搞错了！[EB/OL]. (2026-01-05)[2026-10-31].
    https://m.163.com/dy/article/KIGAVOME0511805E.html.
[3] 阿里云开发者社区. 去不掉的 AI 味儿[EB/OL]. (2026-09-19)[2026-10-31].
    https://developer.aliyun.com/article/1764611.
[4] BRAGG W H, BRAGG W L. The reflexion of X-rays by crystals[J].
    Proceedings of the Royal Society A, 1913, 88(605): 428-438.
    DOI: 10.1098/rspa.1913.0040.
[5] GRUENE T, MUGNAIOLI E. 3D electron diffraction for chemical analysis:
    instrumentation developments and innovative applications[J].
    Chemical Reviews, 2021, 121(19): 11823-11834. DOI: 10.1021/acs.chemrev.1c00207.
[6] CULLITY B D, STOCK S R. Elements of X-ray diffraction[M]. 3rd ed.
    Upper Saddle River: Prentice Hall, 2001.
[7] WILLIAMS D B, CARTER C B. Transmission electron microscopy:
    a textbook for materials science[M]. 2nd ed. New York: Springer, 2009.
[8] WYCKOFF R W G. Crystal structures[M]. 2nd ed. New York:
    Interscience Publishers, 1963: 7-83.
[9] MEAGHER E P, LAGER G A. Polyhedral thermal expansion in the TiO2
    polymorphs: refinement of the crystal structure of rutile and brookite
    at high temperature[J]. The Canadian Mineralogist, 1979, 17: 77-85.
[10] NIST. X-ray transition energies database[DB/OL]. [2026-10-31].
     https://physics.nist.gov/PhysRefData/XrayTrans/Html/search.html.
[11] OpenStax. University physics: volume 3[EB/OL]. [2026-10-31].
     https://openstax.org/books/university-physics-volume-3/pages/4-6-x-ray-diffraction.

看见原子 · 第一期
下期：电子显微镜，如何把原子“拍”出来？
感谢观看
```

## 2. 实现

- 场景：`chapters/s01/manim/credits.py`，纯黑背景 `#000000`，文字居中，匀速向上滚动。
- 时长：约 70 秒；最后音乐渐弱。
- 字号：标题 40，段落标题 22，正文 18，参考文献 15。
- 不出现软件版本号、路径、日志、课程内部信息。
- 参考文献按 GB/T 7714 的顺序编码格式；URL 过长时在画面内换行。

## 3. 待确认

- 若最后一期需要加入单位/学校/指导教师，另起一段，不修改本期片尾。
- 若操作员希望 AI 协作署名换一种措辞（如“AI 辅助制作”），只需改 `credits.py` 一行。

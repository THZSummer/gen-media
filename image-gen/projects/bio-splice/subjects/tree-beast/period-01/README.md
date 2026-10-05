# 第一期 · 兽皮的树

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/tb-r7-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 12101 / 12102 / 12103**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**雾林 · 柔光 · 平视 · 方**

雾把林地压成一片灰绿，树干成为画面里唯一的"实体"——
**本期的主角是树干表面的材质**，所以用柔光（硬光会在树皮纹理上打出一堆干扰阴影）。

## 二、本期主题与结果

**底座 ＝ 老树（腾出版：不写树皮）**　**移植件 ＝ 兽皮纹 K1**

| 部位 | 编号 | 落点 | 结果 |
|------|------|------|------|
| 兽皮纹 | K1 | 树皮（**属性**） | ✅ 成立：树干上出现一条明显的兽皮/毛皮带 |

⚠️ 底座用**腾出版**是有意的（规律 96/100）：占用版（照常写 `rough fissured bark`）只到 4.25，
腾掉树皮描述后，兽皮与周围树皮的材质差别一眼可辨（4.55）。

## 三、成品

| # | 文件 | 评分 | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-tree-hide.png`](01-tree-hide.png) | **4.55** ✅ 首选 | `9c4de578` | `a2f7354faf` |
| 2 | [`02-tree-hide-b.png`](02-tree-hide-b.png) | **4.55** ✅ 首选 | `12886056` | `0a99c15554` |
| 3 | [`03-tree-hide-c.png`](03-tree-hide-c.png) | **4.55** ✅ 首选 | `a2214d66` | `1e60fb1b8f` |

对照：[`controls/tree.png`](controls/tree.png) —— **同轮**的纯树底座（腾出版）。

## 四、本期验证

1. **纹理是属性，可以腾出**：树皮纹理删得掉，所以腾出版有效——
   与 cordyceps 的虫体表、flytrap 的缘齿同型（规律 96/100）。
2. 材质替换只到"部分成立"（A=4）：兽皮与树皮的边界仍然可见接缝，如实给分。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject tree-beast 7 --dry
python3 run_round.py --subject tree-beast 7
python3 score.py --round work/tree-beast/r7/round.json --scores work/tree-beast/r7/scores.json \
    --control base-tree --region bark=250,200,550,500 \
    --audit-sheet subjects/tree-beast/rounds/tb-r7-audit.jpg \
    --subject tree-beast -o subjects/tree-beast/rounds/tb-r7-review.md
python3 curate.py --period subjects/tree-beast/period-01 --from work/tree-beast/r7/round.json \
    --pick tree-hide=01-tree-hide --pick tree-hide-b=02-tree-hide-b --pick tree-hide-c=03-tree-hide-c \
    --control base-tree=controls/tree --note "…" --force
bash make_sheet.sh period subjects/tree-beast/period-01
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第一期【兽皮的树】交付 3 张（腾出版底座） | 小七 |

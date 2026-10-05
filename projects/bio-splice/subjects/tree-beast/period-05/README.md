# 第五期 · 树兽（收官）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/tb-r6-review.md)
> 引擎：Z-Image-Turbo　**1280×1024**　steps 12　**seed 12101 / 12102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**暮色林 · 逆光剪影 · 广角 24mm · 横幅 1280×1024**

收官把整棵树放进暮色逆光里：树干上覆着兽皮、顶端挑着弯角——
**"树兽"这个形象在剪影里最完整**（斜光会把材质的接缝暴露出来，剪影不会）。

## 二、本期主题与结果

**底座 ＝ 老树（腾出树皮）**　**移植件 ＝ 兽皮纹 K1 + 兽足 K2 + 兽角 K4**

| 部位 | 编号 | 结果 |
|------|------|------|
| 兽皮纹 | K1 | ✅ 成立 |
| 兽角 | K4 | ✅ 完整成立 |
| **兽足** | **K2** | ❌ **未落地**（根系区放大 ×1.6 逐张判读：根还是根） |

⚠️ **三件里成两件**，成品按 A=4 收——**如实标注，不粉饰**。

## 三、成品

| # | 文件 | 评分 | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-tree-beast.png`](01-tree-beast.png) | **4.55** ✅ 首选 | `d3280536` | `83d2a25ebd` |
| 2 | [`02-tree-beast-b.png`](02-tree-beast-b.png) | **4.55** ✅ 首选 | `d3875556` | `0ec6e3e829` |

对照：[`controls/tree.png`](controls/tree.png) —— **同轮**的纯树底座。

## 四、本期验证：兽足为什么落不下来（否定结论）

两条原因同时成立：

1. **落点是典范结构**：根系是树的器官（规律 99）；
2. **「足」需要一个关节/肢体作承载面**——树没有腿（规律 74/97）。

→ 与 dragon-nines 的「鹰爪必须先用四肢底座」**完全同型**。
这是本仓第一次在乙组出现"某个部位彻底做不成"的子主题，
教训写进 **规律 105**：**选件时要同时问"落点是不是典范结构"和"这件需要什么承载面"。**

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject tree-beast 6 --dry
python3 run_round.py --subject tree-beast 6
python3 score.py --round work/tree-beast/r6/round.json --scores work/tree-beast/r6/scores.json \
    --control base-tree --region trunk=300,150,680,600 \
    --audit-sheet subjects/tree-beast/rounds/tb-r6-audit.jpg \
    --subject tree-beast -o subjects/tree-beast/rounds/tb-r6-review.md
python3 curate.py --period subjects/tree-beast/period-05 --from work/tree-beast/r6/round.json \
    --pick tree-beast=01-tree-beast --pick tree-beast-b=02-tree-beast-b \
    --control base-tree=controls/tree --note "…" --force
bash make_sheet.sh period subjects/tree-beast/period-05
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第五期【树兽】交付 2 张（收官；兽足未落地已注明） | 小七 |

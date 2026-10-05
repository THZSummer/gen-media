# 第四期 · 枯木的皮与角

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/tb-r9-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 12101 / 12102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**霜晨 · 平光 · 方 —— 换底座（老树 → 枯立木）**

本期是唯一**换底座**的一期：把老树换成**枯立木**（裂开的枯干 + 裸露根），
没有一片叶子——于是树干上那层兽皮与那对弯角成了画面里唯一"活着"的东西。

## 二、本期主题与结果

**底座 ＝ 枯立木**　**移植件 ＝ 兽皮纹 K1 + 兽角 K4**

| 部位 | 编号 | 结果 |
|------|------|------|
| 兽皮纹 | K1 | ✅ 成立 |
| 兽角 | K4 | ✅ 完整成立 |

## 三、成品

| # | 文件 | 评分 | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-deadwood-hide-horns.png`](01-deadwood-hide-horns.png) | **5.00** ✅ 首选 | `259c4335` | `835d75520e` |
| 2 | [`02-deadwood-hide-horns-b.png`](02-deadwood-hide-horns-b.png) | **5.00** ✅ 首选 | `23348b95` | `d15c530971` |

对照：[`controls/tree.png`](controls/tree.png) —— **同轮**的纯枯立木（无兽皮、无角）。

## 四、本期验证

**换底座第一次「不降反稳」**（规律 106 的出处）：
老树 → 枯立木，K1 + K4 两件**同样成立**；
而 flower-bird 玉兰 → 百合时命中率从 5/5 掉到 1/2。

> **推测**：**属性替换（兽皮纹）与空面新增（兽角）对底座形态的依赖低**；
> 需要几何配合的落点（花心深浅、瓣型）更敏感。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject tree-beast 9 --dry
python3 run_round.py --subject tree-beast 9
python3 score.py --round work/tree-beast/r9/round.json --scores work/tree-beast/r9/scores.json \
    --control base-tree --region trunk=350,200,600,600 \
    --audit-sheet subjects/tree-beast/rounds/tb-r9-audit.jpg \
    --subject tree-beast -o subjects/tree-beast/rounds/tb-r9-review.md
python3 curate.py --period subjects/tree-beast/period-04 --from work/tree-beast/r9/round.json \
    --pick deadwood-hide-horns=01-deadwood-hide-horns \
    --pick deadwood-hide-horns-b=02-deadwood-hide-horns-b \
    --control base-tree=controls/tree --note "…" --force
bash make_sheet.sh period subjects/tree-beast/period-04
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第四期【枯木的皮与角】交付 2 张（换底座验证） | 小七 |

# 第二期 · 有眼的捕蝇草

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/ff-r4-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 10101 / 10102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**沼泽 · 平视叶面 · 方**

本期主角是**叶面上的那只眼**，所以机位改成**正对叶面**的平视，
用平光（阴天）避免叶面反光把眼的高光吃掉。

## 二、本期主题与结果

**底座 ＝ 捕蝇草（宽叶面版）**　**移植件 ＝ 眼 T2**

| 部位 | 编号 | 落点 | 结果 |
|------|------|------|------|
| 眼 | T2 | 叶面（植物上本来没有「眼」这个位置） | ✅ 成立：光滑的深色动物眼长在绿叶上，虹膜高光清楚 |

⚠️ **解剖扣分（C=4）**：这只眼**没有眼睑与眼窝**，放大看有「贴上去」的感觉。
按 101 号的假设，补一处「窝 / 睑 / 接缝」的写法可能能救——**尚未验证**。

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-flytrap-eye.png`](01-flytrap-eye.png) | T2（**主图**） | **4.80** ✅ 首选 | `748c5634` | `ec17d89aef` |
| 2 | [`02-flytrap-eye-b.png`](02-flytrap-eye-b.png) | T2（seed 10102） | **4.80** ✅ 首选 | `f7e08ea7` | `b35f881c02` |

对照：[`controls/flytrap.png`](controls/flytrap.png) —— **同轮**的纯捕蝇草（叶面上什么都没有）。

## 四、本期验证

1. **植物上「眼」是真·空位新增**：叶面是一个连续的自由面，没有典范结构占位（规律 99）。
2. 这是本子主题**唯一没给满分的一件**：跨界单件缺少解剖接缝，如实记录，不修饰。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject flytrap-fang 4 --dry
python3 run_round.py --subject flytrap-fang 4
python3 score.py --round work/flytrap-fang/r4/round.json --scores work/flytrap-fang/r4/scores.json \
    --control base-flytrap --region lobe=250,150,550,500 \
    --audit-sheet subjects/flytrap-fang/rounds/ff-r4-audit.jpg \
    --subject flytrap-fang -o subjects/flytrap-fang/rounds/ff-r4-review.md
python3 curate.py --period subjects/flytrap-fang/period-02 --from work/flytrap-fang/r4/round.json \
    --pick flytrap-eye=01-flytrap-eye --pick flytrap-eye-b=02-flytrap-eye-b \
    --control base-flytrap=controls/flytrap --note "…" --force
bash make_sheet.sh period subjects/flytrap-fang/period-02
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第二期【有眼的捕蝇草】交付 2 张（4.80，解剖如实扣分） | 小七 |

# 第一期 · 跃出水面

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/fb-r6-review.md)
> 引擎：Z-Image-Turbo　**1280×1024**　steps 12　**seed 6101 起（多 take 见出处表）**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**刚离水、水花未落 · 逆光 · 平视 100mm · 横幅 1280×1024**

时间线的第一格：鱼**刚刚**冲出水面，水花还在往下掉。横幅给跃起的弧线留出空间，逆光让水花与翼缘同时亮起来。

> 出水阶段是**期内恒定**的（每期只停在一个瞬间），
> **期间各异**：水线位置、机位、光线、画幅都不同——五期连起来是一条时间线。

## 二、本期主题与结果

**底座 ＝ 鱼（离水）**　**移植件 ＝ 鸟翼 B1**

| 部位 | 编号 | 结果 |
|------|------|------|
| 鸟翼 | B1 | ✅ **完整成立**：鱼躯干上长出一对完整的鸟翼，翼羽结构与鱼体衔接自然 |

> ⚠️ 本期是「生境硬约束」（规律 85）的**直接产物**：
> 同一个底座、同一句话，在水下 0% 落地，在水面之上 100% 落地。
> 所以 fish-bird 的每一期都必须是**离水**的场景。

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-fish-wings.png`](01-fish-wings.png) | B1（体侧的翼，**主图**） | **5.00** ✅ 首选 | `0e9dd46a` | `a172b859b4` |
| 2 | [`02-fish-wings-spread.png`](02-fish-wings-spread.png) | B1（从背上全展） | **5.00** ✅ 首选 | `1ffb64a8` | `b4876ccbe6` |

对照：[`controls/fish.png`](controls/fish.png) —— **同轮**的纯鱼底座（同 seed、同呈现、句式骨架相同）。

## 四、本期验证

1. **离水即落地**：这是「离水探针」（R4）之后第一个正式期，两个 take 全成。
2. 水花与逆光是**加分项**：它们让「刚出水」这个瞬间一眼可读，也把翼的存在感托起来。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject fish-bird 6 --dry
python3 run_round.py --subject fish-bird 6
python3 score.py --round work/fish-bird/r6/round.json --scores work/fish-bird/r6/scores.json \
    --control base-fish --region body=300,400,650,350 \
    --audit-sheet subjects/fish-bird/rounds/fb-r6-audit.jpg \
    --subject fish-bird -o subjects/fish-bird/rounds/fb-r6-review.md
python3 curate.py --period subjects/fish-bird/period-01 --from work/fish-bird/r6/round.json \
    --pick fish-wings=01-fish-wings --pick fish-wings-spread=02-fish-wings-spread \
    --control base-fish=controls/fish --note "…" --force
bash make_sheet.sh period subjects/fish-bird/period-01
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第一期【跃出水面】交付 2 张 | 小七 |

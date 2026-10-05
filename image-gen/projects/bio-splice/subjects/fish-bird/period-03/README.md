# 第三期 · 完全离水·双翼全展

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/fb-r8-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 6101 起（多 take 见出处表）**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**完全在空中 · 侧上方视角 · 逆光勾羽 · 方**

时间线的第三格：鱼**完全脱离水**，双翼全展。侧上方视角同时交代翼面与鱼身，逆光把每一根羽枝勾出来——本期是全子主题里最「飞行」的一张。

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
| 1 | [`01-fish-wings-spread.png`](01-fish-wings-spread.png) | B1（全展，**主图**） | **5.00** ✅ 首选 | `cda5a7ac` | `8e65b9366c` |
| 2 | [`02-fish-wings-spread-b.png`](02-fish-wings-spread-b.png) | B1（全展，seed 6102） | **5.00** ✅ 首选 | `4044a13f` | `6265b5be0f` |

对照：[`controls/fish.png`](controls/fish.png) —— **同轮**的纯鱼底座（同 seed、同呈现、句式骨架相同）。

## 四、本期验证

1. **完全离水是兼容性的满格状态**：翼的最大展开在这里才读得完整。
2. 与期 01/02 合看，三期正好是「渐次离开水」的三格：水花未落 → 水线穿过 → 完全在空中。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject fish-bird 8 --dry
python3 run_round.py --subject fish-bird 8
python3 score.py --round work/fish-bird/r8/round.json --scores work/fish-bird/r8/scores.json \
    --control base-fish --region body=250,300,520,380 \
    --audit-sheet subjects/fish-bird/rounds/fb-r8-audit.jpg \
    --subject fish-bird -o subjects/fish-bird/rounds/fb-r8-review.md
python3 curate.py --period subjects/fish-bird/period-03 --from work/fish-bird/r8/round.json \
    --pick fish-wings-spread=01-fish-wings-spread --pick fish-wings-spread-b=02-fish-wings-spread-b \
    --control base-fish=controls/fish --note "…" --force
bash make_sheet.sh period subjects/fish-bird/period-03
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第三期【完全离水·双翼全展】交付 2 张 | 小七 |

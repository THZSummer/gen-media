# 第三部分 · 四翼（皮）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/wa-r3-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 13101 / 13102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**洞窟口 · 硬光 · 方**

图鉴第三页：**背上一对蝙蝠皮翼**。洞窟口的硬光 + 深背景
把皮革质膜面与细长指骨读得很清楚——皮翼的"骨架感"是它的辨识点。

## 二、本期主题与结果

**底座 ＝ 中型鸟（保留原翼）**　**移植件 ＝ 蝙蝠皮翼 W3**

| 部位 | 编号 | 落点 | 结果 |
|------|------|------|------|
| 蝙蝠皮翼 | W3 | 背部（**空面**） | ✅ **完整成立** |

## 三、成品

| # | 文件 | 评分 | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-bird-bat.png`](01-bird-bat.png) | **5.00** ✅ 首选 | `605234aa` | `a8847bfeb3` |
| 2 | [`02-bird-bat-b.png`](02-bird-bat-b.png) | **5.00** ✅ 首选 | `c17087cf` | `0d04e7dfa3` |

对照：[`controls/bird.png`](controls/bird.png) —— **同轮**的纯鸟。

## 四、本期验证

皮翼与膜翅都是"真的翅"，但**材质完全不同**（皮革 vs 半透膜），
说明本册的差异来自**供体本身的形态**，不是呈现的差别。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject wing-atlas 3 --dry
python3 run_round.py --subject wing-atlas 3
python3 score.py --round work/wing-atlas/r3/round.json --scores work/wing-atlas/r3/scores.json \
    --control base-bird --region back=250,200,550,500 \
    --audit-sheet subjects/wing-atlas/rounds/wa-r3-audit.jpg \
    --subject wing-atlas -o subjects/wing-atlas/rounds/wa-r3-review.md
python3 curate.py --period subjects/wing-atlas/period-03 --from work/wing-atlas/r3/round.json \
    --pick bird-bat=01-bird-bat --pick bird-bat-b=02-bird-bat-b \
    --control base-bird=controls/bird --note "…" --force
bash make_sheet.sh period subjects/wing-atlas/period-03
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第三部分【四翼（皮）】交付 2 张 | 小七 |

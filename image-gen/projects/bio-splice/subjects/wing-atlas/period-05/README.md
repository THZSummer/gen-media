# 第五部分 · 四翼（鹤羽）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/wa-r8-review.md)
> 引擎：Z-Image-Turbo　**1280×1024**　steps 12　**seed 13101 / 13102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**秋林 · 逆光 · 广角 135mm · 横幅 1280×1024**

图鉴最后一页：**背上一对鹤的白翼**。秋林的暖色背景 + 逆光，
让白色羽翼在画面里成为最亮的东西——**双层翼**（自身褐色翼 + 背上白翼）
是这一页最清楚的图鉴关系。

## 二、本期主题与结果

**底座 ＝ 中型鸟（保留原翼）**　**移植件 ＝ 鹤的白翼 W5'**

| 部位 | 编号 | 落点 | 结果 |
|------|------|------|------|
| 鹤的白翼 | W5' | 背部（**空面**） | ✅ **完整成立**——本册最有说服力的一张 |

## 三、成品

| # | 文件 | 评分 | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-bird-crane.png`](01-bird-crane.png) | **5.00** ✅ 首选 | `16b5234d` | `bbc5d2b45c` |
| 2 | [`02-bird-crane-b.png`](02-bird-crane-b.png) | **5.00** ✅ 首选 | `dd523efc` | `bf4e43b47b` |

对照：[`controls/bird.png`](controls/bird.png) —— **同轮**的纯鸟。

## 四、本期验证

1. **"是翅" + "不同形" = 最稳的组合**：鹤翼本身是翅（规律 107），
   且白色长翼与自身褐色短翼在**形状与颜色上都不同形**（规律 91）。
2. 收官页把整册的逻辑收束成一句话：
   **同一只鸟，背上换四次翅——图鉴的六页（基准 + 四种 + 本页）就此闭合。**

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject wing-atlas 8 --dry
python3 run_round.py --subject wing-atlas 8
python3 score.py --round work/wing-atlas/r8/round.json --scores work/wing-atlas/r8/scores.json \
    --control base-bird --region back=300,200,600,500 \
    --audit-sheet subjects/wing-atlas/rounds/wa-r8-audit.jpg \
    --subject wing-atlas -o subjects/wing-atlas/rounds/wa-r8-review.md
python3 curate.py --period subjects/wing-atlas/period-05 --from work/wing-atlas/r8/round.json \
    --pick bird-crane=01-bird-crane --pick bird-crane-b=02-bird-crane-b \
    --control base-bird=controls/bird --note "…" --force
bash make_sheet.sh period subjects/wing-atlas/period-05
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.5 | 第五部分【四翼（鹤羽）】交付 2 张（收官） | 小七 |

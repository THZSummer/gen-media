# 第一部分 · 双翼基准

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/wa-r1-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 13101 / 13102 / 13103**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**枝头 · 侧逆光 · 平视 400mm · 方**

图鉴的**第一页**：统一底座本身。侧逆光把鸟的轮廓与羽缘勾出来，
平视机位是后面四部分共用的机位规格。

## 二、本期主题与结果

**底座 ＝ 中型鸟**　**移植件 ＝ 无（基准部分）**

⚠️ 本部分**刻意不放移植件**（规律 108）：它是后四部分的**参照系**——
"第二对翅"是在这只鸟的基础上"多出来的那一对"，没有基准就读不出"多"。

因此本部分**没有对照镜头**（基准本身就是对照），
客观指标一栏为空——已在 [复核报告](../rounds/wa-r1-review.md) 里如实标注。

## 三、成品

| # | 文件 | 评分 | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-bird-baseline.png`](01-bird-baseline.png) | **5.00** ✅ 首选 | `3d80eb6b` | `4f2884affc` |
| 2 | [`02-bird-baseline-b.png`](02-bird-baseline-b.png) | **5.00** ✅ 首选 | `ac1ca1f9` | `33e5fd555f` |
| 3 | [`03-bird-baseline-c.png`](03-bird-baseline-c.png) | **5.00** ✅ 首选 | `62cb1c60` | `99fdabc314` |

## 四、本期验证

**"基准部分"是图鉴册的骨架**（规律 108）：
本册与 `horn-atlas` 都采用「第 1 部分 = 基准，第 2–5 部分 = 四种候选器官」的结构。
→ 好处：读者一眼能看出"加的是什么"，也是后续做 A/B 对照的天然锚点。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject wing-atlas 1 --dry
python3 run_round.py --subject wing-atlas 1
python3 score.py --round work/wing-atlas/r1/round.json --scores work/wing-atlas/r1/scores.json \
    --region back=250,200,550,500 \
    --audit-sheet subjects/wing-atlas/rounds/wa-r1-audit.jpg \
    --subject wing-atlas -o subjects/wing-atlas/rounds/wa-r1-review.md
python3 curate.py --period subjects/wing-atlas/period-01 --from work/wing-atlas/r1/round.json \
    --pick base-bird=01-bird-baseline --pick base-bird-b=02-bird-baseline-b \
    --pick base-bird-c=03-bird-baseline-c --note "…"
bash make_sheet.sh period subjects/wing-atlas/period-01
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第一部分【双翼基准】交付 3 张（图鉴的参照系） | 小七 |

# 第四部分 · 四翼（飞鱼鳍）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/wa-r7-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 13101 / 13102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**水边 · 湿润光 · 方**

图鉴第四页：**背上一对飞鱼的长鳍**。水边湿润的反光与长鳍的流线呼应，
这一页的材质是"薄而硬的鳍条"，与膜翅、皮翼都不同。

## 二、本期主题与结果

**底座 ＝ 中型鸟（保留原翼）**　**移植件 ＝ 飞鱼长鳍 W4'**

| 部位 | 编号 | 落点 | 结果 |
|------|------|------|------|
| 飞鱼长鳍 | W4' | 背部（**空面**） | ✅ **完整成立** |

## 三、成品

| # | 文件 | 评分 | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-bird-flyfish.png`](01-bird-flyfish.png) | **5.00** ✅ 首选 | `691b86a1` | `cb1d03c7b1` |
| 2 | [`02-bird-flyfish-b.png`](02-bird-flyfish-b.png) | **5.00** ✅ 首选 | `475699d5` | `d7332e52d8` |

对照：[`controls/bird.png`](controls/bird.png) —— **同轮**的纯鸟。

## 四、本期验证：**语义才是关键**（规律 107）

本页的供体来自**同一次追问**（R6），与失败的"鱼胸鳍"只差一个词：

| 供体 | 语义 | 结果 |
|------|------|------|
| `stiff fish pectoral fins` | 只是鳍 | ❌ **0%**（R4） |
| **`long gliding flying-fish fins`** | 鳍，但**自带「飞」** | ✅ 5.00 |

→ **光有"像翅的形状"不够，必须具备"能飞"的语义。**

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject wing-atlas 7 --dry
python3 run_round.py --subject wing-atlas 7
python3 score.py --round work/wing-atlas/r7/round.json --scores work/wing-atlas/r7/scores.json \
    --control base-bird --region back=250,200,550,500 \
    --audit-sheet subjects/wing-atlas/rounds/wa-r7-audit.jpg \
    --subject wing-atlas -o subjects/wing-atlas/rounds/wa-r7-review.md
python3 curate.py --period subjects/wing-atlas/period-04 --from work/wing-atlas/r7/round.json \
    --pick bird-flyfish=01-bird-flyfish --pick bird-flyfish-b=02-bird-flyfish-b \
    --control base-bird=controls/bird --note "…" --force
bash make_sheet.sh period subjects/wing-atlas/period-04
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第四部分【四翼（飞鱼鳍）】交付 2 张 | 小七 |

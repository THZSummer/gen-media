# 第一部分 · 无角基准

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/ha-r1-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 14101 / 14102 / 14103**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**晨雾草场 · 柔光 · 平视 400mm · 方**

图鉴的**第一页**：一匹**本来没有角**的马。晨雾与柔光让马体成为唯一的实体，
平视机位是后面四部分共用的机位规格。

## 二、本期主题与结果

**底座 ＝ 一匹标准马**　**移植件 ＝ 无（基准部分）**

⚠️ 本部分**刻意不放移植件**（规律 108）：它是后四部分的**参照系**——
"多了一支角"这件事，没有基准就读不出来。

因此本部分**没有对照镜头**（基准本身就是对照），客观指标一栏为空，已在 review 里注明。

## 三、成品

| # | 文件 | 评分 | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-horse-baseline.png`](01-horse-baseline.png) | **5.00** ✅ 首选 | `e583728c` | `1353e1632e` |
| 2 | [`02-horse-baseline-b.png`](02-horse-baseline-b.png) | **5.00** ✅ 首选 | `55b60755` | `55278e9261` |
| 3 | [`03-horse-baseline-c.png`](03-horse-baseline-c.png) | **5.00** ✅ 首选 | `542be338` | `5adc76e8c7` |

## 四、本期验证

**「无角」本身就是本册的关键设计**（规律 99）：
马没有角 → 额顶/鼻梁是**空面** → 后四部分的角不需要腾占位、也不需要承载结构，
"五条门槛全过"从这里就开始了。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject horn-atlas 1 --dry
python3 run_round.py --subject horn-atlas 1
python3 score.py --round work/horn-atlas/r1/round.json --scores work/horn-atlas/r1/scores.json \
    --region head=350,100,400,400 \
    --audit-sheet subjects/horn-atlas/rounds/ha-r1-audit.jpg \
    --subject horn-atlas -o subjects/horn-atlas/rounds/ha-r1-review.md
python3 curate.py --period subjects/horn-atlas/period-01 --from work/horn-atlas/r1/round.json \
    --pick base-horse=01-horse-baseline --pick base-horse-b=02-horse-baseline-b \
    --pick base-horse-c=03-horse-baseline-c --note "…"
bash make_sheet.sh period subjects/horn-atlas/period-01
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第一部分【无角基准】交付 3 张（图鉴的参照系） | 小七 |

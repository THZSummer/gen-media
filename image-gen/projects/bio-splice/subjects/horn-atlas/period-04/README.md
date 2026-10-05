# 第四部分 · 羊角

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/ha-r4-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 14101 / 14102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**晨雾草场 · 侧逆光 · 平视 · 方**

羊角是**卷曲**的（盘旋在耳侧），所以本页回到侧逆光：
让卷曲的每一圈都有明暗交界，这一册里**辨识度最高的一件**。

## 二、本期主题与结果

**底座 ＝ 一匹无角的马**　**移植件 ＝ 卷曲羊角 H3**

| 部位 | 编号 | 落点 | 结果 |
|------|------|------|------|
| 羊角 | H3 | 额顶（**空面**） | ✅ **完整成立**：一对卷曲羊角盘旋在耳侧 |

## 三、成品

| # | 文件 | 评分 | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-horse-ramhorns.png`](01-horse-ramhorns.png) | **5.00** ✅ 首选 | `6ed1cad0` | `9552daafa3` |
| 2 | [`02-horse-ramhorns-b.png`](02-horse-ramhorns-b.png) | **5.00** ✅ 首选 | `53cc94ad` | `a2f498cf0e` |

对照：[`controls/horse.png`](controls/horse.png) —— **同轮**的纯马。

## 四、本期验证

同样是"角"，**鹿角是分叉、牛角是直弯、羊角是卷曲**——
三种形态在同一底座上互不混淆，说明本册的图鉴价值来自**供体形态的差异**，
而不是呈现的花样。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject horn-atlas 4 --dry
python3 run_round.py --subject horn-atlas 4
python3 score.py --round work/horn-atlas/r4/round.json --scores work/horn-atlas/r4/scores.json \
    --control base-horse --region head=350,80,400,400 \
    --audit-sheet subjects/horn-atlas/rounds/ha-r4-audit.jpg \
    --subject horn-atlas -o subjects/horn-atlas/rounds/ha-r4-review.md
python3 curate.py --period subjects/horn-atlas/period-04 --from work/horn-atlas/r4/round.json \
    --pick horse-ramhorns=01-horse-ramhorns --pick horse-ramhorns-b=02-horse-ramhorns-b \
    --control base-horse=controls/horse --note "…" --force
bash make_sheet.sh period subjects/horn-atlas/period-04
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第四部分【羊角】交付 2 张 | 小七 |

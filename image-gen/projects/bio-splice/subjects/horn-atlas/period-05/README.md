# 第五部分 · 独角鲸长牙 / 犀角（收官）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/ha-r5-review.md)
> 引擎：Z-Image-Turbo　**1024×1280**　steps 12　**seed 14101 / 14102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**霜晨草原 · 侧逆光 · 贴面特写 · 竖 1024×1280**

收官从"成对的角"走到**单支的角**，并换成**贴面特写**：
霜晨的侧逆光下，螺旋的纹路与鼻梁上的角质都被放大到能看清质感。

## 二、本期主题与结果

**底座 ＝ 一匹无角的马**　**移植件 ＝ 独角鲸长牙 H5 + 犀角 H4**

| 部位 | 编号 | 落点 | 结果 |
|------|------|------|------|
| 独角鲸长牙 | H5 | 额顶（**空面**） | ✅ **完整成立**：一支长螺旋长牙 |
| 犀角 | H4 | **鼻梁**（空面） | ✅ **完整成立**：一支厚重的角质角 |

## 三、成品

| # | 文件 | 评分 | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-horse-narwhal.png`](01-horse-narwhal.png) | **5.00** ✅ 首选 | `b72a2d5c` | `04ffb9b2a0` |
| 2 | [`02-horse-rhino.png`](02-horse-rhino.png) | **5.00** ✅ 首选 | `ab66b26e` | `58a184dc02` |

对照：[`controls/horse.png`](controls/horse.png) —— **同轮**的纯马（特写机位）。

## 四、本期验证

1. **长牙不是角，但形态救回了语义**（规律 110）：独角鲸的长牙解剖上是"牙"，
   但"一支向上的螺旋"的形态被模型接受了——**形态与语义同时成立时，语义的小偏差会被带过去**。
2. 收官页完成图鉴的闭合：**从无角 → 成对的角（鹿/牛/羊）→ 单支的角（额顶/鼻上）**。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject horn-atlas 5 --dry
python3 run_round.py --subject horn-atlas 5
python3 score.py --round work/horn-atlas/r5/round.json --scores work/horn-atlas/r5/scores.json \
    --control base-horse --region head=300,80,450,500 \
    --audit-sheet subjects/horn-atlas/rounds/ha-r5-audit.jpg \
    --subject horn-atlas -o subjects/horn-atlas/rounds/ha-r5-review.md
python3 curate.py --period subjects/horn-atlas/period-05 --from work/horn-atlas/r5/round.json \
    --pick horse-narwhal=01-horse-narwhal --pick horse-rhino=02-horse-rhino \
    --control base-horse=controls/horse --note "…" --force
bash make_sheet.sh period subjects/horn-atlas/period-05
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第五部分【独角鲸长牙 / 犀角】交付 2 张（收官） | 小七 |

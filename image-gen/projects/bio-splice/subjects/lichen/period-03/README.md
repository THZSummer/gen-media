# 第三期 · 枝状地衣

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/lc-r3-review.md)
> 引擎：Z-Image-Turbo　**1024×1280**　steps 12　**seed 8101 / 8103**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**冻原 · 逆光 · 微距低机位 · 竖 1024×1280**

枝状地衣是**立起来**的（像小灌木），所以用低机位竖幅看它的高度；
冻原逆光把顶端的白粉霜勾亮。

## 二、本期主题与结果

**底座 ＝ 真菌菌丝体**　**移植件 ＝ 枝状体 FR1**

| 部位 | 编号 | 结果 |
|------|------|------|
| 枝状体 | FR1 | ✅ 成立：密密分叉、顶端带白色粉霜，像一丛石蕊 |

⚠️ **底座自带分叉**：菌丝体的描述里本来就有 `branching threads`，
它在冻原上自己就长成了珊瑚状——所以枝状件只贡献了「更密 + 白粉霜」，A 给 4。

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-mycelium-fruticose.png`](01-mycelium-fruticose.png) | FR1（**主图**） | **4.55** ✅ 首选 | `0bb08aee` | `acf842d977` |
| 2 | [`02-mycelium-fruticose-b.png`](02-mycelium-fruticose-b.png) | FR1（seed 8103） | **4.55** ✅ 首选 | `8313748e` | `bdec631b14` |

对照：[`controls/mycelium.png`](controls/mycelium.png) —— **同轮**的纯菌丝体底座。

## 四、本期验证

1. **对照已经把一半做完了就要扣分**（规律 95）：底座自己带分叉形态，
   移植件的边际贡献要如实评估（4.55 而不是 5.00）。
2. 竖幅 + 低机位在**非动物**题材上是安全的——规律 80 的坑（末端部件被画成另一个体）
   只适用于会「长出肢体」的动物底座。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject lichen 3 --dry
python3 run_round.py --subject lichen 3
python3 score.py --round work/lichen/r3/round.json --scores work/lichen/r3/scores.json \
    --control base-mycelium --region subject=250,250,520,700 \
    --audit-sheet subjects/lichen/rounds/lc-r3-audit.jpg \
    --subject lichen -o subjects/lichen/rounds/lc-r3-review.md
python3 curate.py --period subjects/lichen/period-03 --from work/lichen/r3/round.json \
    --pick mycelium-fruticose=01-mycelium-fruticose --pick mycelium-fruticose-b=02-mycelium-fruticose-b \
    --control base-mycelium=controls/mycelium --note "…" --force
bash make_sheet.sh period subjects/lichen/period-03
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第三期【枝状地衣】交付 2 张（4.55，如实扣分） | 小七 |

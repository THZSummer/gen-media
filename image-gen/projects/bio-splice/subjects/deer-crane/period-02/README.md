# 第二期 · 鹤腿的鹿

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/dc-r2-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 7101 起（多 take 见出处表）**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**浅水沼泽 · 晨光 · 平视全身 400mm · 方**

涉禽的腿只有站在浅水里才读得出来：水面给出了「腿有多长」的参照，晨光在水面上拉出反光，把腿的轮廓托出来。

> 呈现层**期内恒定**（该期所有镜头含对照共用一套），**期间各异**（五期各有身份）。

## 二、本期主题与结果

**底座 ＝ 鹿**　**移植件 ＝ 鹤的细腿 G2（底座**不写腿**，腾出腿位）**

| 部位 | 编号 | 结果 |
|------|------|------|
| 细腿 | G2 | ⚠️ **部分成立**：腿变细变长、关节感向涉禽靠；**但仍是鹿的褐色皮毛 + 蹄** |

**同轮之外还做了一版对照**（R3）：底座照常写 `four long legs`（不腾位），结果与腾出版**几乎相同**——这条对照写在 [dc-r1-r6.md](../rounds/dc-r1-r6.md)。

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-deer-cranelegs.png`](01-deer-cranelegs.png) | G2（**主图**） | **4.25** ✅ 成品 | `ee9581d9` | `35cf81506f` |
| 2 | [`02-deer-cranelegs-b.png`](02-deer-cranelegs-b.png) | G2（seed 7102） | **4.25** ✅ 成品 | `2b0b1816` | `218c14f8f8` |

对照：[`controls/deer.png`](controls/deer.png) —— **同轮**的纯鹿底座（同 seed、同呈现、句式骨架相同）。

## 四、本期验证

1. **腾出占位对典范结构既不加分也不减分**（R2 vs R3）：腿的长短被改变了，但材质（褐色 + 蹄）没变——决定成败的是材质。
2. 原定「低机位 · 竖」按规律 80 改为平视全身：末端部件在低机位竖幅下会被画成另一个体。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject deer-crane 2 --dry
python3 run_round.py --subject deer-crane 2
python3 score.py --round work/deer-crane/r2/round.json --scores work/deer-crane/r2/scores.json \
    --control base-deer --region legs=350,550,350,400 \
    --audit-sheet subjects/deer-crane/rounds/dc-r2-audit.jpg \
    --subject deer-crane -o subjects/deer-crane/rounds/dc-r2-review.md
python3 curate.py --period subjects/deer-crane/period-02 --from work/deer-crane/r2/round.json \
    --pick deer-cranelegs=01-deer-cranelegs --pick deer-cranelegs-b=02-deer-cranelegs-b \
    --control base-deer=controls/deer --note "…" --force
bash make_sheet.sh period subjects/deer-crane/period-02
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第二期【鹤腿的鹿】交付 2 张（部分成立）；含 R3 占用版对照 | 小七 |

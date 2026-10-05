# 第一期 · 长颈的鹿

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/dc-r1-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 7101 起（多 take 见出处表）**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**晨雾竹林 · 柔光 · 平视 400mm · 方**

竹林的竖向线条与「长颈」这个主题同构，雾把背景压平，让颈的长度成为画面里唯一可读的方向。平视机位不仰不俯——颈的长度不被透视骗。

> 呈现层**期内恒定**（该期所有镜头含对照共用一套），**期间各异**（五期各有身份）。

## 二、本期主题与结果

**底座 ＝ 鹿**　**移植件 ＝ 鹤的长颈 G1（底座不写颈，腾出颈位）**

| 部位 | 编号 | 结果 |
|------|------|------|
| 长颈 | G1 | ⚠️ **部分成立**：颈明显变长变细、立起来，姿态向涉禽靠；但**没有鹤的灰色细羽**，身份仍偏鹿 |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-deer-craneneck.png`](01-deer-craneneck.png) | G1（**主图**） | **4.25** ✅ 成品 | `671ea052` | `06af7f6eb4` |
| 2 | [`02-deer-craneneck-b.png`](02-deer-craneneck-b.png) | G1（seed 7102） | **4.25** ✅ 成品 | `bb2dba96` | `ac89be033f` |

对照：[`controls/deer.png`](controls/deer.png) —— **同轮**的纯鹿底座（同 seed、同呈现、句式骨架相同）。

## 四、本期验证

1. **鹿的颈是典范结构**（规律 87）：删掉底座里的颈描述也没用——模型会自己补回一个颈，鹤颈句只能**改形状**（更长更细），改不动材质。
2. 本期如实给 A=3（部分到位），不因为「看起来更修长」就给满分。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject deer-crane 1 --dry
python3 run_round.py --subject deer-crane 1
python3 score.py --round work/deer-crane/r1/round.json --scores work/deer-crane/r1/scores.json \
    --control base-deer --region neck=380,150,300,300 \
    --audit-sheet subjects/deer-crane/rounds/dc-r1-audit.jpg \
    --subject deer-crane -o subjects/deer-crane/rounds/dc-r1-review.md
python3 curate.py --period subjects/deer-crane/period-01 --from work/deer-crane/r1/round.json \
    --pick deer-craneneck=01-deer-craneneck --pick deer-craneneck-b=02-deer-craneneck-b \
    --control base-deer=controls/deer --note "…" --force
bash make_sheet.sh period subjects/deer-crane/period-01
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第一期【长颈的鹿】交付 2 张（部分成立） | 小七 |
